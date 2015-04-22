from unittest import TestCase
from django.test import RequestFactory
import pytest
import django; django.setup()

from imago.views import BillList

import json


class BillSearchTests(TestCase):

    def setUp(self):
        self.results_count = 10
        self.factory = RequestFactory()

    @pytest.mark.django_db
    def test_bill_results_count(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        request.params = request.GET.copy()
        response = endpoint.get(request)
        resp_obj = json.loads(response.content.decode())
        results = resp_obj.get('results', None)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), self.results_count)
