import secrets

import requests

from MultiFeatures.IndianRailway.dataConfig import is_train_number_valid
from MultiFeatures.IndianRailway.errors import HTTPErr, InternetUnreachable, NotAValidTrainNumber


class Confirmtkt:
    """
    A class for interacting with the ConfirmTkt API to get information.

    Attributes:
        confirmtkt (str): The base URL for the ConfirmTkt API.
        headers (dict): The headers to be included in the API requests.
    """

    def __init__(self):
        """
        Initializes a new Confirmtkt instance.

        Args:
            api (str): The base URL for the ConfirmTkt API.
        """
        self.confirmtkt = "https://securedapi.confirmtkt.com/"
        self.headers = {
            'Host': 'securedapi.confirmtkt.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/4.9.2',
        }

    def generate_random_hex_string(self, length_: int = 32):
        """Generate a random hexadecimal string of the specified length."""
        if length_ % 2 != 0:
            raise ValueError("Length should be an even number for a valid hexadecimal string.")
        num_bytes = length_ // 2
        random_bytes = secrets.token_bytes(num_bytes)
        hex_string = secrets.token_hex(num_bytes)
        return hex_string

    def _fetch(self, route, params, timeout=60, notSecured=False):
        """
        Sends an HTTP GET request to the ConfirmTkt API.

        Args:
            route (str): The API route to be appended to the base URL.
            params (dict): The parameters to include in the request.
            timeout (int): The maximum time to wait for the request to complete.

        Raises:
            HTTPErr: If the response status code is not 200.

        Returns:
            dict: The JSON response from the API.
        """
        url = "https://api.confirmtkt.com/" if notSecured else self.confirmtkt
        headers = {
            'Host': 'api.confirmtkt.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/4.9.2',
        } if notSecured else self.headers
        resp = requests.get(url + route, params=params, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            raise HTTPErr(status_code=resp.status_code, error="Response status code is not 200, it is {}".format(
                resp.status_code))
        return resp.json()

    def live_train_status(self, train_no: str, doj: str, locale: str = "en"):
        """
        Gets the live status of a train from the ConfirmTkt API.

        Args:
            train_no (str): The train number.
            doj (str): The date of journey in the format 'dd-mm-yyyy'.
            locale (str, optional): The locale for the response. Defaults to 'en'.

        Raises:
            NotAValidTrainNumber: If the provided train number is not valid.
            InternetUnreachable: If there is an issue connecting to the internet.
            HTTPErr: If the response status code is not 200.

        Returns:
            dict: The JSON response containing live train status information.
        """
        if not is_train_number_valid(str(train_no)):
            raise NotAValidTrainNumber
        try:
            params = {
                "trainno": str(train_no),
                "doj": str(doj),
                "locale": str(locale),
                "session": self.generate_random_hex_string(),
            }
            resp = self._fetch("api/trains/livestatusall", params=params, notSecured=True)
            return resp
        except requests.exceptions.ConnectionError:
            raise InternetUnreachable

    def train_monthlyavailability(self, src: str, dest: str, train_no: str, doj: str, locale: str = "en",
                                  travelclasses: str = "1A,2A,3A,3E,SL", quota: str = "GN"):
        """
        Fetch monthly availability information for a specific train.

        Parameters:
        - src (str): Source station code.
        - dest (str): Destination station code.
        - train_no (str): Train number.
        - doj (str): Date of journey in the format 'dd-mm-yyyy'.
        - locale (str): Locale for the response. Default is "en".
        - travelclasses (str): Comma-separated list of travel classes. Default is "1A,2A,3A,3E,SL".
        - quota (str): Quota for the availability check. Default is "GN".

        Returns:
        - dict: Monthly availability information for the specified train.

        Raises:
        - InternetUnreachable: If a connection error occurs during the API request.
        - HTTPErr: If the response status code is not 200.

        """
        try:
            params = {
                "source": src,
                "destination": dest,
                "travelclasses": travelclasses,
                "quota": quota,
                'doj': doj,
                'locale': locale,
                'session': self.generate_random_hex_string(),
            }
            resp = self._fetch(f"api/trains/{train_no}/monthlyavailability", params=params)
            return resp
        except requests.exceptions.ConnectionError:
            raise InternetUnreachable

    def available_trains(self, src: str, dest: str, doj: str, travelclass: str = "ZZ", passengerTrains: bool = True,
                         showEcClass: bool = True, quota: str = "GN"):
        """
        Fetch available trains between two stations.

        Parameters:
        - src (str): Source station code.
        - dest (str): Destination station code.
        - doj (str): Date of journey in the format 'dd-mm-yyyy'.
        - travelclass (str): Travel class for the journey. Default is "ZZ".
        - passengerTrains (bool): Whether to include passenger trains in the results. Default is True.
        - showEcClass (bool): Whether to include EC class in the results. Default is True.
        - quota (str): Quota for the availability check. Default is "GN".

        Returns:
        - dict: Available trains between the specified stations.
        - None: If no trains are available (as Str).
        Raises:
        - InternetUnreachable: If a connection error occurs during the API request.
        - HTTPErr: If the response status code is not 200.
        Note:
        - This call may take a long time to complete.

        """
        try:
            params = {
                'source': src,
                'destination': dest,
                'doj': doj,
                'travelClass': travelclass,
                'quota': quota,
                'passengerTrains': passengerTrains,
                'showEcClass': True,
            }

            resp = self._fetch("api/trains/latest", params=params)
            return resp
        except requests.exceptions.ConnectionError:
            raise InternetUnreachable

    def is_irctc_user_id_valid(self, user_id: str):
        """
        Checks if the provided IRCTC user ID is valid.

        Args:
            user_id (str): The IRCTC user ID to check.

        Returns:
            bool: True if the user ID is valid, False otherwise.
        """

        params = {
            "userid": user_id,
        }
        resp = self._fetch("api/platform/irctcregistration/checkuserid", params=params)
        return False if resp.get('status') is None else True

    def reset_irctc_account_password(self, user_id, contact_info, is_email=False):
        """
        Reset the password of an IRCTC account. New password will be sent to the provided contact info.

        Args:
            user_id (str): The IRCTC user ID.
            contact_info (str): The phone number or email address associated with the IRCTC account.
            is_email (bool, optional): Whether the provided contact info is an email address. Defaults to False.

        Returns:
            dict: The JSON response from the API.

        Raises:
            InternetUnreachable: If a connection error occurs during the API request.
            HTTPErr: If the response status code is not 200.
        Note:
            Use this method only if you have permission to reset the password of the IRCTC account.
        """
        otptype = 'E' if is_email else 'M'
        params = {
            'userid': user_id,
            'otptype': otptype,
            'phonenumber' if not is_email else 'email': contact_info,
        }
        try:
            resp = self._fetch("api/platform/irctcregistration/changepassword", params=params)
            return resp
        except requests.exceptions.ConnectionError:
            raise InternetUnreachable
