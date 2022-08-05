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
    stack_element = driver.find_element(By.CLASS_NAME, "job-specialties")
    for element in stack_element.find_elements(By.CLASS_NAME, "ui"):
        stacks.append(element.get_attribute('innerText'))
    result["stacks"] = stacks

    # 주요업무
    main_task = driver.find_element(By.CLASS_NAME, "duty.break").get_attribute("innerText")
    result["main_task"] = main_task

    # 채용 상세
    description = driver.find_element(By.CLASS_NAME, "content.break").get_attribute("innerText")
    result["introduction"] = description

    # 복지 혜택
    benefit = {}
    keys = ["개인 장비", "자기 계발", "통근, 교통", "식사, 간식", "연차, 휴가", "보험, 의료"]
    elements = driver.find_element(By.CLASS_NAME, "ui.divided.company.info.items")\
        .find_elements(By.CLASS_NAME, "content")
    for key, element in zip(keys, elements):
        benefit[key] = element.get_attribute('innerText')
    result["benefit"] = str(benefit)

    # 근무지
    location = driver.find_element(By.CLASS_NAME, "address").get_attribute("innerText")
    result["location"] = location

    # 요약
    keys = ["채용 분야", "지역", "경력 여부", "고용 형태", "연봉", "마감일", "수정일"]
    elements = driver.find_element(By.CLASS_NAME, "ui.job-infoset-content.items")\
        .find_elements(By.CLASS_NAME, "content")
    for key, element in zip(keys, elements):
        value = element.get_attribute("innerText")
        if key=="경력 여부":
            result["career"] = value
        elif key=="연봉":
            result["salary"] = value
        elif key=="마감일":
            result["deadline"] = value

    driver.close()
    return result
