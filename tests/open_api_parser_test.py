import json

import pytest
from unittest.mock import Mock, patch

import requests

from fastapi_openapi_parser.OpenApiParser import OpenApiParser

from tests.fixtures.openapi_json_rinex_to_csv_fixture import openapi_json_rinex_to_csv_fixture
from tests.fixtures.parser_rinex_to_csv_fixture import parser_rinex_to_csv_fixture
from tests.services import rinex_to_csv

OPEN_API_PARSE_REQUEST_GET = "fastapi_openapi_parser.OpenApiParser.requests.get"

from tests.data.data import test_data


class TestOpenApiParser:

    @pytest.mark.parametrize("tags", [False, True])
    def test_parse_from_service(self, openapi_json_rinex_to_csv_fixture, tags):
        parser = OpenApiParser()

        client, openapi = next(openapi_json_rinex_to_csv_fixture(tags=tags))

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = openapi.encode()

        with patch(OPEN_API_PARSE_REQUEST_GET, return_value=mock_response):
            result = parser.parse_from_service('http://example.com')

            assert result == 200

            assert parser.get_raw_response_in_json() == json.loads(openapi)

            if tags:
                tags_open_api = getattr(parser, '_OpenApiParser__tags_open_api')
                assert tags_open_api != {}

    def test_parse_from_service_request_exception(self):
        with patch(OPEN_API_PARSE_REQUEST_GET) as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException

            parser = OpenApiParser()
            status_code = parser.parse_from_service('http://example.com')

            assert status_code == -1
            assert parser.get_raw_response_in_json() == {}

    def test_parse_from_service_json_decode_error(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"not a valid json"

        with patch("requests.get", return_value=mock_response):
            with pytest.raises(json.JSONDecodeError) as exc:
                json.loads(mock_response.content.decode("utf-8"), cls=json.JSONDecoder)

            parser = OpenApiParser()
            status_code = parser.parse_from_service('http://example.com')

            assert status_code == -2

    def test_get_paths(self, parser_rinex_to_csv_fixture):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture())

        paths = parser.get_paths()

        urls = [route.path for route in rinex_to_csv.app.routes]

        for path in paths:
            assert path in urls

    def test_get_path_method(self, parser_rinex_to_csv_fixture):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture())

        paths = parser.get_paths()

        for path in paths:
            route = rinex_to_csv.app.routes[4 + paths.index(path)]
            assert parser.get_path_method(path) == route.methods.pop().lower()

    def test_get_path_method(self, parser_rinex_to_csv_fixture):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture())

        paths = parser.get_paths()

        for path in paths:
            route = rinex_to_csv.app.routes[4 + paths.index(path)]
            assert parser.get_path_method(path) == route.methods.pop().lower()

    @pytest.mark.parametrize("path, expected", test_data)
    def test_check_api_gateway_tags(self, parser_rinex_to_csv_fixture, path, expected):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture(tags=True))

        assert parser.check_api_gateway_tags(path=path, tag_key="x-large-file-queues") == expected.get(
            "large_file_queues")

    @pytest.mark.parametrize("path, expected", test_data)
    def test_get_body_multipart_form_data(self, parser_rinex_to_csv_fixture, path, expected):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture(tags=True))

        assert parser.get_body_multipart_form_data(path=path, method=parser.get_path_method(path)) == expected.get(
            "get_body_multipart_form_data")

    @pytest.mark.parametrize("path, expected", test_data)
    def test_get_body_application_json(self, parser_rinex_to_csv_fixture, path, expected):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture(tags=True))

        assert parser.get_body_application_json(path=path, method=parser.get_path_method(path)) == expected.get(
            "get_body_application_json")

    @pytest.mark.parametrize("path, expected", test_data)
    def test_get_queries_param(self, parser_rinex_to_csv_fixture, path, expected):
        parser: OpenApiParser = next(parser_rinex_to_csv_fixture(tags=True))

        assert parser.get_queries_param(path=path, method=parser.get_path_method(path)) == expected.get(
            "get_queries_param")
