

from django.db import models
from common.abstract import SchemaModel


class Tile512(SchemaModel):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    src_filename = models.TextField(null=True, blank=True)
    src_pixel_xl = models.BigIntegerField(null=True)
    src_pixel_xr = models.BigIntegerField(null=True)
    src_pixel_yu = models.BigIntegerField(null=True)
    src_pixel_ud = models.BigIntegerField(null=True)
    embedding = models.JSONField(null=True) # cbers_cc_plugin.resources.types.EmbeddingJSON
    cdf = models.JSONField(null=True) # cbers_cc_plugin.resources.types.CdfJSON
    metadata = models.JSONField(null=True)
    
    class Meta:
        db_table = 'cbers_cc_plugin"."tile_512'