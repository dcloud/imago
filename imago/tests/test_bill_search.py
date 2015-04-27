from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
import pytest
import django; django.setup()

from imago.views import BillList


class BillSearchTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()

    @pytest.mark.django_db
    def test_bills_http200(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        response = endpoint.get(request)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")

    @pytest.mark.django_db
    def test_bills_deserialize(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn("results", content, "Content dictionary should contain a results object")
        self.assertIn("meta", content, "Content dictionary should contain a meta object")
