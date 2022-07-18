from crawler import crawling

crawling()
crawling(q="백엔드")
crawling(q="백엔드", date_posted="3days")
crawling(q="백엔드", employment_type="FULLTIME")
crawling(q="백엔드", date_posted="3days", employment_type="FULLTIME")
crawling(q="백엔드", start =10, date_posted="3days", employment_type="FULLTIME")
