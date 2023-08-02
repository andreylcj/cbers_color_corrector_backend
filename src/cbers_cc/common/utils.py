

from datetime import datetime
from dateutil import parser, tz
from typing import List, Dict
import math
import numpy as np
import json
import codecs
import pickle


def iso_parser(date_str: str) -> datetime:
    """Iso Parser.
    """
    response = None
    error = False
    try:
        response = datetime.fromisoformat(date_str)
    except:
        error = True    
    if error:
        error = False
        try:
            response = parser.isoparse(date_str)
        except:
            error = True            
    if error:
        raise Exception(f"Invalid date: {date_str}")
    return response


def smart_tz_handle(date_str):
    """Parse date as string handling timezone.
    """
    try:
        date = parser.parse(date_str)
        if date.tzinfo is None:
            date = date.replace(tzinfo=tz.tzutc())
        # Retorna a representação em string da data com o fuso horário UTC
        return date.strftime('%Y-%m-%dT%H:%M:%S.%f %z')
    except Exception as e:
        # print(f"Erro ao processar a data: {e}")
        return None


class ValidateRequestDataIterator:
    def __init__(
        self,
        serializer, 
        data: List, 
        ignore_error_codes: List[str]=['unique']
    ) -> None:
        # self.serializer = serializer(data=data, many=True)
        self.serializer = serializer
        self.data = data
        self.ignore_error_codes = ignore_error_codes
        self._serializer_errors = []
        # self.data_is_valid = self.serializer.is_valid()
        self._iter_count = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        
        if self._iter_count == len(self.data):
            raise StopIteration
        
        row = self.data[self._iter_count]
        serializer = self.serializer(data=row, many=False)
        row_is_valid = serializer.is_valid()
        class Found(Exception): pass
            
        if not row_is_valid and serializer.errors != {}:
            try:
                row_is_valid = True
                for field, field_errors in serializer.errors.items():
                    for error in field_errors:
                        if error.code not in self.ignore_error_codes:
                            raise Found
            except Found:
                row_is_valid = False
                
        self._iter_count = self._iter_count + 1
        self._serializer_errors.append(serializer.errors)
        
        return row_is_valid, row

    @property
    def serializer_errors(self):
        return self._serializer_errors
    

def valid_data(
    serializer, 
    data: List, 
    ignore_error_codes: List[str]=['unique']
) -> List[bool]:
    serializer = serializer(data=data, many=True)
    data_is_valid = serializer.is_valid()
    valid_data = []
    # for idx, row in enumerate(serializer.data):
    for idx, row in enumerate(data):
        if not data_is_valid \
        and serializer.errors[idx] != {}:
            skip_row = False
            for field, field_errors in serializer.errors[idx].items():
                for error in field_errors:
                    if error.code not in ignore_error_codes:
                        skip_row = True
                        break
                if skip_row:
                    break
            if skip_row:
                valid_data.append(False)
                continue
        valid_data.append(True)
    return valid_data, serializer.errors


def is_data_full_valid(
    serializer, 
    data: List, 
    ignore_error_codes: List[str]=['unique']
) -> bool:
    
    serializer = serializer(data=data, many=True)
    data_is_valid = serializer.is_valid()
    
    if data_is_valid:
        return True
    
    class Found(Exception): pass
    
    try:
        for serializer_error in serializer.errors:
            for field, field_errors in serializer_error.items():
                for error in field_errors:
                    if error.code not in ignore_error_codes:
                        raise Found
    except:
        return False
    
    return True
    

DJANGO_MODEL_TYPE_TO_FEATURE_TYPE = {
        'BigAutoField': 'int',
        'DateTimeField': 'datetime',
        'DateField': 'datetime',
        'CharField': 'str',
        'IntegerField': 'int',
        'BigIntegerField': 'int',
        'FloatField': 'float',
        'JSONField': 'JSONB',
        'ForeignKey': 'int',
        'TextField': 'str',
    }


def phightlight(
    content, 
    size: int=40,
    lcontent: str="!***",
    lfill: str=" ",
    rcontent: str="***!",
    rfill: str=" ",
) -> str:
    l_len = len(lcontent)
    r_len = len(rcontent)
    content_len = len(content)
    content_space = size - l_len - r_len
    lspace = math.floor((content_space - content_len) / 2)
    rspace = content_space - content_len - lspace
    lfill = lfill * lspace
    rfill = rfill * rspace
    return f'{lcontent}{lfill}{content}{rfill}{rcontent}'


def get_unique_dict(
    list_of_dict,
    ignore_items: List=[{}]
) -> List[Dict]:
    """Get a List unique dictionaries
    List to contain unique dictionaries"""
    listOfUniqueDicts = []
    # A set object
    setOfValues = set()
    # iterate over all dictionaries in list
    for dictObj in list_of_dict:
        
        if dictObj in ignore_items:
            continue
        
        list_Of_tuples = []
        # For each dictionary, iterate over all key
        # and append that to a list as tuples
        for key, value in dictObj.items():
            list_Of_tuples.append( (key, value))
        strValue = ""
        # convert list of tuples to a string
        for key, value in sorted(list_Of_tuples):
            # sort list of tuples, and iterate over them
            # append each pair to string
            strValue += str(key) + "_" + str(value) + "_"
        # Add string to set if not already exist in set
        if strValue not in setOfValues:
            # If string is not in set, then it means
            # this dictionary is unique
            setOfValues.add(strValue)
            listOfUniqueDicts.append (dictObj)
    
    return listOfUniqueDicts


def split_list(
    arr: List,
    batch_size: int,
) -> List[List]:
    # arr_copy = deepcopy(arr)
    sub_lists = [
        arr[i:i+batch_size] 
        for i in range(0,len(arr),batch_size)
    ]
    return sub_lists


DJANGO_MODEL_TYPE_TO_NUMPY_TYPE = {
        'BigAutoField': lambda field: np.dtype('i8'),
        'DateTimeField': lambda field: np.dtype('M8[ns]'),
        'DateField': lambda field: np.dtype('M8[D]'),
        'CharField': lambda field: np.dtype(f'U{field.max_length}'),
        'IntegerField': lambda field: np.dtype('i8'),
        'BigIntegerField': lambda field: np.dtype('i8'),
        'FloatField': lambda field: np.dtype('float'),
        'JSONField': lambda field: np.dtype('O'),
        'ForeignKey': lambda field: np.dtype('i8'),
        'TextField': lambda field: np.dtype('O'),
    }
    
    
def handle_inf(value: float):
    is_inf = False
    try:
        is_inf = math.isinf(value)
    except:
        is_inf = False
    if is_inf:
        return str(value)
    return value


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False
    

def pickle_as_base64(obj) -> str:
    return codecs.encode(pickle.dumps(obj), "base64").decode()