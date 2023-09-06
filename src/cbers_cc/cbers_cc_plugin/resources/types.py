

from typing import TypedDict, List, Tuple


class EmbeddingJSON(TypedDict):
    embedding: List[float]


class CdfJSON(TypedDict):
    r: List[float]
    g: List[float]
    b: List[float]


Embedding = List[float]
PixelRGB = Tuple[int, int, int]
Image = List[List[PixelRGB]]

class Tile512GetSimilarRequest(TypedDict):
    tile512: Image


class Tile512GetSimilarResponse(TypedDict):
    cdf: CdfJSON
    similarity: float