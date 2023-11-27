import sys
import requests
import datetime
import time
import threading
# import pprint
# import json

# This is the target url
URL = 'http://10.10.210.87/upload/'

def countdown_timer(seconds):
    print('Timer start!')
    for i in range(seconds, 0, -1):
        print(f'[{i}]')
        time.sleep(1)
    print('Time up!')

def upload_data(url, file_name):
    # To get cookie
    session = requests.session()
    res = session.get(url)
    csrf = session.cookies['csrftoken']
    print(f"It got a csrf = {csrf}")

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

    response = session.post(
        url, 
        data = data, 
        files = files, 
        headers = headers
        )
    
    return response

def upload_task(url, file_name):
    
    response = upload_data(url, file_name)
    # 2023.9.15 Log保存 
    with open("work/upload.log", "ab") as f:
        f.write(response.text.encode())
    
    if response.status_code == 200:
        print("------------- Upload complete -------------")
        
    else:
        print (f"-- missed upload, error: {response.status_code} --")

        
# main function
if __name__ == "__main__":
    print ("-------------- start upload --------------")
    
    # countdown_timer(10)
    
    file_name = 'csvs/' + sys.argv[1] + '.csv'
    print("ファイル名 = ", file_name)
    
    while True:
        response_code = ""
        now = datetime.datetime.now()
        now_full = now.strftime("%Y-%m-%d %H:%M")
        now_s = now.strftime("%S")
        print(now_s)
        if now_s == "05":
            print("It's time to upload!")
            try:
                response = upload_data(URL, file_name)
                response_code = response.status_code
                with open("work/upload.log", "a") as f:
                    # f.write(response.text.encode())
                    f.write(f'{now_full} status({response_code}) : upload complete\n')

            except Exception as e: 
                print("Exception error has occurred")
                with open("work/upload.log", "a") as f:
                    f.write(f'{now_full} status({response_code}) : Exception error occurred {e} \n')
                    
            if response_code == 200:
                print("------------- Upload complete -------------")
        
            else:
                print (f"-- missed upload, error: {response_code} --")
        else:
            print("Not at time, It's " + now.strftime("%Y-%m-%d %H:%M:%S"))
        # threading.Timer(10, upload_task(URL, file_name)).start()
        time.sleep(1)
