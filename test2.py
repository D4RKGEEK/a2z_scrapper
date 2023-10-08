import json
import os
from datetime import datetime
import requests
from bypass import uploadrar_direct
import urllib.parse


def download_file(folder, url, base_file_name):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            current_month = datetime.now().strftime('%B')
            db_folder = 'DB'
            month_folder = os.path.join(db_folder, current_month)
            day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))
            sub_folder = os.path.join(day_folder, folder)
            os.makedirs(sub_folder, exist_ok=True)
            filename = os.path.join(sub_folder, base_file_name)


            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def apk_downloader():
    current_month = datetime.now().strftime('%B')
    db_folder = 'DB'
    month_folder = os.path.join(db_folder, current_month)
    day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))
    if os.path.exists(day_folder):
        json_files = [f for f in os.listdir(day_folder) if f.endswith('.json')]
        if json_files:
            for json_filename in json_files:
                json_path = os.path.join(day_folder, json_filename)
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
                    if not data["torr"]:
                        link = data["dl_link_final"]
                        link = uploadrar_direct(link)
                        base_file_name = os.path.basename(link)
                        link = requests.utils.requote_uri(link)
                        if "uploadrar" in link:
                            folder_name = data["app_name"] + " " + data["app_version"] + " Premium MOD Apk [APKISM.COM]"
                            status = download_file(folder_name, link, base_file_name)
                            if status is True:
                                data["apk_path"] = os.path.join(os.getcwd(), day_folder, folder_name,
                                                                os.path.basename(link))
                                with open(json_path, 'w') as updated_json_file:
                                    json.dump(data, updated_json_file, indent=4)
                            else:
                                link = data["dl_links"]
                                older_name = data["app_name"] + " " + data[
                                    "app_version"] + " Premium MOD Apk [APKISM.COM]"
                                status = download_file(folder_name, link, base_file_name)
                                if status is True:
                                    data["apk_path"] = os.path.join(os.getcwd(), day_folder, folder_name,
                                                                    os.path.basename(link))
                                    with open(json_path, 'w') as updated_json_file:
                                        json.dump(data, updated_json_file, indent=4)


def apk_scanner():
    current_month = datetime.now().strftime('%B')
    db_folder = 'DB'
    month_folder = os.path.join(db_folder, current_month)
    day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))
    if os.path.exists(day_folder):
        json_files = [f for f in os.listdir(day_folder) if f.endswith('.json')]
        if json_files:
            vt_link = None
            hybrid_link = None
            for json_filename in json_files:
                json_path = os.path.join(day_folder, json_filename)
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
                    print(data["title"])
                    apk_path = data["apk_path"]
                    vt_link = virus_total(apk_path)
                    hybrid_link = hybrid_analysis(apk_path)
                    if vt_link is not None:
                        vt_link = vt_link
                    if hybrid_link is not None:
                        hybrid_link = hybrid_link
                    else:
                        hybrid_link = None
                    print(vt_link, hybrid_link)
                    if vt_link and hybrid_link is not None:
                        data["scan_vt"] = vt_link
                        data["scan_hybrid"] = hybrid_link
                        data["vt_status"] = True
                        data["hybird_status"] = True
                        with open(json_path, 'w') as updated_json_file:
                            json.dump(data, updated_json_file, indent=4)
                    else:
                        continue
apk_downloader()
