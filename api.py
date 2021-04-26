import sys, urllib, pprint, requests, json

date = sys.argv[1]
date_list = [1, "eq", [date]]

query = {
	"resource": "http://www.chp.gov.hk/files/misc/latest_situation_of_reported_cases_covid_19_eng.csv",
	"section":1,
	"format":"json",
	"filters": [
		date_list
	]
}

response = requests.get("https://api.data.gov.hk/v2/filter?q=%s" % urllib.parse.quote_plus(json.dumps(query)).replace('+', ''))

print("\nResponse status: %d\n"%response.status_code)
pprint.pprint(response.json())