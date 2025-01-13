import os
import gdown

url = 'https://drive.google.com/drive/folders/1ognnZYI9YbNlGth-CrFg1DxV133A1MrC?usp=sharing'
folder =os.path.join(os.getcwd(), 'models')
if not os.path.exists(folder):
    os.makedirs(folder)

folder_id = url.split('/')[-1]

gdown.download_folder(id=folder_id, output=folder, quiet=False, use_cookies=False)