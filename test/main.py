import unittest
from unittest import mock
from unittest.mock import patch
from MultiFeatures.IndianRailway.confirmtkt import Confirmtkt, HTTPErr, InternetUnreachable, NotAValidTrainNumber
import requests

class TestConfirmtkt(unittest.TestCase):
    def setUp(self):
        self.confirmtkt = Confirmtkt()

    @patch('requests.get')
    def test_live_train_status(self, mock_get):
        # Mocking the requests.get function
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'success'}

        train_no = '12345'
        doj = '28-12-2023'

        # Testing the live_train_status method
        result = self.confirmtkt.live_train_status(train_no, doj)
        self.assertEqual(result, {'status': 'success'})

    @patch('requests.get')
    def test_train_monthlyavailability(self, mock_get):
        # Mocking the requests.get function
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'success'}

        src = 'SRC'
        dest = 'DEST'
        train_no = '12345'
        doj = '01-01-2023'

        # Testing the train_monthlyavailability method
        result = self.confirmtkt.train_monthlyavailability(src, dest, train_no, doj)
        self.assertEqual(result, {'status': 'success'})

    @patch('requests.get')
    def test_available_trains(self, mock_get):
        # Mocking the requests.get function
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'success'}

        src = 'SRC'
        dest = 'DEST'
        doj = '01-01-2023'

        # Testing the available_trains method
        result = self.confirmtkt.available_trains(src, dest, doj)
        self.assertEqual(result, {'status': 'success'})

    @patch('requests.get')
    def test_is_irctc_user_id_valid(self, mock_get):
        # Mocking the requests.get function
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'success'}

        user_id = 'idk'

        # Testing the is_irctc_user_id_valid method
        result = self.confirmtkt.is_irctc_user_id_valid(user_id)
        self.assertTrue(result)

    @patch('requests.get', side_effect=requests.exceptions.ConnectionError)
    def test_internet_unreachable_exception(self, mock_get):
        # Mocking the requests.get function to simulate ConnectionError
        with self.assertRaises(InternetUnreachable):
            self.confirmtkt.live_train_status('12345', '01-01-2023')

    @patch('requests.get', return_value=mock.Mock(status_code=404))
    def test_http_err_exception(self, mock_get):
        # Mocking the requests.get function to simulate HTTP error (404)
        with self.assertRaises(HTTPErr):
            self.confirmtkt.train_monthlyavailability('SRC', 'DEST', '12345', '01-01-2023')

    def test_not_a_valid_train_number_exception(self):
        # Testing the NotAValidTrainNumber exception
        with self.assertRaises(NotAValidTrainNumber):
            self.confirmtkt.live_train_status('sswe3', '28-12-2023')


if __name__ == '__main__':
    unittest.main()
