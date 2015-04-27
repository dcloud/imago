from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
import pytest
import django; django.setup()

from imago.views import BillList


class BillSearchTests(TestCase):

    def setUp(self):
        self.results_count = 10
        self.factory = ApiRequestFactory()

    @pytest.mark.django_db
    def test_bill_results_count(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        results = content.get('results', None)

        self.assertIsNotNone(results)
        self.assertEqual(len(results), self.results_count)
