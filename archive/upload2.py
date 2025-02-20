import sys
import requests
import datetime
import time
import threading
# import pprint
# import json

#Network/NTP
import network
import rp2
import ntptime
#import time


# This is the target url
URL = 'http://10.10.210.87/upload/'

#Wi-Fi接続パラメータ
ssid = "0024A5C1575C-G/A"
password = "s3ws533kkphsh"
#日本標準時(UTC+9時間)
UTC_OFFSET = 9
#NTPサーバ ドメイン
NTP_SRV = "ntp.nict.jp"


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
    #print(f"It got a csrf = {csrf}")

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
    with open("../upload_file/upload.log", "ab") as f:
        f.write(response.text.encode())
    
    if response.status_code == 200:
        print("------------- Upload complete -------------")
        
    else:
        print (f"-- missed upload, error: {response.status_code} --")

        
# main function
if __name__ == "__main__":
    print ("-------------- start upload --------------")
    
    # countdown_timer(10)
    dir_path = "/home/pi/works/upload_file/"
    file_name = dir_path + sys.argv[1] + '.csv'
    print("ファイル名 = ", file_name)
    
    try:
        #Wi-Fiに接続
        print ("--- connecting ---")
        ip_add = wifi_connect()
    
        #NTPサーバから日時取得
        get_ntp_time()    
        #1秒待ち
        time.sleep(1)
        

    except KeyboardInterrupt:
        # Turn off the display
        print("「Ctrl + c」キーが押されました。")
    
    while True:
        response_code = ""
        now = datetime.datetime.now()
        now_full = now.strftime("%Y-%m-%d %H:%M")
        now_s = now.strftime("%S")

        print("\rnow: "+now_s,end="")
        if now_s == "05":
            print("\n")
            print(f"Start to upload! @{now_full}.")
            try:
                response = upload_data(URL, file_name)
                response_code = response.status_code
                with open("../upload_file/upload.log", "a") as f:
                    # f.write(response.text.encode())
                    f.write(f'{now_full} status({response_code}) : upload complete\n')

            except Exception as e: 
                print("Exception error has occurred")
                with open("../upload_file/upload.log", "a") as f:
                    f.write(f'{now_full} status({response_code}) : Exception error occurred {e} \n')
                    
            if response_code == 200:
                print("------------- Upload complete -------------")
        
            else:
                print (f"-- missed upload, error: {response_code} --")
        time.sleep(1)

#except KeyboardInterrupt:
    # Turn off the display
#    print("「Ctrl + c」キーが押されました。")

##################################################
#      液晶ディスプレイ（LCD）初期設定
##################################################

#I2Cを利用するため、オブジェクト（i2c）を作成
#i2c = I2C(0,sda=Pin(16), scl=Pin(17), freq=400000)
#LCDのパラメータを設定
#ADR = 0x27
#ROW = 2
#COL = 16

#LCDを利用するため、オブジェクト（lcd）を作成
#lcd = I2cLcd(i2c, ADR, ROW, COL)

##################################################
#      【関数】Wi-Fiに接続
##################################################

def wifi_connect():
    #Wi-Fi地域（日本）の設定
    rp2.country('JP')

    #ステーションインタフェースの有効化
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    #Wi-Fiの省電力をオフに設定
    wlan.config(pm = 0xa11140)
    
    #液晶ディスプレイ画面を消去
    #lcd.clear()

    #Wi-Fiに接続
    wlan.connect(ssid, password)
    while not wlan.isconnected() and wlan.status() >= 0:

        #LCDに文字表示
        #lcd_disp("Wait for", "connection...")       
        #time.sleep(1)
    
    ip_add = wlan.ifconfig()[0]
    #lcd_disp("Connected on", f' {ip_add}')
    
    #ダミー
    time.sleep(2)

    return ip_add


##################################################
#      【関数】NTPサーバから日時取得
##################################################

def get_ntp_time():

    #NTPサーバ
    ntptime.server = NTP_SRV
    
    #NTPサーバへの接続待ち
    time.sleep(1)
    
    #ローカル時刻をUTC標準時刻に同期
    ntptime.settime()
      
    #液晶ディスプレイ画面を消去
    lcd.clear()
    
    #LCDに文字表示
    lcd_disp("Connected to", "NTP server.")
    
    #ダミー
    time.sleep(2)

##################################################
#      【関数】日付・時刻整形
##################################################

def format_dttm(day_tm):
    
    #日付
    dat = ("%4d/%02d/%02d" % (day_tm[0:3]))
    
    #時刻
    tm = ("%2d:%02d:%02d" % (day_tm[3:6]))
    
    return dat ,tm


##################################################
#      【関数】LCDに文字表示
##################################################

#def lcd_disp(msg1, msg2):
    #LCDに文字を表示
#    lcd.move_to(0, 0)
#    lcd.putstr(msg1) 
#    lcd.move_to(0, 1)
#    lcd.putstr(msg2)


##################################################
#      【関数】日付時刻を取得
##################################################

def get_dattm():
     
    #ローカル時刻
    lcl_tm =  time.localtime(time.mktime(time.localtime()) + UTC_OFFSET * 60 * 60)          
   
    #日付・時刻整形
    dat ,tm = format_dttm(lcl_tm)
        
    return dat,tm
   
   
##################################################
#      メイン
##################################################

try:
    
    #Wi-Fiに接続
    ip_add = wifi_connect()
    
    #NTPサーバから日時取得
    get_ntp_time()
    
    #液晶ディスプレイ画面を消去
#    lcd.clear()
    
    #液晶ディスプレイに日付・時刻表示
#    while True:
        #日付・時刻を取得
#        dat,tm = get_dattm()    
    
        #LCDに文字表示
#        lcd_disp(dat, tm)
        
        #1秒待ち
        time.sleep(1)
        

except KeyboardInterrupt:
    # Turn off the display
    print("「Ctrl + c」キーが押されました。")
    
    #LCD消灯
#    lcd.backlight_off()
#    lcd.display_off()
    
#    machine.reset()
