import unittest
import urllib.parse

import requests

from main import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/method")

    def test_get(self):
        get_response = requests.get(self.app_path)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.json(),
            {"method": "GET"},
        )

    def test_post(self):
        post_response = requests.post(self.app_path)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(
            post_response.json(),
            {"method": "POST"},
        )

    def test_put(self):
        put_response = requests.put(self.app_path)
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.json(),
            {"method": "PUT"},
        )

    def test_options(self):
        options_response = requests.options(self.app_path)
        self.assertEqual(options_response.status_code, 200)
        self.assertEqual(
            options_response.json(),
            {"method": "OPTIONS"},
        )

    def test_delete(self):
        delete_response = requests.delete(self.app_path)
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            delete_response.json(),
            {"method": "DELETE"},
        )


if __name__ == "__main__":
    unittest.main()
