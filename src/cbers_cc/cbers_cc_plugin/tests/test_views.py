

import json
import time
from .test_setup import TestSetUp
from common.decorators import log_details
from ..models import (
    Tile512
)
from pprint import pprint
import os
from common.test_resources import (
    test_method,
    FieldCustomGenerate
)
from cbers_cc_plugin.resources.types import (
    EmbeddingJSON,
    CdfJSON,
    Tile512GetSimilarRequest
)
from typing import List
import numpy as np
import logging
import environ
from django.urls import reverse
env = environ.Env()
environ.Env.read_env()


logger = logging.getLogger('django')


class TestViews(TestSetUp):
    
    @log_details("Create Tile 512")
    def TestCreateTile512(self):
        data = self.fake_data_gen.generate(
            model=Tile512,
            assert_filled=[
                'src_filename',
                'src_pixel_xl',
                'src_pixel_xr',
                'src_pixel_yu',
                'src_pixel_ud',
            ]
        )[0]
        data['embedding'] = EmbeddingJSON(
            embedding=[.5 for i in range(512)]
        )
        data['cdf'] = CdfJSON(
            r=[.5 for i in range(256)],
            g=[.5 for i in range(256)],
            b=[.5 for i in range(256)],
        )
        url = reverse('Tile512ViewSet-list')
        res = test_method(
            url=url,
            method='post',
            api_test_case=self,
            token=self.token,
            data=data,
        )
        content = res.content.decode("utf-8") 
        res = json.loads(content)
        self.assertGreater(res['id'], 0)
        self.assertJSONEqual(
            json.dumps(res['embedding'], sort_keys=True),
            json.dumps(data['embedding'], sort_keys=True)
        )
        self.assertJSONEqual(
            json.dumps(res['cdf'], sort_keys=True), 
            json.dumps(data['cdf'], sort_keys=True)
        )
    
    @log_details("Populate Tile 512")
    def populate_tile_512(self):
        data = self.fake_data_gen.generate(
            model=Tile512,
            assert_filled=[
                'src_filename',
                'src_pixel_xl',
                'src_pixel_xr',
                'src_pixel_yu',
                'src_pixel_ud',
            ],
            qty=3,
        )
        for idx, item in enumerate(data):
            curr_val: float = .2 if idx == 0 else .4 if idx == 1 else .6 
            item['embedding'] = EmbeddingJSON(
                embedding=[curr_val for i in range(1, 512+1)]
            )
            item['cdf'] = CdfJSON(
                r=[curr_val for i in range(1, 256+1)],
                g=[curr_val for i in range(1, 256+1)],
                b=[curr_val for i in range(1, 256+1)],
            )
            tile512 = Tile512(**item)
            tile512.save()
        
        
        path: str = 'cbers_cc_plugin/tests/payload/tile_info.json'
        with open(path, "r") as f:
            data = json.loads(f.read())
        data = {
            'src_filename': "s01_pancromatica.tif",
            'src_pixel_xl': data['col_off'],
            'src_pixel_xr': data['col_off'] + data['width'],
            'src_pixel_yu': data['row_off'],
            'src_pixel_yd': data['row_off'] + data['height'],
            'embedding': data['embedding'],
            'cdf': data['extra']['correspondent_pretty_tile_cdf'],            
        }
        tile512 = Tile512(**data)
        tile512.save()

    @log_details("Tile 512 Get Similar")
    def tile512_get_similar(self):
        path: str = 'cbers_cc_plugin/tests/payload/tile512.json'
        with open(path, "r") as f:
            data = json.loads(f.read())
        request_data: Tile512GetSimilarRequest = {
            'tile512': data['tile512']
        }
        
        url = reverse('Tile512ViewSet-get_similar')
        res = test_method(
            url=url,
            method='post',
            api_test_case=self,
            token=self.token,
            data=request_data,
        )
        content = res.content.decode("utf-8") 
        res = json.loads(content)
        
        path: str = 'cbers_cc_plugin/tests/payload/tile_info.json'
        with open(path, "r") as f:
            data = json.loads(f.read())
        expected_similarity: float = 0
        expected_cdf = data['extra']['correspondent_pretty_tile_cdf']
        
        self.assertLessEqual(abs(expected_similarity - res['similarity']), 1e-3)
        self.assertTrue('cdf' in res)
        self.assertEqual(
            json.dumps(res['cdf'], sort_keys=True),
            json.dumps(expected_cdf, sort_keys=True),
        )

    @log_details("Basic", omit_start=False)
    def test_base(self):
        self.TestCreateTile512()
        self.populate_tile_512()
        self.tile512_get_similar()
        