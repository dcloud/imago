from unittest import TestCase
from imago.tests.helpers import ApiRequestFactory, decode_json_or_none
from restless.http import HttpError
import pytest
import django; django.setup()

from imago.views import BillList


@pytest.mark.django_db
class BillSearchTests(TestCase):

    def setUp(self):
        self.factory = ApiRequestFactory()

    def test_bills_http200(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        response = endpoint.get(request)
        self.assertEqual(response.status_code, 200,
                         msg="Endpoint should return a 200 response when no URL params provided")

    def test_bills_defaults(self):
        endpoint = BillList()
        request = self.factory.get('/bills/')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn("meta", content, "Content dictionary should contain a meta object")
        self.assertIn("results", content, "Content dictionary should contain a results object")
        if 'results' in content:
            results = content.get('results')
            self.assertIsInstance(results, list, "JSON results should be a list")
            expected_fields = ('id', 'identifier', 'title', 'classification', 'subject')
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Bill dict should have key '{}'".format(field))

    def test_bills_custom_fields(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?fields=title,legislative_session,from_organization_id,classification')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")
        self.assertIn("meta", content, "Content dictionary should contain a meta object")
        self.assertIn("results", content, "Content dictionary should contain a results object")
        if 'results' in content:
            results = content.get('results')
            self.assertIsInstance(results, list, "JSON results should be a list")
            expected_fields = ('title', 'legislative_session', 'from_organization_id', 'classification')
            expected_field_str = ", ".join(expected_fields)
            for item in results:
                for field in expected_fields:
                    self.assertIn(field, item, "Bill dict should have key '{}'".format(field))
                for r_field in item.keys():
                    self.assertIn(r_field, expected_fields, "Bill dict should only have keys '{}'".format(expected_field_str))

    def test_bills_search(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?q=Wisconsin')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")

    def test_bills_sponsorships(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?sponsorships__person__id=ocd-person/8f8aacb2-0ff7-41b9-9c69-91db22cfa818')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")

    def test_bills_from_organization(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?from_organization_id=ocd-organization/98004f81-af38-4600-82a9-d1f23200be0b')
        response = endpoint.get(request)
        content = decode_json_or_none(response.content)
        if not content:
            self.fail("Unable to decode JSON from response.content")

        self.assertIsInstance(content, dict, "Content should be a JSON dictionary")

    def test_invalid_parameter(self):
        endpoint = BillList()
        request = self.factory.get('/bills/?sponsorships__organization__post_label__contains=foo')
        with self.assertRaises(HttpError):
            response = endpoint.get(request)
            content = decode_json_or_none(response.content)
            if not content:
                self.fail("Unable to decode JSON from response.content")

            self.assertEqual(response.status_code, 400,
                             msg="Endpoint should return a 400 response when an invalid URL param provided")
            self.assertIn('error', content, "Expect error in response JSON")

