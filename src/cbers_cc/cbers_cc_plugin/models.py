

from django.db import models
from common.abstract import SchemaModel


class Embedding(SchemaModel):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ...
    metadata = models.JSONField(null=True)
    
    class Meta:
        db_table = 'cbers_cc_plugin"."embedding'
    
    
class ReferenceImage(SchemaModel):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    embbeding = models.ForeignKey(
        Embedding, 
        null=True, 
        on_delete=models.SET_NULL, 
    )
    cdf = models.JSONField(null=True)
    metadata = models.JSONField(null=True)
    
    class Meta:
        db_table = 'cbers_cc_plugin"."reference_image'