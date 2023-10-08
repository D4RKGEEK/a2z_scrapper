import requests
import sqlite3
from google_play_scraper import app
from distutils.version import LooseVersion
from datetime import date
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from slugify import slugify
from datetime import datetime
from datetime import date
from data import format_article, store_links, meta_check
import os, json
from data import non_play_content_parser
from data import *

current_date = datetime.now().strftime("%b, %d, %Y")


def parse_version(version_string):
    return tuple(map(int, version_string.split('.')))

def youtube_parser(url):
    reg_exp = r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*'
    match = re.match(reg_exp, url)
    return match.group(7) if match and len(match.group(7)) == 11 else False

def playstore_post(data, is_update=False, existing_post_id=None, non_play=True):
    meaningful_id = data["id"]
    post_title = data["title"]
    post_link = data["link"]
    requirements = data["requirements"]
    overview = data["overview"]
    mod_info = data["mod_info"]
    app_name = data["app_name"]
    app_version = data["app_version"]
    app_mod = data["app_mod"]
    dl_links = data["dl_link_final"]
    apksize = data["apk_size"]
    img_link = data["img"]
    scrap_content = data["scrap_content"]
    play_store_id = data["play_store_id"]

    if non_play:
        img2 = img_link
        img2 = requests.get(img2)
        name = app_name
        version = app_version
        mod = app_mod
        size = apksize
        mod_info = mod_info
        cat = "Third Party MODs"
        content = scrap_content
        wp_url = "https://apkism.com/xmlrpc.php"
        wp_username = "test"
        wp_password = "test"
        wp = Client(wp_url, wp_username, wp_password)
        post = WordPressPost()
        data = {
            'name': f'{name} + MOD APK.jpg',
            'type': 'image/jpeg',
            'bits': xmlrpc_client.Binary(img2.content),
        }
        response = wp.call(media.UploadFile(data))
        thumbnail_id = response['id']
        img_url = response['url']
        post.thumbnail = thumbnail_id
        post.title = name + " Mod APK " + version + " (" + mod + ") "
        title = post_title
        thumbnail_url = (response["url"])
        post.slug = slugify(name + " Mod APK")
        catergory = "3rd Party Mods"
        post.terms_names = {
            'post_tag': [name + " Mod"],
            'category': [f'{catergory}'],
        }

        cat_link = slugify(cat)
        desp = scrap_content
        post.content = f"""
                          <h1 style="text-align: center;">{title}</h1>

 <p style="text-align: center;"><strong>Download The Latest Apk Version of {name} MOD, A <a href="https://apkism.com/category/{cat_link}">{cat}</a> App For Android Device. This MOD Includes {mod} Features Unlocked. Download Yours Now!</strong></p>

<h2>What is {name} MOD APK?</h2>
{name} MOD APK is an unofficial app that provides modifications or enhancements to the normal {name} experience on Android devices. This MOD includes {mod} features unlocked, such as additional content, new levels, and premium features.

<h2>About {name}</h2>
{desp}

<h2>Features of {name} MOD APK</h2>

No Ads: Unlike the standard version, {name} MOD APK removes all commercial content, providing an uninterrupted experience.
More Features: Enjoy unlocked features and enhanced app experience.
{mod} Unlocked: Access premium features without any restrictions.


<h2>Download {name} MOD APK Latest Version</h2>
You can download the MOD APK file for {name} with all {mod} features unlocked from our website. This version allows you to access all the app's content without any subscription fees.

To install the MOD APK file, follow these steps:

Download the APK file from our website.
On your Android device, go to Settings > Security > Unknown Sources and enable installation from unknown sources.
Locate the downloaded APK file and tap on it to begin the installation.
Follow the prompts to complete the installation.
Once installed, launch {name} and log in with your account details.
<h2>How to Install {name} MOD APK on PC</h2>
To install {name} MOD APK on your Windows PC, follow these steps:

Download and install BlueStacks software from a trusted source.
Download {name} MOD APK from our website.
Install the APK file using BlueStacks by following the provided steps.
Once installed, you can enjoy {name} MOD APK on your PC.
<h2>Conclusion</h2>
If you're looking for an unlocked version of {name}, the {name} MOD APK is a great choice. It provides access to all the app's content without any restrictions and comes with bug fixes and performance improvements for a smooth experience. Download now and enjoy!
                                            """
        post.post_status = 'publish'
        post.custom_fields = []


        datos_download = {
            'option': 'links',
            'type': 'apk',
            '0': {
                'link': f'{dl_links}',
                'texto': 'Download MOD'
            },
            'direct-link': None,
            'direct-download': None
        }
        post.custom_fields.append({
            'key': 'datos_download',
            'value': datos_download
        })

        # app_info
        ##########################
        datos_informacion = {
            'app_status': None,  # new
            'descripcion': f'',
            'version': f'{app_version}',
            'tamano': f'{size}',
            'fecha_actualizacion': f'{current_date}',
            'last_update': None,
            'requerimientos': f'{requirements}',
            'consiguelo': f'{play_store_id}',
            'categoria_app': 'APPS',
            'os': 'ANDROID',
            'offer': {
                'amount': None,
                'currency': 'USD'
            },
            'novedades': f'<p>{mod} \n {mod_info}</p>'
        }

        post.custom_fields.append({
            'key': 'datos_informacion',
            'value': datos_informacion
        })


        if is_update:
            print(existing_post_id)
            post.id = wp.call(posts.EditPost(existing_post_id, post))
            return version, post.id, post.slug, img_link
        else:
            post.id = wp.call(posts.NewPost(post))
            print(post.id)
            return version, post.id, post.slug, img_link


    if str(play_store_id).startswith("http"):
        temp = play_store_id.split("=")[1].split("&")[0]
        result = app(
            temp,
            lang='en',
            country='us'
        )
        name = app_name
        version = app_version
        mod = app_mod
        size = apksize
        mod_info = mod_info
        desp = result["descriptionHTML"]
        rated = result["score"]
        install = result["installs"]
        cat = result["genre"]
        img = result["icon"] + "=s200-rw"
        playstore_link = result["url"]
        video = result["video"]
        screenshots = result["screenshots"]
        ss1 = screenshots[1]
        ss2 = screenshots[2]
        ss3 = screenshots[3]


        if video is not None:
            yt = youtube_parser(video)

        banner = result["headerImage"]
        dev = result["developer"]
        shortdesp = result["summary"]
        ratings = result["ratings"]
        ss = (result["screenshots"])
        catergory = result['genre']
        video = result['video']
        whatsnew = "Bug Fixes"
        cover = result['headerImage']
        icon = result['icon']
        ratings = result['ratings']
        installs = result['installs']
        play_id = result['appId']
        vote = result['score']

        wp_url = "https://apkism.com/xmlrpc.php"
        wp_username = "test"
        wp_password = "test"
        wp = Client(wp_url, wp_username, wp_password)
        post = WordPressPost()
        img2 = requests.get(result["icon"] + "=s200-rw")
        data = {
            'name': f'{name} + MOD APK.jpg',
            'type': 'image/jpeg',
            'bits': xmlrpc_client.Binary(img2.content),
        }
        response = wp.call(media.UploadFile(data))
        thumbnail_id = response['id']
        post.thumbnail = thumbnail_id
        post.title = name + " Mod APK " + version + " (" + mod + ") "
        title = post_title
        thumbnail_url = (response["url"])
        post.slug = slugify(name + " Mod APK")
        #
        post.terms_names = {
            'post_tag': [name + " Mod"],
            'category': [f'{catergory}'],
        }
        cat_link = slugify(cat)
        desp = scrap_content

        post.content = f"""
                                  <h1 style="text-align: center;">{title}</h1>

         <p style="text-align: center;"><strong>Download The Latest Apk Version of {name} MOD, A <a href="https://apkism.com/category/{cat_link}">{cat}</a> App For Android Device. This MOD Includes {mod} Features Unlocked. Download Yours Now!</strong></p>

        <h2>What is {name} MOD APK?</h2>
        {name} MOD APK is an unofficial app that provides modifications or enhancements to the normal {name} experience on Android devices. This MOD includes {mod} features unlocked, such as additional content, new levels, and premium features.

        <h2>About {name}</h2>
        {desp}

        <h2>Features of {name} MOD APK</h2>

        No Ads: Unlike the standard version, {name} MOD APK removes all commercial content, providing an uninterrupted experience.
        More Features: Enjoy unlocked features and enhanced app experience.
        {mod} Unlocked: Access premium features without any restrictions.


        <h2>Download {name} MOD APK Latest Version</h2>
        You can download the MOD APK file for {name} with all {mod} features unlocked from our website. This version allows you to access all the app's content without any subscription fees.

        To install the MOD APK file, follow these steps:

   <ol>
        <li>Download the APK file from our website.</li>
        <li>On your Android device, go to Settings &gt; Security &gt; Unknown Sources and enable installation from unknown sources.</li>
        <li>Locate the downloaded APK file and tap on it to begin the installation.</li>
        <li>Follow the prompts to complete the installation.</li>
        <li>Once installed, launch {name} and log in with your account details.</li>
    </ol>
        
        
        <h2>How to Install {name} MOD APK on PC</h2>
        To install {name} MOD APK on your Windows PC, follow these steps:
    <ol>
        <li>Download and install BlueStacks software from a trusted source.</li>
        <li>Download {name} MOD APK from our website.</li>
        <li>Install the APK file using BlueStacks by following the provided steps.</li>
        <li>Once installed, you can enjoy {name} MOD APK on your PC.</li>
    </ol>
        <h2>Conclusion</h2>
        If you're looking for an unlocked version of {name}, the {name} MOD APK is a great choice. It provides access to all the app's content without any restrictions and comes with bug fixes and performance improvements for a smooth experience. Download now and enjoy!
                                                    """
        post.post_status = 'publish'
        post.custom_fields = []

        # dl_link
        custom = {
            '0': {
                'title': 'test',
                'content': 'test'
            }
        }
        post.custom_fields.append({
            'key': 'custom_boxes',
            'value': custom
        })


        datos_download = {
            'option': 'links',
            'type': 'apk',
            '0': {
                'link': f'{dl_links}',
                'texto': 'Download MOD'
            },
            'direct-link': None,
            'direct-download': None
        }
        post.custom_fields.append({
            'key': 'datos_download',
            'value': datos_download
        })

        # screenshots
        ##########################

        datos_imagenes = [
            f'{ss1}=h300',
            f'{ss2}=h300',
            f'{ss3}=h300'
        ]

        post.custom_fields.append({
            'key': 'datos_imagenes',
            'value': datos_imagenes
        })

        # app_info
        ##########################
        datos_informacion = {
            'app_status': None,  # new
            'descripcion': f'{shortdesp}',
            'version': f'{app_version}',
            'tamano': f'{size}',
            'fecha_actualizacion': f'{current_date}',
            'last_update': None,
            'requerimientos': f'{requirements}',
            'consiguelo': f'{play_store_id}',
            'categoria_app': 'APPS',
            'os': 'ANDROID',
            'offer': {
                'amount': None,
                'currency': 'USD'
            },
            'novedades': f'<p>{mod} \n {mod_info}</p>'
        }

        post.custom_fields.append({
            'key': 'datos_informacion',
            'value': datos_informacion
        })

        # app_yt
        ##########################

        datos_video = {
            'id': yt
        }

        post.custom_fields.append({
            'key': 'datos_video',
            'value': datos_video
        })

        if is_update:
            post.id = wp.call(posts.EditPost(existing_post_id, post))
            return version, post.id, post.slug, img
        else:
            print("Asd")
            post.id = wp.call(posts.NewPost(post))
            return version, post.id, post.slug, img


