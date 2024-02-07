import shutil

def copy_data():

# Specify the source and destination paths
    source_folder = './data'
    destination_folder = '/var/www/files/data'

# Use shutil.copytree to copy the entire folder and its contents
    shutil.copytree(source_folder, destination_folder)

    print(f"Folder '{source_folder}' copied to '{destination_folder}'")

