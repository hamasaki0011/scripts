import sys
import requests
# import pprint
# import json

file_name = '../upload_file/' + sys.argv[1] + '.csv'
print("ファイル名 = ", file_name)

url = 'http://10.10.210.87/upload/'

session = requests.session()

# To get cookie
res = session.get(url)
csrf = session.cookies['csrftoken']
print("csrf = ", csrf)

data = {
    # "next": url,
    "csrfmiddlewaretoken" : csrf,
}
files = {
    'file': open(file_name, 'rb')
    }

headers = {
    "Referer": url,
    # 注意：以下を指定すると誤動作する
    # "Content-Type": "multipart/form-data" ,
}

response = session.post(url, data = data, files = files, headers = headers)

print('post_r =', response.status_code)

# 2023.9.15 ファイル保存 
with open("work/response_text.txt", "ab") as f:
    f.write(response.text.encode())
