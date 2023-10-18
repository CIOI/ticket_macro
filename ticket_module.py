from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep

class Login:
    '''
    attribute
        url
        id
        password
        driver
        wait: 페이지 로딩 최대 10초 기다리기
    method
        retry_click : element 가 클릭이 되지 않았을 때 1초뒤 재시도
        return_driver : self.driver 반환
        1. main_page : webdriver 를 켜고 메인 페이지 접속
        2. into_login_page: 로그인 페이지 접속
        3. login: 로그인 후 메인페이지로 돌아오기
    '''
    def __init__(self, url, id, password):
        self.url=url
        self.id=id
        self.password=password

    def main_page(self):
        self.driver=webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        
    def retry_click(self,element):
        try:
            element.click()
        except:
            print("첫 클릭 실패:")
            sleep(1)
            element.click()
    
    def into_login_page(self):
        try:
            sign_in_link = self.driver.find_element(By.LINK_TEXT,"Sign in")
            self.retry_click(sign_in_link)
            self.driver.implicitly_wait(1)
        except:
            sign_in_link = self.driver.find_element(By.LINK_TEXT,"Sign in")
            self.retry_click(sign_in_link)
            self.driver.implicitly_wait(1)
            print("login 페이지 클릭요망")

    def login(self):
        self.main_page()
        self.into_login_page()
        text_input = self.driver.find_element(By.ID,"EmailAddress1")
        text_input.send_keys(self.id)
        password_input = self.driver.find_element(By.ID, "Password")
        password_input.send_keys(self.password)
        sign_in_link = self.driver.find_element(By.ID, "jq-user-form-submit")
        sign_in_link.click()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
    
    def return_driver(self):
        return self.driver
    
class Choose(Login):
    '''
    commom_method
        return_driver : self.driver 반환
        retry_click : element 가 클릭이 되지 않았을 때 1초뒤 재시도
    
    attribute
            url
            id(Login)
            password(Login)
            driver
            date_calender(Choose) : calender 가 업데이트 될때마다 재지정해줘야함(JavaScript 동적 업데이트 때문)
    
    Login_method
        1. main_page : webdriver 를 켜고 메인 페이지 접속
        2. into_login_page: 로그인 페이지 접속
        3. login: 로그인 후 메인페이지로 돌아오기
    
    Choose_method
    실제로 사용하게 될것은 1과 8
        1. next_month               : 다음달 캘린더로 date_calender를 업데이트(티켓 열리면 1월은 3번 2월은 4번 호출)
        2. prev_month               : 전달 캘린더로 date_calender를 업데이트(사용할일 잘 없을듯)
        3. get_available date       : 캘린더에서 클릭가능한 날짜 요소들을 가져옴
        4. chosse date(target_date) : 날짜 선택
        5. get_available time       : 클릭 가능한 시간 요소들을 가져옴
        6. choose time(target_time) : 시간 선택
        7. select_num               : 장바구니 담기 (0 -> 1)
        7* test_select_num(num=1)   : group 티켓이 아닌 개인티켓 담기(테스트용)
        8. get_ticket(date,time)    : 선택,장바구니 담기까지 과정
        8* test_get_ticket          : 8과 같지만 테스트용
    '''
    def __init__(self, url, id, password) -> None:
        super().__init__(url,id,password)
        
    def get_calender(self):
        self.date_calender=self.driver.find_element(By.CLASS_NAME, 'ui-datepicker-header')
        #캘린더 열릴때까지 기다려
        self.wait.until(EC.presence_of_element_located((By.ID, "calendar-widget")))
        
    def next_month(self):
        try:
            element=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-handler="next"]')))
            
            self.retry_click(element)
        except:
            element=self.driver.find_element(By.CSS_SELECTOR,'[data-handler="next"]')
            print('stop at next_month')
        #calendar_widget = self.wait.until(EC.presence_of_element_located((By.ID, "calendar-widget")))
        #self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-handler="next"]'))).click()
            
        #새로운 캘린더로 초기화
        self.date_calender=self.driver.find_element(By.CLASS_NAME, 'ui-datepicker-header')
    
    def prev_month(self):
        try:
            element=self.driver.find_element(By.CSS_SELECTOR,'[data-handler="prev"]')
            super().retry_click(element)
        except:
            element=self.driver.find_element(By.CSS_SELECTOR,'[data-handler="prev"]')
            print('stop at prev_month')
        self.date_calender=self.driver.find_element(By.CLASS_NAME, 'ui-datepicker-header')
        
    def get_available_date(self):
        self.available_date=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-state-default")))
        print(len(self.available_date))
        #print(element)
        #self.available_date = self.driver.find_elements(By.CLASS_NAME,"high_availability")
        
    def choose_date(self,target_date:str):
        for button in self.available_date:
            if button.text == target_date:
                specific_element = button
                break  # 원하는 요소를 찾으면 반복문 종료
        specific_element.click()

    def get_available_time(self):
        self.available_time = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"day-show")))
        print('가능시간 개수',len(self.available_time))
        
    def choose_time(self,target_time:str):
        global time_button
        print(self.available_time)
        for t in self.available_time:
            try:
                time_button=t.find_element(By.LINK_TEXT,target_time)
                break #원하는 날짜를 찾으면 바로 종료
            except:
                pass
        #더블클릭
        try:
            time_button.click()
        except:
            sleep(1)
            time_button.click()
        
    def select_num(self):
        try:
            group_reservation = self.driver.find_element(By.CSS_SELECTOR,'.jq-basket-item[data-ticket="2399"]')
            select_element = group_reservation.find_element(By.CSS_SELECTOR,'select.jq-basket-item-quantity')
        except:
            group_reservation = self.driver.find_element(By.CSS_SELECTOR,'.jq-basket-item[data-ticket="2399"]')
            select_element = group_reservation.find_element(By.CSS_SELECTOR,'select.jq-basket-item-quantity')
        select = Select(select_element)
        select.select_by_value('1')

    def test_select_num(self,num='1'):
        num_of_participant = self.driver.find_element(By.CSS_SELECTOR,'.jq-basket-item[data-ticket="2400"]')
        select_element = num_of_participant.find_element(By.CSS_SELECTOR,'select.jq-basket-item-quantity')
        sleep(1)
        select = Select(select_element)
        select.select_by_value(num)

    def get_ticket(self,target_date,target_time):
        sleep(1)
        self.get_available_date()
        self.choose_date(target_date)
        sleep(1)
        self.get_available_time()
        self.choose_time(target_time)
        sleep(1)
        self.select_num()
    
    def test_get_ticket(self,target_date,target_time):
        sleep(1)
        self.get_available_date()
        self.choose_date(target_date)
        sleep(1)
        self.get_available_time()
        self.choose_time(target_time)
        sleep(1)
        self.test_select_num()
        
