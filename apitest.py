from hashlib import sha1
import hmac
import requests
import json
import os
from dateutil.tz import tzlocal
from dateutil import parser
from dotenv import load_dotenv

def calc_url(request):
   load_dotenv()
   dev_id = os.getenv("PTV_DEV_ID")
   key = os.getenv("PTV_DEV_KEY")
   base_url = "http://timetableapi.ptv.vic.gov.au"

   request_with_dev_id = request + "?devid=" + str(dev_id)

   key_bytes = key.encode()
   request_url_bytes = request_with_dev_id.encode()

   hashed = hmac.new(key_bytes, request_url_bytes, sha1)

   signature = hashed.hexdigest()

   full_url = base_url + request_with_dev_id + "&signature=" + signature
   return full_url

def get_json(input_string):
   return requests.get(calc_url(input_string)).json()

def local_tz(raw_string):
   if raw_string is not None:
      utc = parser.parse(raw_string[:-1] + " UTC")
      return utc.astimezone(tzlocal())

def save_json(var_name, file_name):
   string = json.dumps(var_name, indent= 4)
   with open({file_name}, "w") as outfile:
      outfile.write(string)

def get_all_route_types():
   return get_json("/v3/route_types")

def get_all_routes():
   return get_json("/v3/routes")

def get_all_stops(route_id, route_type):
   return get_json(f"/v3/stops/route/{route_id}/route_type/{route_type}")

def get_departures(route_type, stop_id):
   return get_json(f"/v3/departures/route_type/{route_type}/stop/{stop_id}")

def get_directions(route_id):
   return get_json(f"/v3/directions/route/{route_id}")

def get_direction_name(route_id, direction_id):
   directions = get_directions(route_id)["directions"]
   for direction in directions:
      if direction["direction_id"] == direction_id:
         return direction["direction_name"]

def print_all_route_types():
   for route_type in get_all_route_types()["route_types"]:
      print(f"\tName: {route_type['route_type_name']}  Number: {route_type['route_type']}")

def print_all_routes(route_type):
   all_routes = get_all_routes()
   for route in all_routes["routes"]:
      if route["route_type"] == route_type:
         print(f"\tRoute Number: {route['route_number']} - {route['route_name']}  | Route ID: {route['route_id']}")

def print_all_stops(route_id, route_type):
   for stop in get_all_stops(route_id,route_type)["stops"]:
      print(f'\tStop ID: {stop["stop_id"]}  -  {stop["stop_name"]}')

def print_next_depatures(route_type, stop_id):
   for depature in get_departures(route_type, stop_id)["departures"][:5]:
      direction = get_direction_name(depature["route_id"],depature["direction_id"])
      print(f"\tDirection: {direction:15} \tScheduled: {local_tz(depature['scheduled_departure_utc'])}")
      print(f"\t\t\t\t\tEstimated: {local_tz(depature['estimated_departure_utc'])}\n")



# print(get_directions(1002))



# utc = datetime.strptime("2023-03-16T18:11:00Z", "%Y-%m-%dT%H:%M:%SZ")
# timezone = pytz.timezone("UTC")
# with_timezone = timezone.localize(utc)

# utc = "2023-03-16T14:52:00Z"
# print(utc)
# print(local_tz(utc))



# print_all_stops(1002,1)
# print_all_routes(1)
# print_next_depatures(1,2361)
# print_all_route_types()

key = ""
while key != "q":
   print()
   print("-"*30)
   print("Menu: ")
   print("  a - Print all route types")
   print("  b - Print all routes")
   print("  c - Print all stops")
   print("  d - Print next 5 depatures")
   print()
   print("  q - Exit")
   print()
   key = input("Select an option: ")
   print("-"*30)

   if key == "a":
      print("\nPrinting all route types:\n")
      print_all_route_types()
   elif key == "b":
      print()
      route_type = int(input("Enter a route type eg. '1' for Trams: "))
      print("\nPrinting all routes\n")
      print_all_routes(route_type)
   elif key == "c":
      print()
      route_type = int(input("Enter a route type eg. '1' for Trams: "))
      route_id = int(input("Enter a route id: "))
      print("\nPrinting all stops:\n")
      print_all_stops(route_id, route_type)
   elif key == "d":
      print()
      route_type = int(input("Enter a route type eg. '1' for Trams: "))
      stop_id = int(input("Enter a stop ID: "))
      print("\nPrinting next 5 depatures:\n")
      print_next_depatures(route_type, stop_id)

