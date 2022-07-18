import requests
from config import set_header
from bs4 import BeautifulSoup

def crawling(q="개발자", start=0, date_posted="", employment_type=""):
    # set header
    headers = set_header()
    
    # build url
    url = build_url(q, start, date_posted, employment_type)

    # print log
    print("CRAWLING URL: " + url)

    # check status
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        return "Error!!!"

    # map beautifulSoup
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # get contents list
    title = soup.findAll("h2", {"class":"SBkjJd"})
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

def build_url(q, start, date_posted, employment_type):
    # Domain
    url = "https://www.google.com"

    # Required
    url += ("/search?q=" + q)
    url += ("&start=" + str(start))
    url += "&ibp=htl;jobs#htivrt=jobs"

    # Optional
    date_tail, type_tail = "",""
    if date_posted in ["today", "3days", "week", "month"]:
        url += ("&htichips=date_posted:" + date_posted)
        date_tail = ("&htischips=date_posted;" + date_posted)
    if employment_type in ["FULLTIME", "INTERN", "CONTRACTOR", "PARTTIME"]:
        if date_tail:
            url += ","
            type_tail = ","
        else:
            url += "&htichips="
            type_tail = "&htischips="
        url += ("employment_type:" + employment_type)
        type_tail += "employment_type;" + employment_type
    url += (date_tail + type_tail)

    return url
