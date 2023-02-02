import requests
from datetime import datetime
import urllib

i_sodi = 443 # midnight two weeks out
dhamaka = 48994
laser_wolf = 58848 # 10 AM 21 days out 
lilia = 418 # 10 AM 30 days out
misi = 3015 # 10 am 30 days out 
una_pizza = 6066 # 9 AM two weeks out
claud = 62659 # 9 am 14 days out
test = 60351
day = "2023-02-17" # 
reservation_times = ['19:45:00', '20:00:00', '20:15:00', '20:30:00']
reservation_times_formatted = []
for i in reservation_times:
    reservation_times_formatted.append(datetime.strptime(day + " " + i, '%Y-%m-%d %H:%M:%S'))
party_size = 2


find_headers = {'Authorization': 'ResyAPI api_key=""'}
find_url = 'https://api.resy.com/4/find?lat=40.730610&long=-73.935242&venue_id=' + str(claud) + '&day=' + day + '&party_size=' + str(party_size)

r_find = requests.get(url = find_url, headers=find_headers)
data_find = r_find.json()

config_tokens = []
available_reservations = data_find["results"]["venues"][0]["slots"]
print("Avail reservations: ", len(available_reservations))
for i in available_reservations:
    datetime_object = datetime.strptime(i["date"]["start"], '%Y-%m-%d %H:%M:%S')
    if datetime_object in reservation_times_formatted:
        config_tokens.append(i["config"]["token"])
if len(config_tokens) == 0:
    print("No reservations")
else:
    details_url = 'https://api.resy.com/3/details?party_size=' + str(party_size) + "&day=" + day + "&config_id=" + urllib.parse.quote(config_tokens[0])
    details_headers = {'Authorization': 'ResyAPI api_key=""', 'Content-Type': 'application/x-www-form-urlencoded'}

    r_details = requests.get(url = details_url, headers=details_headers)
    data_details = r_details.json()
    book_token = data_details["book_token"]["value"]

    book_url = "https://api.resy.com/3/book"
    book_headers = {
        'Authorization': 'ResyAPI api_key=""',
        'X-Resy-Auth-Token': '',
    }
    book_post_data = {
        'book_token': book_token,
        'struct_payment_method': '{"id":}',
    }

    r_book = requests.post(url = book_url, data = book_post_data, headers = book_headers)
    data_book = r_book.json()
    print(data_book)
