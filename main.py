import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import wget
import os
import time
from copy_to_serve_dir import copy
from save_to_db import send_request
import shutil


BASE_URL = "https://bilecik.edu.tr/sks/Icerik/Yemek_Men%C3%BCs%C3%BC_cc6e6"
RECORD_DATA_DIR = "data"
CONTAINER = None
wait_for = 300
tz = pytz.timezone("Europe/Istanbul")

if(wait_for < 300):
    print(f"\nBE CAREFUL wait_for value is {wait_for}\n")

# Get today's date
def get_todays_date():
    # Get the current time in the specified timezone
    current_time = datetime.datetime.now(tz)

    # Format the date as "dd.mm.yyyy"
    formatted_date = current_time.strftime("%d-%m-%Y")

    return formatted_date

def get_current_hour():
    current_time = datetime.datetime.now(tz)

    return current_time.hour


# Downloads menu
def download_menu(date):
    path = f"./data/{date}/{date}.jpeg"

    url = get_menu_url()

    filename = wget.download(url, path)


# Container holds the current values from site, like photo url food list etc
def get_menu_container():
    global CONTAINER

    r = requests.get(BASE_URL)

    soup = BeautifulSoup(r.content, 'html.parser')

    CONTAINER = soup.find("div", {"class": "icerik-govde"})


def get_menu_url():
    menu_url = CONTAINER.find("img")["src"]

    return menu_url


def get_menu_date():
    menu_date = CONTAINER.find_all("p")[1].getText()

    formatted_date = menu_date.replace(".", "-")

    return formatted_date


def get_foods(date):
    food_list = CONTAINER.find_all("p")[2:-2]

    foods = ""

    foods_array = []

    for food in food_list:
        foods_array.append(food.getText().strip())
        foods += food.getText() + "\n\n"

    with open(f"./data/{date}/menu.txt", "w") as f:
        f.write(foods.strip())

    return foods_array


# Creates the data directory
def create_data_directory():
    os.mkdir("data")

# Creates a directory with school's menu date


def create_date_dir(date):
    os.mkdir(f"data/{date}")

# Returns true if we save today's menu


def did_we_save(date):
    if is_txt_saved(date) and is_photo_saved(date):
        return True
    return False


def is_txt_saved(date):
    if os.path.exists(f"./data/{date}/menu.txt"):
        return True
    return False


def is_photo_saved(date):
    if os.path.exists(f"./data/{date}/{date}.jpeg"):
        return True
    return False


def remove_todays_menu_data(date):
    shutil.rmtree(f"./data/{date}", ignore_errors=True)

def main():
    print("Bot is started.")

    while True:
        print("Bot is running.")

        # Create data directory if not exist
        if not os.path.exists(f"./{RECORD_DATA_DIR}"):
            create_data_directory()

        try:

            # Keep the container updated
            get_menu_container()

            # Even though there are not files with today's date,
            # url's food date will return a outdated date, we don't want to save data every time we make a request
            # so we will make a double check and if there are files exist with url's food date
            # we won't save anything
            menu_date = get_menu_date()

            remove_todays_menu_data(menu_date)
            # shutil may not work when a file is tried to add at the same time while removing the folder
            # so we wait a bit
            time.sleep(2)

            if not os.path.exists(f"./data/{menu_date}"):
                create_date_dir(menu_date)

            try:
                download_menu(menu_date)
            except Exception as e:
                print(f"Fotoğraf indirilemedi.\nHata: {e}")

            try:
                get_foods(menu_date)
            except Exception as e:
                print(f"Menü listesi indirilemedi.\nHata: {e}")

            print("\nVeriler güncellendi!\n")

            if did_we_save(menu_date):
                copy()
                send_request(get_foods(menu_date), menu_date)

        except Exception as e:
            print("Huge error: ", e)
        
        time.sleep(wait_for)



main()
