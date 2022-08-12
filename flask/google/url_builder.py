from google.validator import valid_params

def bulid(params):

    # Domain
    url = "https://www.google.com"

    # Required
    url += ("/search?q=" + params["q"])
    url += ("&start=" + str(params["start"]))
    url += "&ibp=htl;jobs"

    # Set Location
    url += "&uule=w+CAIQICILU291dGggS29yZWE"
    url += "&hl=ko"
    url += "&gl=kr"

    # Set URL
    url += "#htivrt=jobs"

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
