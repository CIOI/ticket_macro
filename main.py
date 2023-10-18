import selenium
import ticket_module
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ticket_module import Choose,Login,Checkout

import json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

url = config['url']
id = config
id_test  = config['id_test']
email_dict = config['email_dict']
password = config['password']
password_test = config['password_test']
timelist_Ann = config['timelist_Ann']
timelist_Gang = config['timelist_Gang']
timelist_HERA = config['timelist_Hera']
timelist_Art = config['timelist_Art']
card_info = config['card_info']
test_card_info = config['test_card_info']

if __name__=='__main__':
    driver1 = Checkout(url,email_dict['email1'],password,'myreal','trip',card_info)
    #driver2 = Checkout(url,email_dict['email2'],password,'myreal','trip',card_info)
    driver1.login()
    #driver2.login()
    driver1.next_month()
    for d,t in timelist_Gang['2']:
        try:
            driver1.test_get_ticket(d,t)
        except:
            print(d,'날짜',t,'시간 실패')
            pass
    
    while True:
        user_input = input("프로그램을 종료하려면 'exit'을 입력하세요: ")
        if user_input.lower() == 'exit':
            print("프로그램을 종료합니다.")
            break  # 루프를 빠져나가고 프로그램 종료