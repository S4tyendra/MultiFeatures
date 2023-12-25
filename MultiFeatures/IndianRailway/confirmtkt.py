import requests

from MultiFeatures.IndianRailway.dataConfig import isTrainNumberValid
from MultiFeatures.IndianRailway.errors import *


class Confirmtkt:
    def __init__(self, api: str = None):
        self.confirmtkt = api or "https://api.confirmtkt.com/"
        self.headers = {
            'Host': 'api.confirmtkt.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/4.9.2',
        }

    def _fetch(self, route, params, timeout=60):
        resp = requests.get(self.confirmtkt + route, params=params, headers=self.headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()

    def livestatusall(self, trainno: str, doj: str, locle: str = "en"):
        if not isTrainNumberValid(str(trainno)):
            raise NotAValidTrainNumber
        params = {
            "trainno": str(trainno),
            "doj": str(doj),
            "locle": str(locle)
        }
        resp = self._fetch("api/trains/livestatusall", params=params)
        return resp
