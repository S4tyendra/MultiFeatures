import base64
import cv2
import numpy as np
import pytesseract
import requests
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode


username = input("Enter the username: ")
password = input("Enter the password: ")
password = base64.b64encode(password.encode('utf-8'))
password = password.decode("utf-8")

timestamp = int(time.time() * 1000)
# print(timestamp)

r = requests.Session()
headers = {
    'Host': 'www.irctc.co.in',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Connection': 'keep-alive',
}

response = requests.get('https://www.irctc.co.in/eticketing/protected/profile/textToNumber/', headers=headers)

cookie_value = response.cookies.get('TS018d84e5')

cookies = {
    'TS018d84e5': f'{cookie_value}',
    'et_appVIP1': '',
    'JSESSIONID': '',
}

headers = {
    'Host': 'www.irctc.co.in',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Greq': '1',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.irctc.co.in/nget/train-search',
    'Connection': 'keep-alive',
}

params = {
    'nlpCaptchaException': 'true',
}

response = requests.get(
    'https://www.irctc.co.in/eticketing/protected/mapps1/loginCaptcha',
    params=params,
    cookies=cookies,
    headers=headers
)

# print(f"Captcha Questions: {response.json()['captchaQuestion']}")
# print( )
# print(f"Status: {response.json()['status']}")

def decode_image_from_base64(base64_string):
    image_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

response_json = response.json()
captcha_question = response_json['captchaQuestion']

decoded_image = decode_image_from_base64(captcha_question)
extracted_text = extract_text_from_image(decoded_image).replace("\n", "")
print(f"captcha code : {extracted_text}")
uid = response_json['status'].replace(" ", "")

leng = len(extracted_text)
Mumb = 16 - leng
most_imp = uid[0:Mumb].replace(" ", "")

final_key = f"{extracted_text}{most_imp}"

# print(f"Finalkey: {final_key}")

# print(len(final_key))

final_payload = f"{username}#UP#{password}#UP#{timestamp}"

# print(final_payload)

def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC, key)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

data_to_encrypt = final_payload
key = bytes(final_key, 'utf-8')
if len(key) != 16:
    raise ValueError("AES key must be 16 bytes long")
encrypted_data = aes_encrypt(data_to_encrypt, key)
payload_ready  = b64encode(encrypted_data).decode('utf-8')


import requests

cookies = {
    'TS018d84e5': f'{cookie_value}',
    'et_appVIP1': '',
    'JSESSIONID': '',
}

headers = {
    'Host': 'www.irctc.co.in',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
}

print(extracted_text)
data = f'grant_type=password&data={payload_ready}&captcha={extracted_text}&uid={uid}&otpLogin=false&lso=&encodedPwd=true'

response = requests.post('https://www.irctc.co.in/authprovider/webtoken', cookies=cookies, headers=headers, data=data)

print(response.json())
