from selenium.webdriver.common.by import By
from dynamic.selenuim_manager import get_driver

# https://www.jumpit.co.kr/position/4075?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic

def crawling(url):
    driver = get_driver(url)
    result = {}

    keys = ["stacks", "mainTask", "qualification", "preferential", "benefit", "procedure"]
    elements = driver.find_elements(By.TAG_NAME, "pre")

    for key, element in zip(keys, elements):
        if key == "stacks":
            value = []
            for stack in element.find_elements(By.CLASS_NAME, "sc-dkqQuH"):
                value.append(stack.get_attribute('innerText'))
        else:
            value = element.get_attribute("innerText")
        
        result[key] = value

    # 요약
    keys = ["career", "education", "deadline", "location"]
    elements = driver.find_elements(By.CLASS_NAME, "styles_item__LhiHT")
    for key, element in zip(keys, elements):
        value = element.find_element(By.TAG_NAME, "dd").get_attribute("innerText")
        result[key] = value

    driver.close()
    return result
