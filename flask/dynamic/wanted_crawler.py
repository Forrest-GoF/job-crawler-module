from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def crawling(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    time.sleep(2)
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")

    result = {}
    
    # 기술스택
    stacks = []
    elements = driver.find_elements(By.CLASS_NAME, "SkillItem_SkillItem__E2WtM")
    for element in elements:
        stacks.append(element.get_attribute('innerText'))
    result["stacks"] = stacks

    # 상세내용
    keys = ["introduction", "mainTask", "qualification", "preferential", "benefit"]
    elements = driver.find_element(By.CLASS_NAME, "JobDescription_JobDescription__VWfcb")\
        .find_elements(By.TAG_NAME, "p")
    for key, element in zip(keys, elements):
        value = element.get_attribute("innerText")
        result[key] = value

    # 마감일 & 근무지역
    keys = ["deadline", "location"]
    elements = driver.find_element(By.CLASS_NAME, "JobWorkPlace_className__ra6rp")\
        .find_elements(By.TAG_NAME, "div")
    for key, element in zip(keys, elements):
        value = element.find_element(By.CLASS_NAME, "body").get_attribute("innerText")
        result[key] = value

    driver.close()
    return result
