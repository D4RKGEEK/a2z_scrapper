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


def parse_version(version_string):
    return tuple(map(int, version_string.split('.')))


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
        print(wp)
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
        post.terms_names = {
            'post_tag': ['tagA', 'another tag'],
            'category': [f'{cat}'],
        }
        print(post.terms_names)

        cat_link = slugify(cat)
        desp = scrap_content
        post.content = f"""
                            <p style="text-align: center;"><strong><h1> {title} </h1></strong></p>

                            <p style="text-align: center;"><strong>Download The Latest Apk Version of {name} MOD, A <a href="https://apkism.com/category/{cat_link}">{cat}</a> App For Android Device. This MOD Includes {mod} Features Unlocked. Download Yours Now!</strong></p>

                            <h2>What Is {name} MOD APK</h2>
                            <img class="aligncenter" src="{thumbnail_url}" alt="{name} MOD Apk" width="220" height="220" />

                            <strong>{name} Mod APK</strong> : A {name} MOD (mobile application) APK is an unofficial app that provides modifications or "enhancements" to the normal {name} experience on Android devices. These mods can include adding new content, new features and some functions unlocked that provides premium or paid subscription.

                            A mod apk is an app that has been modified or "unlocked" to allow access to {mod} features. These features can include additional content, new levels, bonus items, and more. Why would I want to unlock a mod apk?

                            There are a number of reasons. For example, some people like to use {mod} features because they feel they get better value for their money. Others might want extra help in retrieving coins or gems that are hidden in the game. And still others may just enjoy playing with upgraded versions of the game objects or graphics. In any case, unlocking mods provides another way for users to customize and enhance their experience on mobile apps.

                            <h2>Features of {name} Mod APK</h2>
                            The popularity of {name} <strong>{version}</strong> MOD APK has exploded in recent years due to its numerous benefits over the standard version of the {name} apk.

                            <strong>No ads</strong>: Unlike the standard version of the {name} apk, which features intrusive advertising throughout in app, {name} Latest MOD APK Download removes all commercial content. This means that you can use this app without ever being interrupted by annoying commercials.

                            <strong>More Features:</strong> With no ads comes more choice - you can use this app with unlocked features unlocked.

                            <strong>Enhanced App experience:</strong> Since there are no interruptions between scenes thanks to ad removal, using {name} APK MOD feels much smoother and faster than using the regular {name} MOD APK {version}.

                            <strong>{mod} Unlocked</strong> : If you've ever tried to use a {mod} feature on <strong>{name} mod download</strong> and found that it was blocked or not available Most apps restrict access to premium features only to those who have paid for them.

                            {desp}
                            <h2>Download {name} MOD APK Latest Version</h2>
                            If you're looking for a MOD APK file for {name}, you can find it here. This particular version of the {name} apk is unlocked {mod} Features, meaning you'll have access to all of the app's content without having to pay for a subscription.

                            To install the MOD APK file, simply download it and then open it up in your preferred File Manager app. Once it's been installed, you should be able to launch {name} and log in with your account details. Enjoy!
                            <h2>How To Install {name} Mod Apk Download</h2>
                            Fortunately, there’s a way to get {name} for free. There are many {name} mod apk download available online, but we recommend using the one from our site. It’s safe and easy to use, and it will unlock all of {name} features for you.

                            To install the <strong>Download {name} mod apk</strong>, just follow these simple steps:

                            1. Download the apk file from our site.

                            2. On your Android device, go to Settings &gt; Security &gt; Unknown Sources and turn on Unknown Sources. This will allow you to install apps from outside of the Google Play Store.

                            3. Find the downloaded apk file and tap on it to begin installation.

                            4. Follow the prompts to finish installation.

                            5. That’s it! You now have access to all of {name} features for free!
                            <h2 class="ac">Download {name} Mod APK For PC</h2>
                            You can download the <strong>{name} Mod APK </strong>on the Windows PC with the following simple steps:
                            <ol>
                                <li>Download Bluestacks software online by downloading it from any third-party source.</li>
                                <li>Install BlueStacks In Your PC.</li>
                                <li>Download {name} MOD APK From Our Website In Bluestacks.</li>
                                <li>Install The .APK File By Steps Provided Above.</li>
                                <li>Once it completes, you can start enjoying {name} mod apk for pc!</li>
                            </ol>
                            <h2>Conclusion</h2>
                            If you're looking for an unlocked version of {name}, the {name} {version} MOD APK is a great option. With this download, you'll be able to access all of {name} content without any restrictions. Plus, the MOD APK comes with a number of bug fixes and performance improvements, so you can enjoy a smooth and uninterrupted experience.
                                            """
        post.post_status = 'publish'
        post.custom_fields = []

        #dl_link
        ##########################

        datos_download = {
            'option': 'links',
            'type': 'apk',
            '0': {
                'link': f'{dl_links}',
                'texto': 'Download MOD Apk'
            },
            'direct-link': None,
            'direct-download': None
        }
        post.custom_fields.append({
            'key': 'datos_download',
            'value': datos_download
        })

        #screenshots
        ##########################

        datos_imagenes = [
            'app_image1',
            'app_image1',
            'app_image1',
            'app_image1',
            'app_image1',
            None,
            None,
            None,
            None,
            None
        ]

        post.custom_fields.append({
            'key': 'datos_imagenes',
            'value': datos_imagenes
        })

        #app_info
        ##########################
        datos_informacion = {
            'app_status': 'updated', #new
            'descripcion': 'app_desp_short',
            'version': f'{app_version}',
            'tamano': f'{size}',
            'fecha_actualizacion': 'app_updated',
            'last_update': None,
            'requerimientos': f'{requirements}',
            'consiguelo': f'{play_store_id}',
            'categoria_app': 'APPS',
            'os': 'ANDROID',
            'offer': {
                'amount': None,
                'currency': 'USD'
            },
            'novedades': f'<p>BUG FIXES</p>'
        }

        post.custom_fields.append({
            'key': 'datos_informacion',
            'value': datos_informacion
        })

        #app_yt
        ##########################

        datos_video = {
            'id': 'app_yd_id'
        }

        post.custom_fields.append({
            'key': 'datos_video',
            'value': datos_video
        })

        post.custom_fields.append({
            'key': 'new_rating_average',
            'value': "4.5"
        })
        post.custom_fields.append({
            'key': 'new_rating_count',
            'value': "users"
        })




        if is_update:
            print(existing_post_id)
            post.id = wp.call(posts.EditPost(existing_post_id, post))
            return version, post.id, post.slug, img_link
        else:
            post.id = wp.call(posts.NewPost(post))
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
        if video is not None:
            yt = video[32:44]
        else:
            yt = ""
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
        print(img2)

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
                    <p style="text-align: center;"><strong><h1> {title} </h1></strong></p>

                    <p style="text-align: center;"><strong>Download The Latest Apk Version of {name} MOD, A <a href="https://apkism.com/category/{cat_link}">{cat}</a> App For Android Device. This MOD Includes {mod} Features Unlocked. Download Yours Now!</strong></p>

                    <h2>What Is {name} MOD APK</h2>
                    <img class="aligncenter" src="{thumbnail_url}" alt="{name} MOD Apk" width="220" height="220" />

                    <strong>{name} Mod APK</strong> : A {name} MOD (mobile application) APK is an unofficial app that provides modifications or "enhancements" to the normal {name} experience on Android devices. These mods can include adding new content, new features and some functions unlocked that provides premium or paid subscription.

                    A mod apk is an app that has been modified or "unlocked" to allow access to {mod} features. These features can include additional content, new levels, bonus items, and more. Why would I want to unlock a mod apk?

                    There are a number of reasons. For example, some people like to use {mod} features because they feel they get better value for their money. Others might want extra help in retrieving coins or gems that are hidden in the game. And still others may just enjoy playing with upgraded versions of the game objects or graphics. In any case, unlocking mods provides another way for users to customize and enhance their experience on mobile apps.

                    <h2>Features of {name} Mod APK</h2>
                    The popularity of {name} <strong>{version}</strong> MOD APK has exploded in recent years due to its numerous benefits over the standard version of the {name} apk.

                    <strong>No ads</strong>: Unlike the standard version of the {name} apk, which features intrusive advertising throughout in app, {name} Latest MOD APK Download removes all commercial content. This means that you can use this app without ever being interrupted by annoying commercials.

                    <strong>More Features:</strong> With no ads comes more choice - you can use this app with unlocked features unlocked.

                    <strong>Enhanced App experience:</strong> Since there are no interruptions between scenes thanks to ad removal, using {name} APK MOD feels much smoother and faster than using the regular {name} MOD APK {version}.

                    <strong>{mod} Unlocked</strong> : If you've ever tried to use a {mod} feature on <strong>{name} mod download</strong> and found that it was blocked or not available Most apps restrict access to premium features only to those who have paid for them.

                    {desp}
                    <h2>Download {name} MOD APK Latest Version</h2>
                    If you're looking for a MOD APK file for {name}, you can find it here. This particular version of the {name} apk is unlocked {mod} Features, meaning you'll have access to all of the app's content without having to pay for a subscription.

                    To install the MOD APK file, simply download it and then open it up in your preferred File Manager app. Once it's been installed, you should be able to launch {name} and log in with your account details. Enjoy!
                    <h2>How To Install {name} Mod Apk Download</h2>
                    Fortunately, there’s a way to get {name} for free. There are many {name} mod apk download available online, but we recommend using the one from our site. It’s safe and easy to use, and it will unlock all of {name} features for you.

                    To install the <strong>Download {name} mod apk</strong>, just follow these simple steps:

                    1. Download the apk file from our site.

                    2. On your Android device, go to Settings &gt; Security &gt; Unknown Sources and turn on Unknown Sources. This will allow you to install apps from outside of the Google Play Store.

                    3. Find the downloaded apk file and tap on it to begin installation.

                    4. Follow the prompts to finish installation.

                    5. That’s it! You now have access to all of {name} features for free!
                    <h2 class="ac">Download {name} Mod APK For PC</h2>
                    You can download the <strong>{name} Mod APK </strong>on the Windows PC with the following simple steps:
                    <ol>
                        <li>Download Bluestacks software online by downloading it from any third-party source.</li>
                        <li>Install BlueStacks In Your PC.</li>
                        <li>Download {name} MOD APK From Our Website In Bluestacks.</li>
                        <li>Install The .APK File By Steps Provided Above.</li>
                        <li>Once it completes, you can start enjoying {name} mod apk for pc!</li>
                    </ol>
                    <h2>Conclusion</h2>
                    If you're looking for an unlocked version of {name}, the {name} {version} MOD APK is a great option. With this download, you'll be able to access all of {name} content without any restrictions. Plus, the MOD APK comes with a number of bug fixes and performance improvements, so you can enjoy a smooth and uninterrupted experience.
                                    """
        post.post_status = 'publish'
        post.custom_fields = []

        # dl_link
        ##########################

        datos_download = {
            'option': 'links',
            'type': 'apk',
            '0': {
                'link': f'{dl_links}',
                'texto': 'Download MOD Apk'
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
            'app_image1',
            'app_image1',
            'app_image1',
            'app_image1',
            'app_image1',
            None,
            None,
            None,
            None,
            None
        ]

        post.custom_fields.append({
            'key': 'datos_imagenes',
            'value': datos_imagenes
        })

        # app_info
        ##########################
        datos_informacion = {
            'app_status': 'updated',  # new
            'descripcion': 'app_desp_short',
            'version': f'{app_version}',
            'tamano': f'{size}',
            'fecha_actualizacion': 'app_updated',
            'last_update': None,
            'requerimientos': f'{requirements}',
            'consiguelo': f'{play_store_id}',
            'categoria_app': 'APPS',
            'os': 'ANDROID',
            'offer': {
                'amount': None,
                'currency': 'USD'
            },
            'novedades': f'<p>BUG FIXES</p>'
        }

        post.custom_fields.append({
            'key': 'datos_informacion',
            'value': datos_informacion
        })

        # app_yt
        ##########################

        datos_video = {
            'id': 'app_yd_id'
        }

        post.custom_fields.append({
            'key': 'datos_video',
            'value': datos_video
        })

        post.custom_fields.append({
            'key': 'new_rating_average',
            'value': "4.5"
        })
        post.custom_fields.append({
            'key': 'new_rating_count',
            'value': "users"
        })

        if is_update:
            post.id = wp.call(posts.EditPost(existing_post_id, post))
            return version, post.id, post.slug, img
        else:
            post.id = wp.call(posts.NewPost(post))
        return version, post.id, post.slug, img
    else:
        print("NON PLAY")


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


print(wordpress_post())