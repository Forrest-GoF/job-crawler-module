import requests
from bs4 import BeautifulSoup

from service.config import header

def crawling(url):
    # check status
    response = requests.get(url, headers=header)
    if response.status_code != requests.codes.ok:
        return "Status Error!!!"

    # map beautifulSoup
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # get contents list
    title = soup.findAll("h2", {"class":"KLsYvd"})
    id = soup.findAll("div", {"class":"KGjGe"})
    company_name = soup.findAll("div", {"class":"oNwCmf"})
    thumbnail = soup.findAll("div", {"class":"x1z8cb"})
    location = soup.findAll("div", {"class":"oNwCmf"})
    platform = soup.findAll("div","iSJ1kb va9cAf")
    url = soup.findAll("a", {"class":"pMhGee"})
    description = soup.findAll("span", {"class":"HBvzbc"})
    type_salary_date_parent = soup.findAll("div", {"class":"KKh3md"})
    
    # parse data
    job_preview_list = []
    for i in range(len(title)):
        job_preview = {}
        job_preview["title"] = title[i].text
        job_preview["id"] = id[i].get("data-encoded-doc-id")
        job_preview["company_name"] = company_name[i].find("div", {"class":"vNEEBe"}).text
        job_preview["location"] = location[i].find("div", {"class":"Qk80Jf"}).text
        job_preview["platform"] = platform[i].find('span').text
        job_preview["applyUrl"] = url[i].get("href")
        job_preview["description"] = description[i].text

        if thumbnail[i].find('g-img'):
            job_preview["thumbnail"] = thumbnail[i].find('g-img').find('img').get("src")

        # extract type/salary/date
        for type_salary_date_tag in type_salary_date_parent:
            type_salary_dates = type_salary_date_tag.findAll("span", {"class":"LL4CDc"})
            for type_salary_date in type_salary_dates:
                if type_salary_date.find("span"):
                    date_salary = type_salary_date.text
                    if date_salary[0].isdigit():
                        job_preview["postedAt"] = date_salary
                    elif date_salary[0] == "₩":
                        job_preview["salary"] = date_salary
                else:
                    job_preview["type"] = type_salary_date.text
        
        # append data
        job_preview_list.append(job_preview)

    # return job list
    return job_preview_list

def build_url(params):
    
    # valid parameters & set default parameters
    valid_params(params)

    # Domain
    url = "https://www.google.com"

    # Required
    url += ("/search?q=" + params["q"])
    url += ("&start=" + params["start"])
    url += "&ibp=htl;jobs#htivrt=jobs"

    # Optional
    date_tail, type_tail = "",""
    if params["date_posted"]:
        url += ("&htichips=date_posted:" + params["date_posted"])
        date_tail = ("&htischips=date_posted;" + params["date_posted"])

    if params["employment_type"]:
        if date_tail:
            url += ","
            type_tail = ","
        else:
            url += "&htichips="
            type_tail = "&htischips="
        url += ("employment_type:" + params["employment_type"])
        type_tail += "employment_type;" + params["employment_type"]
        
    url += (date_tail + type_tail)

    return url

def valid_params(p):
    DEFAULT_Q = "개발"
    DEFAULT_STARAT = "0"
    DEFALUT_DATE_POSTED = ""
    DEFALUT_EMPLOYMENT_TYPE = ""
    expected_date_posted = ["today", "3days", "week", "month"]
    employment_type = ["FULLTIME", "INTERN", "CONTRACTOR", "PARTTIME"]

    if "q" not in p:
        p["q"] = DEFAULT_Q
    if "start" not in p or not p["start"].isdigit():
        p["start"] = DEFAULT_STARAT
    if "date_posted" not in p or p["date_posted"] not in expected_date_posted:
        p["date_posted"] = DEFALUT_DATE_POSTED
    if "employment_type" not in p or p["employment_type"] not in employment_type:
        p["employment_type"] = DEFALUT_EMPLOYMENT_TYPE    
