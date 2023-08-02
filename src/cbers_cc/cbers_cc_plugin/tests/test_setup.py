

import json
from django.urls import reverse
from common.test_resources import (
    FakeDataGenerator, 
    TestSetUpPrintAppLabel
)
from django.contrib.auth.models import User
import logging
import os
import environ
env = environ.Env()
environ.Env.read_env()


logger = logging.getLogger('django')


class TestSetUp(TestSetUpPrintAppLabel):
    
    APP_LABEL = "CbersCCPlugin"

    def setUp(self):
        self.token_url = reverse('token_obtain_pair')
        self.fake_data_gen = FakeDataGenerator()
        username = 'testuser'
        password = '12345'
        self.user = User.objects.create_user(username=username, password=password)
        self.token = self.client.post(
            self.token_url,
            data={'username': username, 'password': password}
        )
        self.token = json.loads(self.token.content)['access']
        return super().setUp()

    def tearDown(self):
        return super().tearDown()