import json
import os
from datetime import datetime
import requests
from bypass import uploadrar_direct
import urllib.parse

from selenium import webdriver
from datetime import datetime
import os
import json
import requests
import hashlib


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, 'rb') as file:
        # Read the file in chunks to avoid memory issues
        chunk_size = 4096
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            sha256_hash.update(data)

    return sha256_hash.hexdigest()


def virus_total(file_name):
    url = "https://www.virustotal.com/api/v3/files/upload_url"

    headers = {
        "accept": "application/json",
        "x-apikey": "36572865f9503122aba76d71a98d73be5aab704f0f598460473b4b40110515a7"
    }

    response = requests.get(url, headers=headers)
    upload_url = response.text
    upload_url = json.loads(upload_url)
    upload_url = upload_url['data']

    files = {"file": (file_name, open(f"{file_name}", "rb"), "application/octet-stream")}

    headers = {
        "accept": "application/json",
        "x-apikey": "36572865f9503122aba76d71a98d73be5aab704f0f598460473b4b40110515a7",
    }

    response = requests.post(upload_url, files=files, headers=headers)

    an_id = response.text
    json_obj = json.loads(an_id)
    id_value = json_obj['data']['id']
    url = "https://www.virustotal.com/api/v3/analyses/" + id_value
    sha256 = None
    retry_count = 0
    max_retries = 3  # You can adjust the maximum number of retries
    while retry_count < max_retries:
        response = requests.get(url, headers=headers)
        json_data = response.text
        parsed_json = json.loads(json_data)
        if "sha256" in parsed_json.get("meta", {}).get("file_info", {}):
            sha256 = parsed_json["meta"]["file_info"]["sha256"]
            break
        retry_count += 1
    if sha256:
        requests.get("https://www.virustotal.com/gui/file/" + sha256)
        url = "https://www.virustotal.com/gui/file/" + sha256
        requests.get(url, verify=False)
        return url
    elif file_name:
        sha256_hash = calculate_sha256(file_name)
        url = "https://www.virustotal.com/gui/file/" + sha256_hash
        return url
    else:
        return None


def hybrid_analysis(file_name):
    file_size = os.path.getsize(file_name)
    if file_size > 100000000:
        return None
    else:
        headers = {
            'accept': 'application/json',
            'user-agent': 'Falcon Sandbox',
            'api-key': 'xfrz86605bc99189aag4t6bx039b7875guud6fmg1bf11804bvf9htkafd8cc69a',
            # requests won't add a boundary if this header is set when you pass files=
            # 'Content-Type': 'multipart/form-data',
        }

        files = {
            'file': open(f'{file_name}', 'rb'),
            'environment_id': (None, '160'),
        }

        response = requests.post('https://www.hybrid-analysis.com/api/v2/submit/file', headers=headers, files=files)
        an_id = response.text
        json_obj = json.loads(an_id)
        id_value = json_obj['sha256']
        url = "http://hybrid-analysis.com/sample/" + id_value
        if url:
            return url
        else:
            return None


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
                        try:
                            link = data["dl_link_final"]
                            link = uploadrar_direct(link)
                            base_file_name = os.path.basename(link)
                            link = requests.utils.requote_uri(link)
                            if "uploadrar" in link:
                                folder_name = data["app_name"] + " " + data["app_version"] + " Premium MOD Apk [APKISM.COM]"
                                status = download_file(folder_name, link, base_file_name)
                                if status is True:
                                    data["apk_path"] = os.path.join(os.getcwd(), day_folder, folder_name,
                                                                    base_file_name)
                                    with open(json_path, 'w') as updated_json_file:
                                        json.dump(data, updated_json_file, indent=4)
                                else:
                                    link = data["dl_links"]
                                    folder_name = data["app_name"] + " " + data[
                                        "app_version"] + " Premium MOD Apk [APKISM.COM]"
                                    status = download_file(folder_name, link, base_file_name)
                                    if status is True:
                                        data["apk_path"] = os.path.join(os.getcwd(), day_folder, folder_name,
                                                                        base_file_name)
                                        with open(json_path, 'w') as updated_json_file:
                                            json.dump(data, updated_json_file, indent=4)
                        except Exception as e:
                            print(e)
                            continue


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
                    apk_path = data["apk_path"]
                    vt_link = data["scan_vt"]
                    if vt_link is not None:
                        if "virustotal" in vt_link:
                            print("vt")
                            vt_link = vt_link
                            hybrid_link = hybrid_analysis(apk_path)
                            if vt_link is not None:
                                vt_link = vt_link
                            if hybrid_link is not None:
                                hybrid_link = hybrid_link
                                print(hybrid_link)
                            else:
                                hybrid_link = None
                    else:
                        vt_link = virus_total(apk_path)
                        hybrid_link = hybrid_analysis(apk_path)
                        if vt_link is not None:
                            vt_link = vt_link
                        if hybrid_link is not None:
                            hybrid_link = hybrid_link
                        else:
                            hybrid_link = None
                    if vt_link and hybrid_link is not None:
                        data["scan_vt"] = vt_link
                        data["scan_hybrid"] = hybrid_link
                        data["vt_status"] = True
                        data["hybird_status"] = True
                        with open(json_path, 'w') as updated_json_file:
                            json.dump(data, updated_json_file, indent=4)
                    else:
                        continue


