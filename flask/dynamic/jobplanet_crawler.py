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
    keys = ["introduction", "main_task", "qualification", "preferential", "procedure", "benefit", "기타", "location"]
    elements = driver.find_elements(By.CLASS_NAME, "recruitment-detail__txt")
    if len(elements)==7: keys.remove("기타")
    print(elements[-2].get_attribute('innerText'), len(keys))
    for key, element in zip(keys, elements):
        value = element.get_attribute('innerText')
        if key!="기타":
            result[key] = value

    # 상세
    keys = ["expired_at", "직무", "career", "type", "salary", "stacks"]
    elements = driver.find_elements(By.CLASS_NAME, "recruitment-summary__dd")
    for key, element in zip(keys, elements):
        value = element.get_attribute('innerText')
        if key!="직무":
            result[key] = value
        elif key=="stacks":
            result["stacks"] = value.split(',')

    driver.close()
    return result
