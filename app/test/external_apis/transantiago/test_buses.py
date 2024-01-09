import unittest
from unittest.mock import patch, MagicMock
from app.helpers.transantiago import TransantiagoAPI

class TestTransantiagoAPI(unittest.TestCase):

    @patch("requests.get")
    def test_set_token(self, mock_requests_get):
        transantiago_api = TransantiagoAPI()
        base64_mock = "c2VjcmV0"
        mock_requests_get.side_effect = [
            MagicMock(text='["123","456"]'),
            MagicMock(text=f"$jwt = '{base64_mock}==';"),
        ]
        transantiago_api.set_token()
        self.assertEqual(transantiago_api.get_token(), "secret")

    @patch("requests.get")
    def test_get_stop_buses(self, mock_requests_get):
        transantiago_api = TransantiagoAPI()
        mock_requests_get.return_value.text = '["bus1", "bus2"]'
        result = transantiago_api.get_stop_buses("123")
        self.assertEqual(result, ["bus1", "bus2"])

    @patch("requests.get")
    def test_get_stops(self, mock_requests_get):
        transantiago_api = TransantiagoAPI()
        mock_requests_get.return_value.text = '["stop1", "stop2"]'
        result = transantiago_api.get_stops()
        self.assertEqual(result, ["stop1", "stop2"])

    @patch("requests.get")
    def test_get_bus_route(self, mock_requests_get):
        transantiago_api = TransantiagoAPI()
        mock_requests_get.return_value.text = '{"route": "bus_route"}'
        result = transantiago_api.get_bus_route("456")
        self.assertEqual(result, {"route": "bus_route"})

    @patch("requests.get")
    def test_get_all_buses(self, mock_requests_get):
        transantiago_api = TransantiagoAPI()
        mock_requests_get.return_value.text = '["bus1", "bus2"]'
        result = transantiago_api.get_all_buses()
        self.assertEqual(result, ["bus1", "bus2"])

if __name__ == '__main__':
    unittest.main()
