import shutil
import os

def create_folder_and_upload(local_file_path1):
        source_folder = f'../insiff/{local_file_path1}'
        destination_folder = '../../var/www/atlanta-api.online/scripts'
        if not os.path.exists(destination_folder+f"/{local_file_path1}"):
            shutil.move(source_folder, destination_folder)
            print(f"Successfully uploaded {local_file_path1} to {destination_folder}")
        else:
              print(f"Already {local_file_path1}")


