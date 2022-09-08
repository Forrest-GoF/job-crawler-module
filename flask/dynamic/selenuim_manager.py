from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_driver(url):
    # 백그라운드 실행 옵션 추가
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # 크롬 드라이버 실행
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(url)
    
    # 스크롤 내리기
    driver.implicitly_wait(30)
    body = driver.find_element(By.CSS_SELECTOR, "body")
    for _ in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    
    return driver
