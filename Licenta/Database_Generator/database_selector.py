import os, random, json

price_decimals = 2
def get_food_price():
  # Give different probabilities for different price ranges.
  price_range = random.randint(1,20)
  if (1 <= price_range and price_range <= 4):
    return round(random.uniform(0, 10), price_decimals)
  elif (5 <= price_range and price_range <= 12):
    return round(random.uniform(10, 25), price_decimals)
  elif (13 <= price_range and price_range <= 17):
    return round(random.uniform(25, 35), price_decimals)
  elif (18 <= price_range and price_range <= 20):
    return round(random.uniform(35, 50), price_decimals)

def get_drink_price():
  # Give different probabilities for different price ranges.
  price_range = random.randint(1,20)
  if (1 <= price_range and price_range <= 4):
    return round(random.uniform(0, 5), price_decimals)
  elif (5 <= price_range and price_range <= 12):
    return round(random.uniform(5, 8), price_decimals)
  elif (13 <= price_range and price_range <= 17):
    return round(random.uniform(8, 12), price_decimals)
  elif (18 <= price_range and price_range <= 20):
    return round(random.uniform(12, 25), price_decimals)

def create_food_dict():
  food_dict = dict()
  for line in open("food_database.txt", "r").readlines():
    # Remove new line from the end.
    line = line.rstrip()
    # Set a desired max length.
    maxLenght = len("Half tomato and mozzarella on ciabatta by Panera bread")
    # Add the new food name and price in dictionary.
    food_dict[line[:maxLenght]] = get_food_price()
  return food_dict

import re

def extract_food_from_html():
  foods = dict()
  food_pattern = re.compile("title=\"Cookbook:(.*?)\"")
  for line in open("cookbook.txt", "r", encoding="utf-8").readlines():
    for match in re.findall(food_pattern, line):
      foods[match] = get_food_price()
  myJson = json.dumps(foods)
  open("json_food2_db.json", "w").write(myJson)  

def extract_drinks_from_html():
  drinks = dict()

  drink1_pattern = re.compile("<dl><dt>(.*?)</dt>")
  drink2_pattern = re.compile("<h3><span class=\"mw-headline\" id=\"(.*?)\">")
  link_pattern = re.compile("<a.*?>(.*?)</a>")

  for line in open("cocktails.txt", "r").readlines():
    for match in re.findall(drink1_pattern, line):
      new_match = re.match(link_pattern, match)
      if new_match:
        match = new_match
      drinks[match] = get_drink_price()
    for match in re.findall(drink2_pattern, line):
      new_match = re.match(link_pattern, match)
      if new_match:
        match = new_match
      drinks[match] = get_drink_price()
  myJson = json.dumps(drinks)
  open("json_drinks_db.json", "w").write(myJson)
  return drinks

def merge_jsons():
  drinks = open("json_drinks_db.json", "r").read()
  drinks = json.loads(drinks)

  food1 = open("json_food_db.json", "r").read()
  food1 = json.loads(food1)

  food2 = open("json_food2_db.json", "r").read()
  food2 = json.loads(food2)

  menu_list = dict()
  for (drink, price) in drinks.items():
    menu_list[drink] = price
  for (food, price) in food1.items():
    menu_list[food] = price
  for (food, price) in food2.items():
    menu_list[food] = price

  myJson = json.dumps(menu_list)
  open("menu_db.json", "w").write(myJson)

def change_prices_to_strings():
  json_content = open("menu_db.json", "r").read()
  json_dict = json.loads(json_content)
  for (name, price) in json_dict.items():
    json_dict[name] = str(price)
  json_content = json.dumps(json_dict)
  open("menu_db.json", "w").write(json_content)

