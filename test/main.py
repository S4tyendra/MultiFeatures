import requests

url = "https://loco.redbus.com/api/Rails/v1/RIS/PnrToolkit"
headers = {
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
    "Content-Type": "application/json",
}
data = {"q": "2104360775"}

try:
    import time
    t1 = time.time()
    response = requests.post('https://google.com/search', headers=headers, json=data)
    print(time.time() - t1)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    print(response.json())  # Print the parsed JSON response

except requests.exceptions.RequestException as e:
    print("Error making request:", e)
