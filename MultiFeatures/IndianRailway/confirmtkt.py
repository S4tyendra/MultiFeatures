import secrets
import traceback
from typing import Optional

import aiohttp

from MultiFeatures.IndianRailway.dataConfig import is_train_number_valid
from MultiFeatures.IndianRailway.errors import HTTPErr, InternetUnreachable, NotAValidTrainNumber


class Confirmtkt:
    """
    A class for interacting with the ConfirmTkt API to get information.

    Attributes:
        _confirmtkt (str): The base URL for the ConfirmTkt API.
        _headers (dict): The headers to be included in the API requests.
    """

    def __init__(self):
        """
        Initializes a new Confirmtkt instance.

        Args:
            api (str): The base URL for the ConfirmTkt API.
        """
        self._config = None
        self._confirmtkt = "https://securedapi.confirmtkt.com/"
        self._headers = {
            'Host': 'securedapi.confirmtkt.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/4.9.2',
        }

    def _generate_random_hex_string(self, length_: int = 32):
        """Generate a random hexadecimal string of the specified length."""
        if length_ % 2 != 0:
            raise ValueError("Length should be an even number for a valid hexadecimal string.")
        num_bytes = length_ // 2
        random_bytes = secrets.token_bytes(num_bytes)
        hex_string = secrets.token_hex(num_bytes)
        return hex_string

    async def _fetch(self, route, params, timeout=60, notSecured=False, method='get', data=None):
        url = "https://api.confirmtkt.com/" if notSecured else self._confirmtkt
        headers = {
            'Host': 'api.confirmtkt.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/4.9.2',
        } if notSecured else self._headers

        async with aiohttp.ClientSession(headers=headers) as session:
            if method.lower() == 'get':
                async with session.get(url + route, params=params, timeout=timeout) as resp:
                    if resp.status != 200:
                        print(await resp.text())
                        print(resp.url)
                        print(f"Response status code is not 200, it is {resp.status} for the url: {url + route} and params: {params}")
                        raise HTTPErr(status_code=resp.status, error=f"Response status code is not 200, it is {resp.status}")
                    return await resp.json()
            elif method.lower() == 'post':
                async with session.post(url + route, params=params, json=data, timeout=timeout) as resp:
                    if resp.status != 200:
                        print(await resp.text())
                        print(resp.url)
                        print(f"Response status code is not 200, it is {resp.status} for the url: {url + route} and params: {params}")
                        raise HTTPErr(status_code=resp.status, error=f"Response status code is not 200, it is {resp.status}")
                    return await resp.json()

    async def live_train_status(self, train_no: str, doj: str, locale: str = "en"):
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
                "session": self._generate_random_hex_string(),
            }
            resp = await self._fetch("api/trains/livestatusall", params=params, notSecured=True)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable

    async def available_trains(self, src: str, dest: str, doj: str, quota: str = "GN"):

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
                'fromStnCode': src,
                'destStnCode': dest,
                'doj': doj,
                'quota': quota,
                'token': self._generate_random_hex_string(64),
                'androidid': '',
                'travelClassOrdering': 'ON,Ixigo',
                'appVersion': '397',
                'prevBookedTrains': 'OFF',
                'noChancePercentage': 'true',
                'getNearbyStation': 'true',
                'session': self._generate_random_hex_string(32)

            }

            resp = await self._fetch("api/platform/trainbooking/tatwnstns", params=params)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            traceback.print_exc()
            raise e

    async def is_irctc_user_id_valid(self, user_id: str):
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
        resp = await self._fetch("api/platform/irctcregistration/checkuserid", params=params)
        print(resp)
        return False if resp.get('status') is None else True

    async def reset_irctc_account_password(self, user_id, contact_info, is_email=False):
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
            resp = await self._fetch("api/platform/irctcregistration/changepassword", params=params)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e

    async def pnr_info(self, pnr: int):
        """
        Gets the PNR status from the ConfirmTkt API.

        Args:
            pnr (int): The PNR number.

        Returns:
            dict: The JSON response containing PNR status information.
        """
        if not isinstance(pnr, int):
            raise ValueError("PNR number should be an integer.")
        if len(str(pnr)) != 10:
            raise ValueError("PNR number should be a 10-digit number.")
        params = {
            "session": self._generate_random_hex_string(),
        }
        try:
            resp = await self._fetch(f"api/pnr/status/{pnr}", params=params, notSecured=True)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e

    async def train_search(self, train: str):
        """
        Search for a train by its number.

        Args:
            train (str): The train number.

        Returns:
            dict: The JSON response containing train information.
        """
        try:
            params = {
                "text": str(train),
                "session": self._generate_random_hex_string(),
            }
            resp = await self._fetch("/api/trains/search", params=params, notSecured=True)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e
    async def train_schedule(self, train_no: int, date: str, locale: str = "en"):
        """
        Gets the schedule of a train from the ConfirmTkt API.

        Args:
            train_no (int): The train number.
            date (str): The date for which the schedule is required.
            locale (str, optional): The locale for the response. Defaults to 'en'.

        Returns:
            dict: The JSON response containing train schedule information.
        """
        if not isinstance(train_no, int):
            raise ValueError("Train number should be an integer.")
        if not is_train_number_valid(str(train_no)):
            raise NotAValidTrainNumber
        try:
            params = {
                "trainNo": str(train_no),
                "date": date,
                "locale": locale,
                "session": self._generate_random_hex_string(),
            }
            resp = await self._fetch("api/trains/schedulewithintermediatestn", params=params, notSecured=True)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e

    async def get_stations_list(self):
        """
        Get the list of stations from the ConfirmTkt API.

        Returns:
            dict: The JSON response containing the list of stations.
        """
        try:
            params = {
                "locale": "en",
                "isCityMajorStationList": "true",
                "session": self._generate_random_hex_string(),
            }
            resp = await self._fetch("api/platform/getStationList", params=params)
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e

    async def send_otp(self, phone_number: str):
        """
        Send OTP to the provided phone number.

        Args:
            phone_number (str): The phone number without +91 to which the OTP will be sent.
        """
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Invalid phone number")
        try:
            params = {
                "mobileNumber": phone_number,
                "newOtp": "true",
                "retry": "false",
                "hashOtp": "true",
                "fireBaseSMSvendor": "karix",
                "locale": "en",
                "channel": "Android",
                "appVersion": "397"
            }
            resp = await self._fetch("api/platform/registerOutput", params=params)
            if resp.get("Error"):
                raise Exception(f"Error sending OTP: {resp['Error']}")
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e

    async def verify_otp(self, phone_number: str, otp: str):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Invalid phone number")
        try:
            params = {
                "mobileNumber": phone_number,
                "otp": otp,
                "locale": "en",
                "channel": "Android",
                "appVersion": "397"
            }
            resp = await self._fetch("api/platform/authenticatenew", params=params)
            if not resp.get("authToken"):
                raise Exception("Invalid OTP or authentication failed")
            self._config['auth_token'] = resp['authToken']
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e

    async def smart_switch(self, from_station: str, to_station: str, date: str, train_type: Optional[str] = None,
                           preferred_class: Optional[str] = None, token: Optional[str] = None):
        try:
            params = {"session": self._generate_random_hex_string()}
            data = {
                "AppVersion": "397",
                "DestStnCode": to_station,
                "Doj": date,
                "FromStnCode": from_station,
                "PlanFcfMax": "RO-F3FMAX",
                "PlanZeroCan": "RO-F3",
                "PreferredClass": preferred_class or "",
                "Quota": "GN",
                "Token": token or self._config.get('auth_token'),
                "TrainType": train_type or "",
            }
            resp = await self._fetch("api/platform/trainbooking/smartswitch", params=params, method='post', data=data)
            if resp.get("error"):
                raise Exception(f"Smart switch error: {resp['error']}")
            return resp
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            raise e
