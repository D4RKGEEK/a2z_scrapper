import os
import json
import re
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
import requests



def save_value_to_file(value):
    file_name = "last_post_id.txt"
    with open(file_name, "w") as file:
        file.write(str(value))


def get_post_id():
    file_name = "last_post_id.txt"
    try:
        with open(file_name, "r") as file:
            value = file.read()
            return int(value)
    except FileNotFoundError:
        return None


def extract_app_details(s):
    title = ''
    version = ''
    feature = ''
    words = s.split()
    for word in words:
        if word.startswith('v') and len(word) >= 2 and word[1].isdigit():
            version = word
        elif (word.startswith('[') and word.endswith(']')) or (word.startswith('(') and word.endswith(')')):
            feature = word[1:-1]
        else:
            if title:
                title += ' '
            title += word
    title = title.strip()
    return version, feature


def generate_meaningful_id(post_title):
    # Combine title and link to create a unique ID
    combined_string = f"{post_title}"

    # Convert the combined string to a numeric ID
    meaningful_id = 0
    for char in combined_string:
        meaningful_id = (meaningful_id * 31 + ord(char)) % (10 ** 9)

    return meaningful_id


def format_article(content, sentences_per_paragraph=4):
    # Split content into sentences
    sentences = sent_tokenize(content)

    # Group sentences into paragraphs
    paragraphs = []
    current_paragraph = []

    for sentence in sentences:
        if sentence.strip():
            current_paragraph.append(sentence)
            if len(current_paragraph) >= sentences_per_paragraph:
                paragraphs.append(current_paragraph)
                current_paragraph = []

    # Construct the formatted article
    formatted_article = ""
    for paragraph in paragraphs:
        paragraph_text = " ".join(paragraph)
        formatted_article += paragraph_text + "\n\n"

    return formatted_article



def store_links(post_title, img_link, post_link, requirements, overview, mod_info, dl_links, dl_link_final, apksize, scrap_content, vt_link, play_link,
     app_name, save_metadata=False):
    current_month = datetime.now().strftime('%B')
    db_folder = 'DB'
    month_folder = os.path.join(db_folder, current_month)
    day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))
    meaningful_id = generate_meaningful_id(app_name)
    app_version, app_mod = extract_app_details(post_title)
    metadata_json_path = os.path.join(db_folder, 'metadata.json')
    json_filename = f'{app_name}.json'
    data_to_save = {
        "id": meaningful_id,
        "play_store_id" : play_link,
        "title": post_title,
        "link": post_link,
        "requirements": requirements,
        "overview": overview,
        "mod_info": mod_info,
        "app_name": app_name,
        "img": img_link,
        "app_version": app_version,
        "app_mod": app_mod,
        "dl_links": dl_links,
        "dl_link_final": dl_link_final,
        "apk_size": apksize,
        "scrap_content": scrap_content,
        "status_tg": False,
        "published": False,
        "post_Id": None,
        "slug": None,
        "scan_vt": vt_link,
        "scan_hybrid": False,
        "torr": False
    }
    os.makedirs(day_folder, exist_ok=True)
    metadata = {}
    json_path = os.path.join(day_folder, json_filename)
    metadata_keys = metadata.keys()
    if save_metadata:
        new_metadata = {
            str(meaningful_id): {
                "app_version": app_version,
                "json_path": json_path
            }
        }
        metadata_json_path = os.path.join('DB', 'metadata.json')
        # Load existing metadata if the file exists
        if os.path.exists(metadata_json_path):
            with open(metadata_json_path, 'r') as metadata_json_file:
                existing_metadata = json.load(metadata_json_file)
        else:
            existing_metadata = {}

        # Update the existing metadata with the new information
        existing_metadata.update(new_metadata)

        # Save the updated metadata to the JSON file
        with open(metadata_json_path, 'w') as metadata_json_file:
            json.dump(existing_metadata, metadata_json_file, indent=4)

    with open(json_path, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=4)


