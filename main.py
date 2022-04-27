from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def find_airline_tickets():
    SCROLL_PAUSE_SEC = 3
    RELOAD_SEC = 1
    cards = []
    function_start_time = time.time()

    while len(cards) < 1:
        cards = driver.find_elements(by=By.CLASS_NAME, value="domestic_Flight__sK0eA")

        time.sleep(RELOAD_SEC)
        check_function_process_time(function_start_time)

    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = -1

    while new_height != last_height:
        last_height = new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_SEC)

        new_height = driver.execute_script("return document.body.scrollHeight")
        cards = driver.find_elements(by=By.CLASS_NAME, value="domestic_Flight__sK0eA")

        check_function_process_time(function_start_time)

    return cards

def check_function_process_time(start_time):
    process_time = time.time() - start_time
    PROCESS_OVER_TIME = 60 # 1분

    if process_time > PROCESS_OVER_TIME:
        raise RuntimeError("정상 프로세스 시간을 초과하였습니다.")

def find_start_time_and_price(text):
    start_time_pattern = re.compile('\d{2}:\d{2}CJU')
    price_pattern = re.compile('\d{2,3},\d{3}원')
    start_time = start_time_pattern.findall(text)[0]
    price = price_pattern.findall(text)[0]

    return dict(start_time=start_time, price=price)

def is_match(start_time, price):
    MINIMUM_HOUR = 13
    MAX_PRICE = 150
    start_hour = start_time[0:5].split(":")[0]
    p = price[0:-1].split(",")[0]

    if int(start_hour) > MINIMUM_HOUR and int(p) < MAX_PRICE:
        return True;

    return False;

if __name__ == '__main__':
    URL = "https://flight.naver.com/flights/domestic/CJU-SEL-20220515?adult=1&fareType=YC"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url=URL)

    try:
        while True:
            airline_tickets = find_airline_tickets()
            latest_air_line = airline_tickets[len(airline_tickets) - 1]
            result_dict = find_start_time_and_price(latest_air_line.text)
            result = is_match(result_dict['start_time'], result_dict['price'])
            print(result_dict['start_time'], result_dict['price'])
            print(result)
    except RuntimeError as error:
        print(str(error))