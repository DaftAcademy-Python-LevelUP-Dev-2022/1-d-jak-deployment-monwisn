import datetime
import unittest
import urllib.parse

import requests

from main import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/events")

    def test_retrieve_incorrect(self):

        retrieve_response = requests.get(self.app_path + "/2022-13-22")

        self.assertEqual(retrieve_response.status_code, 400)

    def test_retrieve_404(self):
        # At least one of those should be 404, unless we are really unlucky
        try_dates = ["/1994-12-29", "/1995-11-28", "/2054-01-05", "/2021-02-04"]
        response_404 = None
        for date in try_dates:
            retrieve_response = requests.get(self.app_path + date)
            if retrieve_response.status_code == 404:
                response_404 = retrieve_response

        self.assertEqual(response_404.status_code, 404)


if __name__ == "__main__":
    unittest.main()
