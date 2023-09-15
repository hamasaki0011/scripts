import requests
import pprint
import json

# url = 'http://127.0.0.1:8080/form.html'
# url = 'http://127.0.0.1:8080/upload.html'
url = 'http://10.10.210.87/upload'
session = requests.session()

res = session.get(url)
# print("res = ", res.text)
csrf = session.cookies['csrftoken']
print("csrf = ", csrf)

data = {
    # "next": url,
    "csrfmiddlewaretoken" : csrf,
}
files = {
    'file': open('testNew_17.csv', 'rb')
    }

headers = {
    "Referer": url,
    # "Content-Type": "multipart/form-data" ,
    }

# response = session.post(url, files = files, headers = headers)
response = session.post(url, data = data, files = files, headers = headers)
# r = requests.post(url, files=files, headers=headers)
print('post_r =', response.status_code)
print('post_headers =', response.headers)
# print('post_text =', response.text)
# pprint.pprint(response.json())