def wordpress_post():
    current_month = datetime.now().strftime('%B')
    db_folder = 'DB'
    month_folder = os.path.join(db_folder, current_month)
    day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))
    if os.path.exists(day_folder):
        json_files = [f for f in os.listdir(day_folder) if f.endswith('.json')]
        if json_files:
            for json_filename in json_files:
                data_dict = {}  # Create an empty dictionary to store the data
                json_path = os.path.join(day_folder, json_filename)
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
                    for key, value in data.items():
                        data[key] = value  # Store the value in the dictionary
                    meaningful_id = data["id"]
                    post_title = data["title"]
                    post_link = data["link"]
                    requirements = data["requirements"]
                    overview = data["overview"]
                    mod_info = data["mod_info"]
                    app_name = data["app_name"]
                    app_version = data["app_version"]
                    app_mod = data["app_mod"]
                    dl_links = data["dl_link_final"]
                    apksize = data["apk_size"]
                    scrap_content = data["scrap_content"]
                    post_id = data["post_Id"]
                    vt_scan = data["scan_vt"]
                    play_store_id = data["play_store_id"]

                    status = meta_check(post_title, app_name)
                    if str(play_store_id).startswith("http"):
                        if status is False:
                            continue
                        if status is True:
                            post_id = get_post_id()
                            version, postid, slug, img = playstore_post(data, is_update=True, existing_post_id=post_id,
                                                                        non_play=False)
                            arguments = (
                                post_title, img, post_link, requirements, overview, mod_info, dl_links, apksize,
                                scrap_content)
                            for save_metadata_value in [True]:
                                store_links(*arguments, save_metadata=True)
                            data["published"] = True
                            data["slug"] = slug
                            data["post_Id"] = post_id
                            with open(json_path, 'w') as json_file:
                                json.dump(data, json_file, indent=4)

                        else:
                            version, postid, slug, img = playstore_post(data, is_update=False, existing_post_id=None,
                                                                        non_play=False)
                            arguments = (
                                post_title, img, post_link, requirements, overview, mod_info, dl_links, apksize,
                                scrap_content, scrap_content, vt_scan, play_store_id, app_name)

                            # Loop over save_metadata values (False and True)
                            for save_metadata_value in [False, True]:
                                store_links(*arguments, save_metadata=save_metadata_value)
                            data["published"] = True
                            data["slug"] = slug
                            data["post_Id"] = postid
                            with open(json_path, 'w') as json_file:
                                json.dump(data, json_file, indent=4)
                    else:
                        if status is False:
                            continue
                        if status is True:
                            post_id = get_post_id()
                            print(post_title)
                            version, postid, slug, img = playstore_post(data, is_update=True, existing_post_id=post_id,
                                                                        non_play=True)
                            # Define the arguments
                            arguments = (
                                post_title, img, post_link, requirements, overview, mod_info, dl_links, apksize,
                                scrap_content, scrap_content, vt_scan, play_store_id, app_name)

                            # Loop over save_metadata values (False and True)
                            for save_metadata_value in [False, True]:
                                store_links(*arguments, save_metadata=save_metadata_value)
                            data["published"] = True
                            data["slug"] = slug
                            data["post_Id"] = post_id
                            with open(json_path, 'w') as json_file:
                                json.dump(data, json_file, indent=4)

                        else:
                            version, postid, slug, img = playstore_post(data, is_update=False, existing_post_id=None,
                                                                        non_play=True)
                            arguments = (
                                post_title, img, post_link, requirements, overview, mod_info, dl_links, apksize,
                                scrap_content, scrap_content, vt_scan, play_store_id, app_name)
                            # Loop over save_metadata values (False and True)
                            for save_metadata_value in [False, True]:
                                store_links(*arguments, save_metadata=save_metadata_value)
                            data["published"] = True
                            data["slug"] = slug
                            data["post_Id"] = post_id
                            with open(json_path, 'w') as json_file:
                                json.dump(data, json_file, indent=4)

    return True


