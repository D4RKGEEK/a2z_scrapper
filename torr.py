from time import sleep
import os
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import glob
import zipfile
import json
from google_play_scraper import app
from slugify import slugify
import requests
import telepot
from telepot.loop import MessageLoop
import os
from torf import Torrent
from distutils.dir_util import copy_tree

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import shutil
from PIL import Image
from io import BytesIO
import undetected_chromedriver as uc

chat_id = 697046197
BOT_TOKEN = '6094110235:AAFtv9xohmShh3m34jP7VVCZAfFyQLLSCno'
bot = telepot.Bot(BOT_TOKEN)

status_check = None

session = requests.Session()


# Function to capture a screenshot and send it to Telegram, returning True or False based on user selection
def capture_screenshot_and_send(chat_id, link, name):
    global status_check
    driver.save_screenshot('screenshot.png')
    img = Image.open('screenshot.png')
    bio = BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)
    bot.sendPhoto(chat_id, photo=bio, caption=f'{name} \n {link}',
                  reply_markup={'keyboard': [['✔️', '❌']], 'one_time_keyboard': True})
    status_check = None
    while status_check is None:
        pass

    return status_check


def check_app(app_name):
    layout = [
        [sg.Text(f"Do you want to upload to torrent? {app_name}?")],
        [sg.Button("Yes"), sg.Button("No")]
    ]

    window = sg.Window("Upload Confirmation", layout)

    while True:
        event, _ = window.read()

        if event in (sg.WINDOW_CLOSED, "No"):
            return False
        elif event == "Yes":
            return True


def confirm_check(app_name):
    layout = [
        [sg.Text(f"Do you want to continue {app_name}?")],
        [sg.Button("Yes"), sg.Button("No")]
    ]

    window = sg.Window("Upload Confirmation", layout)

    while True:
        event, _ = window.read()

        if event in (sg.WINDOW_CLOSED, "No"):
            return False
        elif event == "Yes":
            return True


def credit_giver():
    src_file = "Downloaded From APKISM.COM.txt"
    src_url = "Download More Modded APKs From APKISM.com.url"

    for root, dirs, files in os.walk("."):
        if not dirs:  # skip if no folder
            continue
        for dir in dirs:
            dst = os.path.join(root, dir)
            shutil.copy(src_file, dst)
            shutil.copy(src_url, dst)


# def torr_maker(folder_name):
#    os.system(
#        f"py3createtorrent -t udp://open.stealth.si:80/announce -t udp://exodus.desync.com:6969/announce -t udp://tracker.cyberia.is:6969/announce -t udp://tracker.opentrackr.org:1337/announce -t udp://tracker.torrent.eu.org:451/announce -t udp://explodie.org:6969/announce -t udp://tracker.birkenwald.de:6969/announce -t udp://tracker.moeking.me:6969/announce -t udp://ipv4.tracker.harry.lu:80/announce -t udp://9.rarbg.me:2970/announce {folder_name}")


def torr_maker(path):
    f_name = os.path.dirname(path)
    filename = os.path.splitext(os.path.basename(f_name))
    final_folder_name = os.path.basename(f_name)
    t = Torrent(path=f'{f_name}',
                trackers=[
                    'udp://tracker.openbittorrent.com:80/announce',
                    'udp://tracker.opentrackr.org:1337/announce',
                    'udp://tracker.pirateparty.gr:6969/announce',
                    'udp://tracker.tiny-vps.com:6969/announce',
                    'udp://tracker.torrent.eu.org:451/announce',
                    'udp://explodie.org:6969/announce',
                    'udp://ipv4.tracker.harry.lu:80/announce',
                    'udp://open.stealth.si:80/announce',
                    'udp://tracker.coppersurfer.tk:6969/announce',
                    'udp://tracker.cyberia.is:6969/announce',
                    'udp://tracker.internetwarriors.net:1337/announce',
                    'udp://tracker.open-internet.nl:6969/announce'
                ],
                comment='Uploaded By APKISM.CoM')
    t.private = True
    try:
        shutil.copytree(f_name, f"X:/APKISM/torrs/{final_folder_name}")
    except FileExistsError:
        print("Skipping the copy operation.")
    t.generate()
    t.write(f'X:/APKISM/torrs_files/{filename}.torrent')
    return True, f"X:/APKISM/torrs_files/{filename}.torrent", f"{filename}.torrent"


def new_glo(desc1, torr_filename, torr_path, name, torr_title, image):
    import requests
    from bs4 import BeautifulSoup

    url = "https://glodls.to/login.php"
    upload_url = 'https://glodls.to/upload'
    session = requests.Session()

    payload = 'password=shifts323212&sign-in-submit=&username=geekyapk'

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
        'host': 'glodls.to'
    }

    response = session.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        headers = {
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryefIwRKqVTe9X3NF3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'host': 'glodls.to'
        }
        files = [
            ('torrent', (f'{torr_filename}.torrent',
                         open(torr_path,
                              'rb'), 'application/json'))
        ]
        form_data = {'descr': f'{desc1}', 'imdb': '', 'lang': '1', 'name': f'{torr_title}', 'nfo': '',
                     'takeupload': 'yes', 'tube': '',
                     'type': '5'}

        response = session.post(upload_url, data=form_data, files=files)
        html = BeautifulSoup(response.text, 'html.parser')
        elements = html.select('.myBlock-con')
        print(elements[-1].get_text())
        return True


