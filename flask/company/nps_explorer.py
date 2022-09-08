import requests
import xmltodict
import re
import os
from dotenv import load_dotenv

load_dotenv()
api_key_decode = requests.utils.unquote(os.getenv('NPS_KEY'))
base_url = "http://apis.data.go.kr/B552015/NpsBplcInfoInqireService"


def get_bass(company_name):
    # parameter settings
    parameters = {
        "serviceKey": api_key_decode,
        "wkpl_nm": company_name_processing(company_name),
        "pageNo": 1,
        "startPage": 1,
        "pageSize": 10,
        "numOfRows": 99999
    }

    # url request
    url = base_url + '/getBassInfoSearch'
    req = requests.get(url, params=parameters)

    # xml to dict
    data_dict = xmltodict.parse(req.text)
    data_list = data_dict['response']['body']['items']['item']

    # most recent data parsing
    companies = {}
    for data in reversed(data_list):
        unique_key = data['wkplNm'] + data['bzowrRgstNo'][:6]
        if unique_key not in companies:
            company = parse_data(data)
            company["updatedAt"] = data['dataCrtYm']
            company["seq"] = data['seq']
            companies[unique_key] = company

    return list(companies.values())


def get_detail(seq):
    # parameter settings
    parameters = {
        "serviceKey": api_key_decode,
        "seq": seq
    }

    # url request
    url = base_url + '/getDetailInfoSearch'
    req = requests.get(url, params=parameters)

    # xml to dict
    data_dict = xmltodict.parse(req.text)
    data = data_dict['response']['body']['item']

    # data parsing
    company = parse_data(data)

    # get detail data
    company['employeeCount'] = data['jnngpCnt']
    company['paidPension'] = data['crrmmNtcAmt']
    company['pensionPerEmployee'] = str(int(int(company['paidPension']) / int(company['employeeCount']) / 2))
    company['foundingDate'] = data['adptDt']

    # calculate average annual salary
    company['averageAnnualSalary'] = str(int(int(company['pensionPerEmployee']) / 0.09 * 2 * 12))

    return company


def parse_data(data):
    registrationStatus = {"1": "REGISTRATION", "2": "WITHDRAWAL"}
    registrationType = {"1": "CORPORATION", "2": "INDIVIDUAL"}

    return {
        "key": data['wkplNm'] + data['bzowrRgstNo'][:6],
        "name": company_name_processing(data['wkplNm']),
        "registrationNumber": data['bzowrRgstNo'][:6],
        "address": data['wkplRoadNmDtlAddr'],
        "registrationStatus": registrationStatus[data['wkplJnngStcd']],
        "registrationType": registrationType[data['wkplStylDvcd']],
        "countyCode": data['ldongAddrMgplDgCd'],
        "cityCode": data["ldongAddrMgplSgguCd"],
        "townCode": data["ldongAddrMgplSgguEmdCd"]
    }


def company_name_processing(original_company_name):
    company_name = original_company_name.replace(" ", "").replace("㈜", "").replace("주식회사", "")
    return str(re.sub(pattern='\([^)]*\)', repl='', string=company_name))
