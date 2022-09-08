import requests
import re
from bs4 import BeautifulSoup

from google.config import header

def crawling(url):
    # check status
    response = requests.get(url, headers=header)
    if response.status_code != requests.codes.ok:
        return []

    # map beautifulSoup
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # get contents list
    title = soup.findAll("h2", {"class":"KLsYvd"})
    key = soup.findAll("div", {"class":"KGjGe"})
    company_name = soup.findAll("div", {"class":"oNwCmf"})
    thumbnail = soup.findAll("div", {"class":"x1z8cb"})
    location = soup.findAll("div", {"class":"oNwCmf"})
    platform = soup.findAll("div","iSJ1kb va9cAf")
    apply_url = soup.findAll("a", {"class":"pMhGee"})
    description = soup.findAll("span", {"class":"HBvzbc"})
    type_salary_date_parent = soup.findAll("div", {"class":"KKh3md"})
    
    # get pre-defined image id
    script_images = re.findall("x3dtbn:(.[^']*)x2", html, re.IGNORECASE)

    # parse data
    job_preview_list = []
    for i in range(len(title)):
        job_preview = {}
        job_preview["title"] = title[i].text
        job_preview["key"] = key[i].get("data-encoded-doc-id")
        job_preview["companyName"] = company_name[i].find("div", {"class":"vNEEBe"}).text
        job_preview["location"] = location[i].find("div", {"class":"Qk80Jf"}).text
        job_preview["platform"] = platform[i].find('span').text
        job_preview["applyUrl"] = apply_url[i].get("href")
        job_preview["description"] = description[i].text

        if thumbnail[i].find('g-img') and script_images:
            job_preview["thumbnail"] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:" + script_images.pop(0).strip("\\")
            script_images.pop(0)

        # extract type/salary/date
        for type_salary_date_tag in type_salary_date_parent[i]:
            type_salary_date_list = type_salary_date_tag.findAll("span", {"class":"LL4CDc"})
            for type_salary_date in type_salary_date_list:
                if type_salary_date.find("span"):
                    salary_date = type_salary_date.find("span").text
                    if salary_date[0].isdigit():
                        job_preview["postedAt"] = salary_date
                    elif salary_date[0] == "₩":
                        job_preview["salary"] = salary_date
                else:
                    job_preview["type"] = type_salary_date.text
        
        # append data
        job_preview_list.append(job_preview)

    # return job list
    return job_preview_list
