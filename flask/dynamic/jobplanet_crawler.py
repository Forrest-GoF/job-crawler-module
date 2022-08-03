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
    
    # 본문
    keys = ["introduction", "제목", "qualification", "preferential", "procedure", "benefit", "etc", "location"]
    elements = driver.find_elements(By.CLASS_NAME, "recruitment-detail__txt")
    for key, element in zip(keys, elements):
        value = element.get_attribute('innerText')
        if key != "제목":
            result[key] = value

    # 마감일
    deadline = driver.find_element(By.CLASS_NAME, "recruitment-summary__end").get_attribute("innerText")
    result["deadline"] = deadline

    # 상세
    keys = ["마감일", "직무", "경력", "고용형태", "급여", "스킬"]
    elements = driver.find_elements(By.CLASS_NAME, "recruitment-summary__dd")
    for key, element in zip(keys, elements):
        value = element.get_attribute('innerText')
        if key=="경력":
            result["career"] = value
        elif key=="스킬":
            result["stacks"] = value.split(',')

    driver.close()
    return result
