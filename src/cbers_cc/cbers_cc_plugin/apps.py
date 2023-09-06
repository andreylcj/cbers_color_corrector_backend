

from django.apps import AppConfig
from transformers import CLIPProcessor, FlaxCLIPModel
from django.core.cache import cache
from django.db.models.signals import post_migrate


CACHE_MODEL_PROCESSOR_KEY: str = 'model_processor_dict'


def cache_model(sender, **kwargs):    
    print(f"Cache model...")    
    model_path: str = "flax-community/clip-rsicd-v2"
    model = FlaxCLIPModel.from_pretrained(model_path)
    processor = CLIPProcessor.from_pretrained(model_path)
    cache.set(
        CACHE_MODEL_PROCESSOR_KEY, 
        {'model': model, 'processor': processor,}, 
        None
    )        
    print(f"Caching model... Done!")


class CbersCcPluginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cbers_cc_plugin'
    
    def ready(self):
        #####################################
        # Cache Machine Learning Models
        #####################################
        already_cached = False
        try:
            cache_model(None)
            already_cached = True
        except Exception as exc:
            already_cached = False
            
        if not already_cached:
            post_migrate.connect(cache_model, sender=self)