def meta_check(post_title, app_name):
    current_month = datetime.now().strftime('%B')
    db_folder = 'DB'
    month_folder = os.path.join(db_folder, current_month)
    app_version, app_mod = extract_app_details(post_title)
    meaningful_id = generate_meaningful_id(app_name)
    metadata_json_path = os.path.join(db_folder, 'metadata.json')
    metadata = {}
    if os.path.exists(metadata_json_path):
        with open(metadata_json_path, 'r') as metadata_json_file:
            existing_metadata = json.load(metadata_json_file)
        metadata.update(existing_metadata)
    if str(meaningful_id) in metadata:
        if metadata[str(meaningful_id)]["app_version"] == app_version:
            return False
        if metadata[str(meaningful_id)]["app_version"] < app_version:
            json_path = metadata[str(meaningful_id)]["json_path"]
            with open(json_path, 'r') as json_path:
                json_data = json.load(json_path)
                post_id = json_data["post_Id"]
                save_value_to_file(post_id)
            return True
    else:
        return None


def non_play_content_parser(content):
    # Parse the content using Beautiful Soup
    soup = BeautifulSoup(content, 'html.parser')

    # Extract all the text within the soup
    all_text = soup.get_text()

    requirements_index = all_text.find('Requirements:')
    if requirements_index != -1:
        requirements_start = requirements_index + len('Requirements:')
        requirements = all_text[requirements_start:all_text.find('Overview:', requirements_start)].strip()
    else:
        requirements = None

    # Find the index of 'Overview:'
    overview_index = all_text.find('Overview:')
    if overview_index != -1:
        overview_start = overview_index + len('Overview:')
        overview_end = re.search(r'[.!?]', all_text[overview_start:]).start() + overview_start
        overview = all_text[overview_start:overview_end].strip()

        # The content after the overview
        rest_of_content = all_text[overview_end + 1:].strip()
    else:
        overview = None
        rest_of_content = None
    if overview and requirements and rest_of_content is not None:
        return overview, requirements, rest_of_content

    return None


def uploadrar_upload(link):
    s = requests.session()
    url = "https://uploadrar.com/"
    payload = 'login=geekyapk&op=login&password=shifts323212&rand=&redirect='
    headers = {
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'host': 'uploadrar.com'
    }
    response = s.post(url, headers=headers, data=payload)
    sess_id = s.cookies['xfss']
    upload_url = s.get("https://uploadrar.com/?op=upload_form")
    upload_url = upload_url.text
    soup = BeautifulSoup(upload_url, 'html.parser')
    form = soup.find(id='uploadurl')
    upload_url = form['action']
    payload = {'file_public': '0',
               'keepalive': '1',
               'link_pass': '',
               'sess_id': f'{sess_id}',
               'to_folder': '',
               'url_mass': f'{link}',
               'utype': 'prem'}
    files = [
    ]
    headers = {
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryA576cwbYL4WhcPIY',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': upload_url
    }
    response = s.post(upload_url, data=payload)
    data = response.text
    data = data.replace('# Keep-Alive\n', '')
    data = json.loads(data)
    element = data[0]
    file_code = element['file_code']

    dl_link = f"http://uploadrar.com/api/file/direct_link?key=10037rhsxg7w5j33zv3o8&file_code={file_code}"
    dl_link = s.get(dl_link)
    dl_link = dl_link.text
    data = json.loads(dl_link)
    dl_link = data['result']['url']
    file_name = os.path.basename(dl_link)
    if "-www.ReXdl.com" in file_name:
        file_name = file_name.replace("-www.ReXdl.com", "-APKISM.COM")
    if "_A2ZAPK.COM" in file_name:
        file_name = file_name.replace("_A2ZAPK.COM", "-APKISM.COM")
    if "-an1.com" in file_name:
        file_name = file_name.replace("-an1.com", "-APKISM.COM")
    if file_name:
        file_name = "[APKISM.COM] " + file_name
    rename = f"http://uploadrar.com/api/file/rename?key=10037rhsxg7w5j33zv3o8&file_code={file_code}&name={file_name}"
    s.get(rename)
    uploadrar_link = "http://uploadrar.com/" + file_code
    return uploadrar_link


