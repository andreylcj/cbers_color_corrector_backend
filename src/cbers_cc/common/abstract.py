

from django.db import models
import logging
import json


logger = logging.getLogger('django')


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


class SchemaModel(models.Model):
    
    @classmethod
    def list_column_names(cls):
        return [
            item.get('other_name', None) or item['name']
            for item in cls.get_schema()
        ]
    
    @classmethod
    def get_schema(cls):
        fields = []
        for f in cls._meta.fields:
            name = f.attname
            other_name = None
            _type = f.__class__.__name__
            if _type == 'ForeignKey' and name.endswith("_id"):
                other_name = name[:-3]
            fields.append({
                'name': name, 
                'type': _type, 
                "other_name": other_name, 
                "is_pk": getattr(f, 'primary_key', False),
                # "details": {
                #     k: v
                #     for k, v in f.__dict__.items()
                #     if is_jsonable(v)
                # },
                "unique_fields": cls.get_unique_fields(),
            })
        return fields
    
    @classmethod
    def get_unique_fields(cls, pk_as_unique: bool=False):
        unique_fields = []
        for field in cls._meta.fields:
            is_unique = getattr(field, '_unique', False)
            if is_unique:
                unique_fields.append(field.attname)
        for constraint in cls._meta.constraints:
            is_unique_constraint = constraint.__class__.__name__ == 'UniqueConstraint'
            if is_unique_constraint:
                for field_name in getattr(constraint, 'fields', []):
                    if field_name not in unique_fields:
                        unique_fields.append(field_name)
        # unique_fields = list(set(unique_fields))
        if unique_fields == [] \
        and pk_as_unique:
            for field in cls._meta.fields:
                is_pk = getattr(field, 'primary_key', False)
                if is_pk:
                    unique_fields.append(field.attname)
        return unique_fields
    
    class Meta:
        abstract = True