from crawler import build_url, crawling

params = {}
# params["q"] = "백엔드"
# params["start"] = "1"
# params["date_posted"] = "month"
# params["employment_type"] = "FULLTIME"

url = build_url(params)
data = crawling(url)

print("Crawling url:", url)
print("num of jobs:", len(data))
