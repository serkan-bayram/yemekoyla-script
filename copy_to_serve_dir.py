import os
import shutil
from datetime import datetime
import time

def copy():
    # Specify the source folder where your date folders are located
    source_folder = './data'

    # Get a list of all the folders in the source folder
    date_folders = [folder for folder in os.listdir(
        source_folder) if os.path.isdir(os.path.join(source_folder, folder))]

    # Convert date folders to datetime objects
    date_folders = [datetime.strptime(folder, "%d-%m-%Y") for folder in date_folders]

    # Sort the date folders in reverse order (latest date first)
    date_folders.sort(reverse=True)

    if date_folders:
        # Get the latest date folder
        latest_date_folder = date_folders[0].strftime("%d-%m-%Y")

        # Create the full source path to the latest date folder
        latest_date_folder_path = os.path.join(
            source_folder, latest_date_folder)

        # Specify the destination folder
        destination_folder = '/var/www/html'

        shutil.rmtree(destination_folder, ignore_errors=True)
        time.sleep(2)
        os.mkdir(destination_folder)

        # Copy the contents of the latest date folder to the destination folder
        for item in os.listdir(latest_date_folder_path):
            source_item = os.path.join(latest_date_folder_path, item)
            destination_item = os.path.join(destination_folder, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, destination_item)
            elif os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
        print(
            f'Copied contents of {latest_date_folder} to {destination_folder}')
    else:
        print('No date folders found in the source folder.')
