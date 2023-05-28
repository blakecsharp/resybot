import base64
import requests
import datetime
import urllib

don_angie = 1505
four_charles = 834
dame = 34341
dcp = 42534
una_pizza = 6066
laser_wolf = 58848
test = 55
venue_id = test
# today_algo = datetime.date.today() + datetime.timedelta(days=13)
# day = today_algo.strftime("%Y-%m-%d")
day = "2023-06-15"


first_choice_reservation_times = ['19:00:00', '21:15:00', '19:30:00', '18:45:00', '21:30:00','20:00:00', '20:15:00', '20:30:00', '21:00:00']
second_choice_reservation_times = ['17:15:00', '21:45:00', '17:00:00','17:30:00','17:45:00', "22:00:00", "22:15:00", '18:00:00','18:30:00', '18:15:00','19:45:00']

party_size = 2

def make_resy(config_token):
    details_headers = {'Authorization': 'ResyAPI api_key=""', 
                       'Content-Type': 'application/x-www-form-urlencoded',
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                        "Origin": "https://resy.com",
                        "Referer": "https://resy.com/"}

    details_url = 'https://api.resy.com/3/details?party_size=' + str(party_size) + "&day=" + day + "&config_id=" + urllib.parse.quote(config_token)
    r_details = requests.get(url = details_url, headers=details_headers)
    data_details = r_details.json()
    book_token = data_details["book_token"]["value"]

    auth_url = "https://api.resy.com/3/auth/password"
    auth_post_data = {
        'email': '',
        'password': '',
    }
    r_auth = requests.post(url = auth_url, data = auth_post_data, headers = details_headers)
    auth_response = r_auth.json()
    auth_token = auth_response['token']

    book_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Origin": "https://resy.com",
        "Referer": "https://resy.com/",
        'Authorization': 'ResyAPI api_key=""', 
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'X-Origin': 'https://widgets.resy.com',
        'X-Resy-Auth-Token': auth_token,
        'X-Resy-Universal-Auth': auth_token,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Ch-Ua-mobile': '?0',
        'Sec-Ch-Ua-platform': '"macOS"',
        'Authority': 'api.resy.com',
        'Sec-Fetch-Dest': 'empty',
        'Cache-Control': 'no-cache',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    book_post_data = {
        'book_token': book_token,
        'struct_payment_method': '{"id":16150987}',
        'source_id': 'resy.com-venue-details'
    }
    book_url = "https://api.resy.com/3/book"
    r_book = requests.post(url = book_url, data = book_post_data, headers = book_headers)
    
    print("headers", r_book.request.headers)
    print(r_book)


first_choice_reservation_times_formatted = []
second_choice_reservation_times_formatted = []

for i in first_choice_reservation_times:
    first_choice_reservation_times_formatted.append(datetime.datetime.strptime(day + " " + i, '%Y-%m-%d %H:%M:%S'))
for i in second_choice_reservation_times:
    second_choice_reservation_times_formatted.append(datetime.datetime.strptime(day + " " + i, '%Y-%m-%d %H:%M:%S'))

find_headers = {'Authorization': 'ResyAPI api_key=""', 
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Origin": "https://resy.com",
                "Referer": "https://resy.com/"}
find_url = "https://api.resy.com/4/find?day=" + str(day) + "&lat=40.7211951220751&location=ny&long=-73.9586259886538&party_size=" + str(party_size) + "&venue_id=" + str(venue_id) + "&exclude_non_discoverable=true&sort_by=available"
r_find = requests.get(url = find_url, headers=find_headers)
data_find = r_find.json()

fc_config_tokens = []
sc_config_tokens = []

available_reservations = data_find["results"]["venues"][0]["slots"]
print("Avail reservations: ", len(available_reservations))
print(available_reservations)

for i in available_reservations:
    datetime_object = datetime.datetime.strptime(i["date"]["start"], '%Y-%m-%d %H:%M:%S')
    if datetime_object in first_choice_reservation_times_formatted and 'out' not in i["config"]["type"].lower():
        fc_config_tokens.append(i["config"]["token"])
    if datetime_object in second_choice_reservation_times_formatted or datetime_object in first_choice_reservation_times_formatted:
        sc_config_tokens.append(i["config"]["token"])

if len(fc_config_tokens) == 0:
    print("No first choice reservations")
if len(fc_config_tokens) > 0:
    print("Getting first choice")
    make_resy(fc_config_tokens[0])
elif len(sc_config_tokens) > 0:
    print("Getting second choice")
    make_resy(sc_config_tokens[0])