def new_tgx(desp1, torr_filename, torr_path, name, torr_title, image2):
    url = "https://torrentgalaxy.to/account-login.php"
    upload_url = "https://torrentgalaxy.to/torrents-upload.php"
    payload = 'password=Shifts323212%40%40&username=apkshadow'
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
        'host': 'torrentgalaxy.to'
    }

    response = session.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        # Set the file to upload
        headers = {
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryCg0ABXm144GDqNGx',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'host': 'torrentgalaxy.to'
        }
        files = [
            ('torrent', (f'{torr_filename}.torrent',
                         open(torr_path,
                              'rb'), 'application/json'))
        ]

        form_data = {'coverpicurl': f'{image2}', 'descr': f'{desp1}', 'upload': 'Upload', 'lang': '1', 'type': '20',
                     'name': f'{torr_title}', 'takeupload': 'yes'}
        response = session.post(upload_url, data=form_data, files=files)
        html = BeautifulSoup(response.text, 'html.parser')
        div_tag = html.find("div", {"class": "panel-body slidingDivf-0a9b5f23e3e308126930b9afffcad40b5017a94e"})
        if div_tag is not None:
            div_tag = div_tag.text
            print(div_tag.strip())
            return True
        else:
            return False
            print(f"Uploaded : {torr_title}")


def new_leet(desc, filename, path, name, torr_title):
    login_url = 'https://1337x.to/login'
    upload_url = 'https://1337x.to/upload'

    payload = {'username': 'geekyapk', 'password': 'Shifts323212@'}
    session = requests.Session()

    # Send a POST request to the login page with the login credentials
    response = session.post(login_url, data=payload)
    if response.status_code == 200:
        # Set the file to upload
        headers = {
            'host': '1337x.to',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1'
        }

        files = [
            ('torrent_file', (f'{filename}.torrent',
                              open(path,
                                   'rb'), 'application/json'))
        ]
        all_words = name.split()
        tag = all_words[0]
        # Send a POST request to the upload page with the file and form data using the same session as the login request
        form_data = {'category': 'Apps', 'description': f'{desc}', 'upload': 'Upload', 'language': '1',
                     'type': '56', 'title': f'{torr_title}', 'tags': f'{tag}:MOD'}
        response = session.post(upload_url, data=form_data, files=files)
        html = BeautifulSoup(response.text, 'html.parser')
        element = html.select_one('.box-info-detail.no-top-radius')

        # Print the text of the element
        print(element.get_text().strip())
        return True
    else:
        print("Login failed.")
        return False


# Function to handle user messages
def handle_message(msg):
    global status_check
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        command = msg['text']
        if status_check is None:
            # User hasn't made a selection yet
            if command == '✔️':
                status_check = True
                print('User selected ✔️ (OK)')
            elif command == '❌':
                status_check = False
                print('User selected ❌ (Not OK)')
            else:
                # User replied with an invalid command, ignore it
                pass
        else:
            if command == '✔️' or command == '❌':
                status_check = None  # Reset status_check when user responds with tick or wrong
                print('User responded with tick or wrong. Resetting status_check to None.')
            else:
                pass


