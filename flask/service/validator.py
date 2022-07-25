def valid_params(p):
    expected_date_posted = ["today", "3days", "week", "month"]
    employment_type = ["FULLTIME", "INTERN", "CONTRACTOR", "PARTTIME"]

    if "q" not in p or not p["q"]:
        raise Exception('q는 필수 파라미터입니다.')

    if "start" not in p:
        p["start"] = "0"
    elif not p["start"].isdigit():
        raise Exception('start가 올바르지 않습니다.')

    if "date_posted" not in p:
        p["date_posted"] = ""
    elif p["date_posted"] not in expected_date_posted:
        raise Exception('date_posted가 올바르지 않습니다. (today / 3days / week / month)')

    if "employment_type" not in p:
        p["employment_type"] = ""
    elif p["employment_type"] not in employment_type:
        raise Exception('employment_type이 올바르지 않습니다. (FULLTIME / INTERN / CONTRACTOR / PARTTIME)')
