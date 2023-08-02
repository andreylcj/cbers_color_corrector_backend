

from typing import TypedDict, List


class EmbeddingJSON(TypedDict):
    embedding: List[float]


class CdfJSON(TypedDict):
    r: List[float]
    g: List[float]
    b: List[float]


Tile512GetSimilarRequest = EmbeddingJSON


class Tile512GetSimilarResponse(TypedDict):
    cdf: CdfJSON
    similarity: float