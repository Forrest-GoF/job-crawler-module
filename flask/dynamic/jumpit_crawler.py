from selenium.webdriver.common.by import By
from dynamic.selenuim_manager import get_driver


def crawling(url):
    driver = get_driver(url)
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
        if key != "기술스택":
            result[key] = value

    # 요약
    keys = ["career", "education", "deadline", "location"]
    elements = driver.find_elements(By.CLASS_NAME, "styles_item__LhiHT")
    for key, element in zip(keys, elements):
        value = element.find_element(By.TAG_NAME, "dd").get_attribute("innerText")
        result[key] = value

    driver.close()
    return result