class Checkout(Choose):
    def __init__(self, url:str, id:str, password:str, surname:str,firstname:str,card_info:list):
        super().__init__(url,id,password)
        self.surname=surname
        self.firstname=firstname
        self.card_info=card_info
    
    def finalize(self):
        finalize_order_link  = self.wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT,'Finalize your order')))        
        finalize_order_link.click()
        self.driver.implicitly_wait(10)
    
    def review_page(self):
        checkbox = self.driver.find_element(By.NAME, "cgvConfirm")
        checkbox.click()
        confirm_button=self.wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR,'a#jq-checkout-confirm')))
        confirm_button.click()
    
    def guide_info_page(self):
        surname_boxs=self.driver.find_elements(By.ID,"SurName")
        firstname_boxs=self.driver.find_elements(By.ID,"FirstName")
        for sbox in surname_boxs:
            sbox.send_keys(self.surname)
        for fbox in firstname_boxs:
            fbox.send_keys(self.firstname)
        confirm_button=self.wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT,'Payment')))
        sleep(2)
        confirm_button.click()
        self.driver.implicitly_wait(10)
    
    def pay(self):
        visa_radio_button=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[type="radio"][name="PBX_TYPECARTE"][value="VISA"]')))
        sleep(1)
        visa_radio_button.click()
        button = self.wait.until(EC.element_to_be_clickable((By.ID,'boutonA0')))# 요소 클릭
        button.click()
        self.driver.implicitly_wait(10)
    
    def insert_card_info(self):
        numero_carte_field = self.driver.find_element(By.ID,'NUMERO_CARTE')
        numero_carte_field.send_keys(self.card_info[0])
        select_month_element = self.driver.find_element(By.ID,'MOIS_VALIDITE')# Select 객체로 변환
        select_month = Select(select_month_element)
        select_month.select_by_value(self.card_info[1])
        select_year_element = self.driver.find_element(By.ID,'MOIS_VALIDITE')# Select 객체로 변환
        select_year = Select(select_year_element)
        select_year.select_by_value(self.card_info[2])
        CV=self.driver.find_element(By.ID,"CVVX")
        CV.send_keys(self.card_info[3])
        val=self.wait.until(EC.element_to_be_clickable((By.ID,"VALIDER")))
        sleep(1)
        val.click()
        
    def checkout(self):
        self.finalize()
        self.review_page()
        self.guide_info_page()
        self.pay()
        self.insert_card_info()       