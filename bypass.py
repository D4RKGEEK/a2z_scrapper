import requests
from bs4 import BeautifulSoup
import threading
import re
import time
from contextlib import suppress
from contextlib import suppress
import requests
from bs4 import BeautifulSoup as Selector
import json
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

api_keys = ["df9ebfee868506bcf0ff042b76582dc6", "d8172d336f1bce9878683a525362af5b", "7d6edd0f8f6a9599fd5d8528b495532c"]


s = requests.session()

def get_download_link(url, data, headers, cookies):
    res = requests.post(url, headers=headers, cookies=cookies, data=data)
    respones = Selector(res.text, 'html.parser')
    download_link = respones.select_one('input[name="url"]')
    if download_link:
        return download_link.attrs['value']
    else:
        return "Not link found"


def uploadrar(fileid):
    segments = fileid.split("/")
    fileid = segments[-1]
    url = f"https://uploadrar.com/{fileid}"
    print(fileid)

    payload = f'adblock_detected=0&id={fileid}&method_free=Free%20Download&method_premium=&op=download2&rand=&referer=https%3A%2F%2Fforum.mobilism.org%2F'
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'host': 'uploadrar.com',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tag = soup.find('span', {'id': 'direct_link'}).find('a')
    href_value = a_tag['href']
    href_value = href_value.replace(" ", "_")
    return href_value


def devuploads(fileid):
    segments = fileid.split("/")
    fileid = segments[-1]
    url = f"https://devuploads.com/{fileid}"

    payload = f'adblock_detected=0&dnumber=9787&id={fileid}&ipp=4119.36.185.88asd&op=download2&rand=kndjok&ransite=2&referer=&tsty=99&xd=asd'
    headers = {
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'host': 'devuploads.com',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the input element with the name "downloadLink"
    download_link_input = soup.find('input', {'name': 'downloadLink'})

    # Check if the input element was found
    if download_link_input:
        # Extract the value of the "downloadLink" input field
        download_link = download_link_input.get('value')

        # Print the download link
        print("Download Link:", download_link)


def a2z_apk(element_with_id_apkdl, data):
    onclick_value = element_with_id_apkdl.get('onclick')
    if "go('" in onclick_value and "')" in onclick_value:
        start_index = onclick_value.index("go('") + len("go('")
        end_index = onclick_value.index("')")
        extracted_value = onclick_value[start_index:end_index]
        id_val = extracted_value.split("','")[0].strip()
        xf_val = data['xf']
        adx_val = data['adx']
        xd_val = data['xd']
        apkid_val = data['apkid']
        varry_val = data['varry']
        user_val = data['user']
        url = f"https://dl.a2zapk.io/server/{id_val}/"
        status = check_url_size(url)
        if status is True:
            return url
        else:
            return None


def check_url_size(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_length = int(response.headers.get('Content-Length', 0))
            if content_length > 500 * 1024:
                return True
    except requests.exceptions.RequestException:
        pass  # Handle request exceptions (e.g., connection error)

    return False




def uploadrar_direct(url):
    segments = url.split("/")
    fileid = segments[-1]
    url = f"https://uploadrar.com/{fileid}"

    payload = f'adblock_detected=0&id={fileid}&method_free=Free%20Download&method_premium=&op=download2&rand=&referer=https%3A%2F%2Fforum.mobilism.org%2F'
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'host': 'uploadrar.com',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <a> tag inside the <span> with id="direct_link"
    a_tag = soup.find('span', {'id': 'direct_link'}).find('a')

    # Get the href attribute value
    href_value = a_tag['href']

    return href_value