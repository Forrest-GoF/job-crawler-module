from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def crawling(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    time.sleep(1)
    driver.implicitly_wait(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")

    result = {}
    
    # 기술스택
    stacks = []
    elements = driver.find_elements(By.CLASS_NAME, "sc-eicpiI")
    for element in elements:
        stacks.append(element.get_attribute('innerText'))
    result["stacks"] = stacks

    # 상세내용
    keys = ["기술스택", "mainTask", "qualification", "preferential", "benefit", "procedure"]
    elements = driver.find_elements(By.CLASS_NAME, "sc-cVAmsi")
    for key, element in zip(keys, elements):
        value = element.find_element(By.TAG_NAME, "pre").get_attribute("innerText")
        if key!="기술스택":
            result[key] = value

    # 요약
    keys = ["career", "education", "deadline", "location"]
    elements = driver.find_elements(By.CLASS_NAME, "styles_item__LhiHT")
    for key, element in zip(keys, elements):
        value = element.find_element(By.TAG_NAME, "dd").get_attribute("innerText")
        result[key] = value

    driver.close()
    return result
