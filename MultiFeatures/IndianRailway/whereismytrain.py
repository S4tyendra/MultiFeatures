import secrets
import traceback
from typing import Optional
import aiohttp
from uuid import uuid4
from datetime import datetime

from MultiFeatures.IndianRailway.dataConfig import is_train_number_valid
from MultiFeatures.IndianRailway.errors import HTTPErr, InternetUnreachable, NotAValidTrainNumber

class WhereIsMyTrain:
    """
    A class for interacting with the WhereIsMyTrain API to get train information.

    Attributes:
        _base_url (str): The base URL for the WhereIsMyTrain API.
        _headers (dict): The headers to be included in the API requests.
        _app_version (str): The version of the app to be used in requests.
    """

    def __init__(self):
        """
        Initializes a new WhereIsMyTrain instance.
        """
        self._base_url = "https://whereismytrain.in/"
        self._headers = {
            'Host': 'whereismytrain.in',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; unknown Build/OPM6.171019.030.E1)',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self._app_version = "7.1.5.633808517"

    def _generate_random_hex_string(self, length_: int = 32):
        """Generate a random hexadecimal string of the specified length."""
        if length_ % 2 != 0:
            raise ValueError("Length should be an even number for a valid hexadecimal string.")
        num_bytes = length_ // 2
        random_bytes = secrets.token_bytes(num_bytes)
        hex_string = secrets.token_hex(num_bytes)
        return hex_string

    async def _fetch(self, route, params, timeout=60):
        """
        Fetches data from the WhereIsMyTrain API.

        Args:
            route (str): The API route to fetch data from.
            params (dict): The query parameters for the request.
            timeout (int): The timeout for the request in seconds. Defaults to 60.

        Returns:
            dict: The JSON response from the API.

        Raises:
            InternetUnreachable: If there's an issue connecting to the internet.
            HTTPErr: If the response status code is not 200.
        """
        url = self._base_url + route
        try:
            async with aiohttp.ClientSession(headers=self._headers) as session:
                async with session.get(url, params=params, timeout=timeout) as resp:
                    if resp.status != 200:
                        print(await resp.text())
                        print(resp.url)
                        print(f"Response status code is not 200, it is {resp.status} for the url: {url} and params: {params}")
                        raise HTTPErr(status_code=resp.status, error=f"Response status code is not 200, it is {resp.status}")
                    return await resp.json()
        except aiohttp.ClientError:
            raise InternetUnreachable
        except Exception as e:
            traceback.print_exc()
            raise e

    async def sync_train_schedule(self, last_synced: int = 0, dev_mode: bool = False, data_version: str = "7.2.4", network_type: str = "WIFI", lang: str = "en"):
        """
        Syncs the train schedule with the server.

        Args:
            last_synced (int): The timestamp of the last sync. Defaults to 0.
            dev_mode (bool): Whether to use dev mode. Defaults to False.
            data_version (str): The version of the data. Defaults to "7.2.4".
            network_type (str): The type of network connection. Defaults to "WIFI".
            lang (str): The language for the response. Defaults to "en".

        Returns:
            dict: The JSON response containing the synced train schedule.
        """
        current_timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        params = {
            "lastSynced": last_synced,
            "dev_mode": str(dev_mode).lower(),
            "dataVersion": data_version,
            "appVersion": self._app_version,
            "networkType": network_type,
            "lang": lang,
            "user": self._generate_random_hex_string(32),
            "ts": current_timestamp
        }
        return await self._fetch("general/sync_train_schedule", params)

    async def live_status(self, train_no: str, date: str, from_station: str, to_station: str, from_day: int = 1, lang: str = "en"):
        """
        Gets the live status of a train.

        Args:
            train_no (str): The train number.
            date (str): The date of journey in the format 'dd-mm-yyyy'.
            from_station (str): The source station code.
            to_station (str): The destination station code.
            from_day (int): The day of journey. Defaults to 1.
            lang (str): The language for the response. Defaults to "en".

        Returns:
            dict: The JSON response containing live train status information.

        Raises:
            NotAValidTrainNumber: If the provided train number is not valid.
        """
        if not is_train_number_valid(str(train_no)):
            raise NotAValidTrainNumber
        
        params = {
            "date": date,
            "appVersion": self._app_version,
            "from_day": from_day,
            "train_no": train_no,
            "from": from_station,
            "to": to_station,
            "lang": lang,
            "user": self._generate_random_hex_string(32),
            "sb_version": "0",
            "qid": str(uuid4()).replace("-", "")
        }
        return await self._fetch("cache/live_status", params)

    async def live_station(self, station_code: str, hrs: int = 8, lang: str = "en"):
        """
        Gets the live status of trains at a particular station.

        Args:
            station_code (str): The station code.
            hrs (int): The number of hours to look ahead for train arrivals. Defaults to 8.
            lang (str): The language for the response. Defaults to "en".

        Returns:
            dict: The JSON response containing live station information.
        """
        params = {
            "appVersion": self._app_version,
            "hrs": hrs,
            "station_code": station_code,
            "lang": lang,
            "user": self._generate_random_hex_string(32),
            "sb_version": "0",
            "qid": str(uuid4()).replace("-", "")
        }
        return await self._fetch("cache/live_station", params)
