import datetime
import unittest
import urllib.parse

import requests

from main import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/events")

    def test_retrieve_correct_dates(self):
        create_response = requests.put(
            self.app_path, json={"date": "2022-03-22", "event": "Drugi dzień wiosny"}
        )
        self.assertEqual(create_response.status_code, 200)

        retrieve_response = requests.get(self.app_path + "/2022-03-22")

        self.assertEqual(retrieve_response.status_code, 200)
        response_json = retrieve_response.json()
        test_event = None
        for event in response_json:
            if event["name"] == "Drugi dzień wiosny":
                test_event = event

        self.assertIsNotNone(test_event)
        self.assertIsInstance(test_event["id"], int)
        self.assertEqual(test_event["date"], "2022-03-22")
        date_added = datetime.date.fromisoformat(test_event["date_added"])
        self.assertGreaterEqual(
            date_added, datetime.date.today() - datetime.timedelta(days=1)
        )
        self.assertLessEqual(
            date_added, datetime.date.today() + datetime.timedelta(days=1)
        )


if __name__ == "__main__":
    unittest.main()
