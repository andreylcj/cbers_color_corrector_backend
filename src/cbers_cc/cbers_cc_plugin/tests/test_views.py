

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
import math
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
        data['embedding'] = [.5 for i in range(512)]
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
            qty=2,
        )
        for idx, item in enumerate(data):
            curr_val: float = -1 if idx == 0 else 1
            item['embedding'] = [curr_val for i in range(1, 512+1)]
            item['cdf'] = CdfJSON(
                r=[curr_val for i in range(1, 256+1)],
                g=[curr_val for i in range(1, 256+1)],
                b=[curr_val for i in range(1, 256+1)],
            )
            tile512 = Tile512(**item)
            tile512.save()
        
        
        # path: str = 'cbers_cc_plugin/tests/payload/tile_info.json'
        # with open(path, "r") as f:
        #     data = json.loads(f.read())
        # data = {
        #     'src_filename': "s01_pancromatica.tif",
        #     'src_pixel_xl': data['col_off'],
        #     'src_pixel_xr': data['col_off'] + data['width'],
        #     'src_pixel_yu': data['row_off'],
        #     'src_pixel_yd': data['row_off'] + data['height'],
        #     'embedding': data['embedding'],
        #     'cdf': data['extra']['correspondent_pretty_tile_cdf'],            
        # }
        # tile512 = Tile512(**data)
        # tile512.save()

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

    @log_details("Tile 512 Get Similar Diff Response For Diff Request")
    def tile512_diff_res_for_diff_req(self):
        path: str = 'cbers_cc_plugin/tests/payload/tile512.json'
        with open(path, "r") as f:
            data = json.loads(f.read())
            
        tile512_data = data['tile512']
        dummy_tile = []
        for i in range(len(tile512_data)):
            dummy_tile.append([])
            for j in range(len(tile512_data[i])):
                dummy_tile[-1].append([255, 255, 255])
        request_data: Tile512GetSimilarRequest = {
            'tile512': dummy_tile
        }
                        
        url = reverse('Tile512ViewSet-get_similar')
        res1 = test_method(
            url=url,
            method='post',
            api_test_case=self,
            token=self.token,
            data=request_data,
        )
        content = res1.content.decode("utf-8") 
        res1 = json.loads(content)
        
        res1['cdf'] = {
            "r": res1['cdf']['r'][:5] + res1['cdf']['r'][50:55] + res1['cdf']['r'][-5:],
            "g": res1['cdf']['g'][:5] + res1['cdf']['g'][50:55] + res1['cdf']['g'][-5:],
            "b": res1['cdf']['b'][:5] + res1['cdf']['b'][50:55] + res1['cdf']['b'][-5:],
        }
        # pprint(res1)
        
        tile512_data = data['tile512']
        dummy_tile = []
        for i in range(len(tile512_data)):
            dummy_tile.append([])
            for j in range(len(tile512_data[i])):
                dummy_tile[-1].append([0, 0, 0])
        request_data: Tile512GetSimilarRequest = {
            'tile512': dummy_tile
        }
        res2 = test_method(
            url=url,
            method='post',
            api_test_case=self,
            token=self.token,
            data=request_data,
        )
        content = res2.content.decode("utf-8") 
        res2 = json.loads(content)
        
        res2['cdf'] = {
            "r": res2['cdf']['r'][:5] + res2['cdf']['r'][50:55] + res2['cdf']['r'][-5:],
            "g": res2['cdf']['g'][:5] + res2['cdf']['g'][50:55] + res2['cdf']['g'][-5:],
            "b": res2['cdf']['b'][:5] + res2['cdf']['b'][50:55] + res2['cdf']['b'][-5:],
        }
        # pprint(res2)
        
        self.assertNotEqual(res1['id'], res2['id'])
        
    @log_details("Basic", omit_start=False)
    def test_base(self):
        self.TestCreateTile512()
        self.populate_tile_512()
        # self.tile512_get_similar()
        self.tile512_diff_res_for_diff_req()
        