if __name__ == '__main__':
    MessageLoop(bot, handle_message).run_as_thread()
    driver = uc.Chrome(headless=False, version_main=109)
    current_month = datetime.now().strftime('%B')
    db_folder = 'DB'
    month_folder = os.path.join(db_folder, current_month)
    day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))
    print(day_folder)
    if os.path.exists(day_folder):
        json_files = [f for f in os.listdir(day_folder) if f.endswith('.json')]
        if json_files:
            for json_filename in json_files:
                json_path = os.path.join(day_folder, json_filename)
                print(json_path)
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
                    if not data["scan_vt"]:
                        continue
                    if not data["torr"]:
                        app_name = data["title"]
                        vt_link = data["scan_vt"]
                        hybrid = data["scan_hybrid"]
                        final_link = False
                        if hybrid is None:
                            driver.get(vt_link)
                            sleep(2)
                            final_link = capture_screenshot_and_send("697046197", vt_link, app_name)
                            print(final_link)
                        if hybrid is not None:
                            driver.get(vt_link)
                            sleep(2)
                            vt_status = capture_screenshot_and_send("697046197", vt_link, app_name)
                            print(vt_status)
                            if vt_status is True:
                                if hybrid is not None:
                                    driver.get(hybrid)
                                    sleep(2)
                                    hybrid_status = capture_screenshot_and_send("697046197", hybrid, app_name)
                                if hybrid is None:
                                    hybird_status = True

                        if final_link or vt_status and hybrid_status is True:
                            scrap_content = data["scrap_content"]
                            if str(scrap_content).startswith("http"):
                                temp = scrap_content.split("=")[1].split("&")[0]
                                result = app(
                                    temp,
                                    lang='en',
                                    country='us'
                                )
                                image = result["icon"]
                                cat = result['genre']
                                dev = result["developer"]
                                summary = data["overview"]
                                wpnew = "Bug Fixes"
                                name = data["app_name"]
                                mod1 = data["mod_info"]
                                mod2 = data["app_mod"]
                                mod = str(mod1) + "\n" + str(mod2)


                            elif str(data.get("img", "")).startswith("http"):
                                image = data["img"]
                                cat = "Third Party MODs"
                                dev = "Unknown"
                                summary = data["overview"]
                                wpnew = "Bug Fixes"
                                name = data["app_name"]
                                mod1 = data["mod_info"]
                                mod2 = data["app_mod"]
                                mod = str(mod1) + "\n" + str(mod2)

                            else:
                                img2, img2_url = search_image(app_name + "MOD APK")
                                image = img2_url
                                cat = "Third Party MODs"
                                dev = "Unknown"
                                summary = data["overview"]
                                wpnew = "Bug Fixes"
                                name = data["app_name"]
                                mod1 = data["mod_info"]
                                mod2 = data["app_mod"]
                                mod1 = str(mod)
                                mod = str(mod1) + "\n" + str(mod2)

                            slug = data["slug"]
                            size = data["apk_size"]
                            version = data["app_version"]

                            if status_check is True:
                                torr_title = data["title"] + " [APKISM]"
                                first = f"[center][b]Torrent Source: [/b][url=https://apkism.com/{slug}]https://apkism.com/{slug}[/url] [/center]\n\n[center][img]https://i.ibb.co/y6km7jr/apkism-2-300x100.png[/img][/center]\n"  # [b]Visit For More MOD APKs[/b][url=https://apkism.com/]APKISM.com[/url][/center]
                                telegram = "\n[center][b]Telegram:[/b][url=https://t.me/apkism_main]Click Here[/url][/center]\n\n"
                                second = f"[img]{image}[/img]\n [b]Name : {app_name} \n [b]Size : {size}MB [/b] \n [b]Version : {version} [/b]\n [b]Category : {cat} [/b] \n [b]Developer : {dev}[/b] \n [b]Mod : {mod}[/b] \n \nThis app has no advertisment. \n\n [b]{name} Info : {summary} \n\n [b]{name} What's New : {wpnew}\n\n"
                                third = f" How To Install?. [/b] [Please Check Website For Games With OBB Files]\n\n[b] Step 1. [/b] Like any additional APK file you sideload this, and you can start doing that by first Downloading {name} Torrent APK file.\n\n[b]Step 2.[/b] Next, go to your File Explorer and browse {name} MOD APK file.\n\n[b]Step 3.[/b] Once you locate the {name} APK file, tap on it, and hit the install button.\n\n[b]Step 4.[/b] It will start installing, and once done, open {name}.\n\n[b]Step 5.[/b] This will be PreMODDED It will ask you for an account, enter the correct details (if asked).\n\n[b]Step 6.[/b] And that’s it you’re done, all the {mod} features will be available for you.\n\n[b]NOTE:[/b] if you faced any error like app not install then please uninstall the previously installed app and then you can easily install the MOD on your device.\n\n[b][color=red]EVERY MOD EXPIRES AFTER A TIME SO IF THE MOD ISN'T WORKING PLEASE WAIT FOR NEW RELESE AND FEEL FREE TO DROP ME A PM FOR ANY HELP.[/color][/b]"
                                desc = first + telegram + second + third + "\n\nHybrid Analysis : " + hybrid + "\n\n VirusTotal Analysis : " + vt_link
                                second1 = f"Name : {name} \n [b]Size : {size}MB [/b] \n [b]Version : {version} [/b]\n \n [b]Mod : {app}[/b] \n \nThis app has no advertisment. \n\n [b]{name} Info : {summary} \n\n [b]{name} What's New : {wpnew}\n\n"
                                desc1 = first + telegram + second1 + third + "\n\nHybrid Analysis : " + hybrid + "\n\n VirusTotal Analysis : " + vt_link
                                folder = data["apk_path"]
                                name = data["app_name"]
                                torr_status, torr_path, torr_filename, = torr_maker(folder)
                                if torr_status is True:
                                    ok1 = new_leet(desc, torr_filename, torr_path, name, torr_title)
                                    ok2 = new_tgx(desc1, torr_filename, torr_path, name, torr_title, image)
                                    ok3 = new_glo(desc1, torr_filename, torr_path, name, torr_title, image)
                                    if ok1 and ok2 and ok3:
                                        data["torr"] = True
                                        with open(json_path, 'w') as updated_json_file:
                                            json.dump(data, updated_json_file, indent=4)
                    else:
                        print("delte")
