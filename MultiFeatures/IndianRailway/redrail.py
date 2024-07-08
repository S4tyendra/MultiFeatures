import aiohttp
import asyncio
from MultiFeatures.IndianRailway.errors import HTTPErr


class RedRail:
    """
    A class for interacting with the RedRail API to get information.

    Attributes:
        base_url (str): The base URL for the RedRail API.
        headers (dict): The headers to be included in the API requests.
    """

    def __init__(self):
        """
        Initializes a new RedRail instance.
        """
        self.base_url = "https://loco.redbus.com"
        self.headers = {
            "Channel_name": "MOBILE_APP",
            "Os": "Android",
            "Accept": "application/json",
            "Appversion": "5.5.1",
            "Auth_key": "1",
            "Accept-Encoding": "gzip, deflate, br",
            "Appversioncode": "505010",
            "Language": "en",
            "Businessunit": "REDRAIL",
            "Currency": "INR",
            "Osversion": "",
            "Country": "India",
            "Country_name": "IND",
            "User-Agent": "okhttp/4.11.0",
        }

    async def _fetch(self, url, method="GET", params=None, data=None, timeout=60):
        """
        Sends an HTTP request to the RedRail API.

        Args:
            url (str): The API endpoint.
            method (str): The HTTP method ('GET' or 'POST').
            params (dict): The parameters to include in the request.
            data (dict): The JSON data to include in the request (for 'POST' method).
            timeout (int): The maximum time to wait for the request to complete.

        Returns:
            dict: The JSON response from the API.
        """
        url = self.base_url + url
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                if method == "GET":
                    async with session.get(url, params=params, timeout=timeout) as response:
                        print(response.url)
                        response.raise_for_status()
                        return await response.json()
                elif method == "POST":
                    async with session.post(url, json=data, timeout=timeout) as response:
                        print(response.url)
                        response.raise_for_status()
                        return await response.json()
                else:
                    raise ValueError("Invalid HTTP method")

        except aiohttp.ClientError as e:
            raise HTTPErr(error=str(e)) from e

    async def pnr_status(self, pnr: str, mobile: str = ""):
        """
        Gets the PNR status from the RedRail API.

        Args:
            pnr (str): The PNR number.
            mobile (str): The mobile number associated with the PNR (optional).

        Returns:
            dict: The JSON response containing PNR status information.
        """
        url = "/api/Rails/v1/RIS/PnrToolkit"
        data = {"pnr": pnr, "mobile": mobile}
        return await self._fetch(url, method="POST", data=data)

    async def train_schedule(self, train_no: str):
        """
        Gets the schedule for a train from the RedRail API.

        Args:
            train_no (str): The train number.

        Returns:
            dict: The JSON response containing train schedule information.
        """
        url = f"/api/Rails/v1/RIS/GetTrainSchedule/{train_no}"
        return await self._fetch(url)

    async def coach_position(self, train_no: str, stn: str):
        """
        Gets the coach position for a train at a station from the RedRail API.

        Args:
            train_no (str): The train number.
            stn (str): The station code.

        Returns:
            dict: The JSON response containing coach position information.
        """
        url = f"/api/Rails/v1/RIS/GetCoachPosition?trainNo={train_no}&stn={stn}"
        return await self._fetch(url)

    async def search_routes(self, src: str, dst: str, doj: str):
        """
        Searches for routes between two stations on a given date from the RedRail API.

        Args:
            src (str): The source station code.
            dst (str): The destination station code.
            doj (str): The date of journey in the format 'yyyymmdd'.

        Returns:
            dict: The JSON response containing route search results.
        """
        url = "/api/Rails/v1/Routes"
        data = {"dst": dst, "src": src, "sortLogic": 1, "doj": doj}
        return await self._fetch(url, method="POST", data=data)

    async def user_status(self, irctc_username: str):
        """
        Gets the user status from the RedRail API.

        Args:
            irctc_username (str): The IRCTC username.

        Returns:
            dict: The JSON response containing user status information.
        """
        url = f"/api/Rails/v1/UserStatus/{irctc_username}"
        return await self._fetch(url)

    async def get_live_train_status(self, train_no: str):
        """
        Gets the live status of a train from the RedRail API.

        Args:
            train_no (str): The train number.

        Returns:
            dict: The JSON response containing live train status information.
        """
        url = f"/api/Rails/v2/RIS/GetLiveTrainStatus/"
        params = {"trainNo": train_no}
        return await self._fetch(url, params=params)
