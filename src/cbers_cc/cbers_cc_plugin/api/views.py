

from rest_flex_fields import FlexFieldsModelViewSet
from cbers_cc_plugin.api.serializers import (
    Tile512Serializer,
)
from cbers_cc_plugin.models import (
    Tile512,
)
from rest_framework.decorators import action
from cbers_cc_plugin.apps import CACHE_MODEL_PROCESSOR_KEY
from cbers_cc_plugin.resources.types import (
    Tile512GetSimilarRequest,
    Tile512GetSimilarResponse,
    Embedding,
)
from cbers_cc_plugin.resources.utils import (
    calculate_tile_embedding
)
from rest_framework.response import Response
from typing import List, Dict
from django.core.cache import cache
import numpy as np


class Tile512ViewSet(FlexFieldsModelViewSet):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    
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
        
        # Calculate embedding
        model_processor = cache.get(CACHE_MODEL_PROCESSOR_KEY)
        embedding: Embedding = calculate_tile_embedding(
            image=np.array(request_data['tile512']),
            model=model_processor['model'],
            processor=model_processor['processor'],
        )
        embedding_txt: str = str(embedding)
        
        # Find similar
        similar_tile = self.Model.objects.raw(f"""
            SELECT 
                res.id, 
                res.similarity,
                res.cdf
            FROM (
                SELECT
                    *,
                    (
                        SELECT SQRT(
                            SUM( (e.value::numeric - q.value::numeric)^2 )
                        )
                        FROM jsonb_array_elements_text(ccc512.embedding) WITH ORDINALITY AS e(value, i),
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