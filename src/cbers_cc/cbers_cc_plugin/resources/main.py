

from typing import TypedDict, List


class Cdf(TypedDict):
    r: List[float]
    g: List[float]
    b: List[float]
    

class RequestBodyData(TypedDict):
    cdf: Cdf
    embedding: List[float]
    
    
class EqFunc(TypedDict):
    r: List[int]
    g: List[int]
    b: List[int]


class ResponseBodyData(TypedDict):
    eqFunc: EqFunc

    
def match_tile(request_data: RequestBodyData) -> ResponseBodyData:
    pass