

from typing import List, Dict, Callable, Any
from faker import Faker
from django.db import models
import random
from rest_framework.test import APITestCase
import pytz
import logging
import math
from rest_framework.test import APITestCase
from .utils import phightlight


logger = logging.getLogger('django')


FieldName = str


class FieldCustomGenerate:
    def __init__(
        self,
        name: str,
        gen: Callable
    ) -> None:
        self.name = name
        self.gen = gen
        
    def generate(self, data):
        return self.gen(data)


class FakeDataGenerator:
    
    DEFAULT_IGNORE_FIELD = [
        # 'id', 
        'created_at', 'updated_at'
    ]
    
    def __init__(self) -> None:
        # Faker.seed(0)
        # self.fake = Faker()
        pass
        
    def _get_fake_val(self, field) -> Any:
        
        val = None
        
        if isinstance(field, models.CharField):
            if field.choices:
                choice = self._field_name_to_fake_method[field.name].pyint(min_value=0, max_value=len(field.choices)-1)
                val = field.choices[choice][0]
            else:
                max_length = field.max_length
                val = self._field_name_to_fake_method[field.name].pystr(min_chars=max_length/max_length, max_chars=math.ceil(max_length/2))
        
        elif isinstance(field, models.TextField):
            val = self._field_name_to_fake_method[field.name].text()
        
        elif isinstance(field, (models.IntegerField, models.BigIntegerField)):
            val = self._field_name_to_fake_method[field.name].pyint(min_value=1, max_value=10000)
        
        elif isinstance(field, models.FloatField):
            val = self._field_name_to_fake_method[field.name].pyfloat(min_value=0, max_value=10000)
        
        elif isinstance(field, models.BooleanField):
            val = random.choice([True, False])
        
        elif isinstance(field, models.DateTimeField):
            val = self._field_name_to_fake_method[field.name].date_time(tzinfo=pytz.timezone('utc')).__str__()
        
        elif isinstance(field, models.DateField):
            val = self._field_name_to_fake_method[field.name].date()
            
        elif isinstance(field, models.ForeignKey):
            try:
                relateds = field.related_model.objects.all()
                relateds_count = field.related_model.objects.count()
                # print(f'relateds_count {relateds_count}')
                max_value = relateds_count - 1
                related_choice = self._field_name_to_fake_method[field.name].pyint(min_value=0, max_value=max_value)
                selected_related = relateds[related_choice]
                val = getattr(selected_related, field.to_fields[0], None)
                if val is None:
                    val = selected_related.id
            except ValueError as val_err_exc:
                if field.null:
                    val = None
                else:
                    raise val_err_exc
            except Exception as exc:
                raise exc
        
        elif isinstance(field, models.JSONField):
            val = {
                "Name": self.fake.name(),
                "Email": self.fake.email(),
                "Country": self.fake.country(),
            }
        
        return val

    def generate(
        self,
        model, 
        qty: int=1,
        ignore_fields: List[str]=None, 
        ignore_fields_by_type: List[str]=None, 
        assert_filled: List[str]=None,
        assert_filled_by_type: List[str]=None,
        assert_unique: List[str]=None,
        custom_generate: List[FieldCustomGenerate]=None,
        faker_seed: int=random.randint(0,999999)
    ) -> Dict:
        if ignore_fields_by_type is None:
            ignore_fields_by_type = [models.BigAutoField]
            
        if assert_filled is None:
            assert_filled = []

        if assert_filled_by_type is None:
            assert_filled_by_type = [models.ForeignKey]

        if assert_unique is None:
            assert_unique = []

        if custom_generate is None:
            custom_generate = []

        
        self.fake = Faker()
        Faker.seed(faker_seed)
        
        is_instance_of_some = lambda field, instance_list: \
            len([x for x in instance_list if isinstance(field, x)]) > 0
        
        get_custom_generate = lambda field, custom_generate_list: [
                field_custom_gen
                for field_custom_gen in custom_generate_list 
                if field_custom_gen.name == field.name
            ]
            
        ########################
        ### Start-Up
        ########################
        if ignore_fields is None:
            ignore_fields = self.DEFAULT_IGNORE_FIELD
        self._field_name_to_fake_method = {}
        self._field_is_custom_gen = {}
        compute_fields = []
        for field in model._meta.fields:
            if field.name in ignore_fields \
            or is_instance_of_some(field, ignore_fields_by_type):
                continue
            compute_fields.append(field)
            custom_gen = get_custom_generate(field, custom_generate)
            is_custom_gen = len(custom_gen) > 0
            if is_custom_gen:
                custom_gen = custom_gen[0]
            self._field_is_custom_gen[field.name] = (is_custom_gen, custom_gen)
            # Insert pk on unique vals
            is_pk = getattr(field, 'primary_key', False)
            if is_pk or field.name in assert_unique:
                self._field_name_to_fake_method[field.name] = self.fake.unique
            else:
                self._field_name_to_fake_method[field.name] = self.fake
        data = []
        
        ########################
        ### Generate Data
        ########################        
        for _ in range(qty):
            data.append({}) 
            for field in compute_fields:
                field_is_custom_gen, custom_gen = self._field_is_custom_gen[field.name]
                
                try:
                    if field_is_custom_gen:
                        val = custom_gen.generate(data)
                    else:
                        val = self._get_fake_val(field)
                        if field.name not in assert_filled \
                        and not is_instance_of_some(field, assert_filled_by_type):
                            if field.null:
                                val = random.choice([None, val])
                            if field.blank:
                                val = random.choice(['', val])
                except Exception as exc:
                    print(f'field: {field.name}')
                    raise exc
                
                data[-1][field.name] = val
        return data


def test_method(
    url: str, 
    method: str, 
    api_test_case: APITestCase,
    format: str='json',
    token: str=None,
    data=None, 
):
    kwargs = {
        'path': url,
        'format': format,
        'data': data,
    }
    if token:
        kwargs['HTTP_AUTHORIZATION'] = 'Bearer ' + token
    return getattr(api_test_case.client, method)(**kwargs)
    
def test_create(
    url, 
    api_test_case: APITestCase, 
    format: str='json',
    token: str=None,
    data=None, 
):
    return test_method(
        url=url,
        method='post',
        api_test_case=api_test_case,
        format=format,
        token=token,
        data=data,
    )
    
    
ALREADY_PRINT_APP = {}
    

class TestSetUpPrintAppLabel(APITestCase):
    def setUp(self):
        already_print_app = ALREADY_PRINT_APP.get(self.APP_LABEL, None)
        if already_print_app is None:
            ALREADY_PRINT_APP[self.APP_LABEL] = False
        if not ALREADY_PRINT_APP[self.APP_LABEL]:
            print("\n" * 2 + "!" + "*" * 48 + "!")
            print(phightlight(self.APP_LABEL, size=50))
            print("!" + "*" * 48 + "!")
        ALREADY_PRINT_APP[self.APP_LABEL] = True
        return super().setUp()