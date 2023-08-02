

from rest_flex_fields import FlexFieldsModelViewSet
from cbers_cc_plugin.api.serializers import (
    Tile512Serializer,
)
from cbers_cc_plugin.models import (
    Tile512,
)
from rest_framework.decorators import action
from cbers_cc_plugin.resources.types import (
    Tile512GetSimilarRequest,
    Tile512GetSimilarResponse,
)
from rest_framework.response import Response
from typing import List, Dict

import numpy as np


class Tile512ViewSet(FlexFieldsModelViewSet):
    serializer_class = Tile512Serializer
    queryset = Tile512.objects.all().order_by('id')
    Model = Tile512
    # filterset_class = EmbeddingFilters
    
    @action(
        detail=False, 
        methods=['POST'], 
        url_path=f'similar', 
        url_name='get_similar'
    )
    def get_similar(self, request, *args, **kwargs):
        request_data: Tile512GetSimilarRequest = request.data
        embedding: List[float] = request_data['embedding']
        embedding_txt: str = str(embedding)
        
        similar_tile = self.Model.objects.raw(f"""
            SELECT 
                res.id, 
                res.cdf,
                res.similarity
            FROM (
                SELECT
                    *,
                    (
                        SELECT SQRT(
                            SUM( (e.value::numeric - q.value::numeric)^2 )
                        )
                        FROM jsonb_array_elements_text(ccc512.embedding->'embedding') WITH ORDINALITY AS e(value, i),
                            jsonb_array_elements_text('{embedding_txt}'::jsonb) WITH ORDINALITY AS q(value, j)
                        WHERE e.i = q.j
                    ) as similarity
                FROM cbers_cc_plugin.tile_512 ccc512
            ) res
            ORDER BY similarity ASC
            LIMIT 1;
        """)
        
        response_kwargs: Dict = {}
        
        if similar_tile is not None:
            similar_tile = similar_tile[0]
            response_data = Tile512GetSimilarResponse(
                cdf=similar_tile.cdf,
                similarity=similar_tile.similarity,
            )
            
        else:
            response_data = {'error': 'No similar tile found.'}
            response_kwargs['status'] = 400
        
        return Response(response_data, **response_kwargs)