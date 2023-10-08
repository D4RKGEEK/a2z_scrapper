import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bypass import uploadrar, devuploads, a2z_apk
import time
from data import store_links, uploadrar_upload
from bs4 import BeautifulSoup
import logging
from telegram_bot import *

# Define the log file where you want to save the logs
log_file = "logfile.log"

def get_element_text(driver, by, selector):
    try:
        element = driver.find_element(by, selector)
        return element.text.strip()
    except:
        return None


def a2z_apps():
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = True
    link_list = []
    driver = uc.Chrome(options=chrome_options)
    driver.get("https://a2zapk.io/Mods/Apps/")

    elements = driver.find_elements(By.XPATH, '//div[@class="AppCont"]')
    for element in elements[:40]:
        ahref = element.find_element(By.TAG_NAME, "a").get_attribute("href")
        title = element.find_element(By.TAG_NAME, "a").get_attribute("title")
        link_list.append(ahref)
    for link in link_list:
        post_link = link
        driver.get(link)
        title = get_element_text(driver, By.XPATH,
                                 "/html/body/div[3]/section/div[1]/div[3]/div[1]/table/tbody/tr/td[2]/div[1]/h1")
        # version_text = get_element_text(driver, By.XPATH, "/html/body/div[3]/section/div[1]/div[3]/div[2]/ul/li[9]")
        # pattern = r'Version: (\d+\.\d+\.\d+)\s*\(([^)]*)\)'
        # match = re.search(pattern, version_text)
        # version, premium_value = None, None
        # if match:
        # version = match.group(1)
        # premium_value = match.group(2) if match.group(2) else "Premium"
        img_element = driver.find_element(By.XPATH,
                                          '/html/body/div[3]/section/div[1]/div[3]/div[1]/table/tbody/tr/td[1]/img')
        img_link = img_element.get_attribute('src')
        requires = get_element_text(driver, By.XPATH, "/html/body/div[3]/section/div[1]/div[3]/div[2]/ul/li[3]")
        requires = requires.replace("Requires ", "")
        size = get_element_text(driver, By.XPATH, "/html/body/div[3]/section/div[1]/div[3]/div[2]/ul/li[6]")
        size = size.replace("Size: ", "")
        app_name = get_element_text(driver, By.XPATH, "/html/body/div[3]/section/div[1]/div[3]/div[2]/h3")
        app_name = app_name.replace(" / Specifications", "")
        app_desp = get_element_text(driver, By.ID, "des")
        app_mod_info = get_element_text(driver, By.CLASS_NAME, "ContentWhatnew")
        dl_page_link = driver.find_element(By.ID, "dlbtn").find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.get(dl_page_link)
        time.sleep(6)
        src_code = driver.page_source
        soup = BeautifulSoup(src_code, 'html.parser')
        form = soup.find('form', id='my_form')  # Find the form by its ID
        if form:
            input_elements = form.find_all('input')  # Find all input elements within the form
            values = {input_element.get('name'): input_element.get('value', '') for input_element in input_elements if
                      input_element.get('name')}
            data_values = values
        dl_link = None
        element_with_id_apkdl = soup.find('a', id='apkdl')
        if element_with_id_apkdl and data_values:
            ok = a2z_apk(element_with_id_apkdl, data_values)
            if ok is not None:
                dl_link = ok

        try:
            play_link = driver.find_element(By.CLASS_NAME, 'GooglePlay').find_element(By.TAG_NAME, 'a')
            play_link = play_link.get_attribute('href')
        except:
            play_link = None
        try:
            virus_scan_link = driver.find_element(By.LINK_TEXT, 'VirusTotal scan report').get_attribute('href')
            # print("VirusTotal Scan Report Link:", virus_scan_link)
        except:
            virus_scan_link = None
            # print("VirusTotal Scan Report Link:", virus_scan_link)
            pass
        if dl_link is None:
            links = driver.find_elements(By.TAG_NAME, 'a')
            additional_link_texts = ["Download APK From Uploadrar", "Download APK From Devuploads",
                                     "Download APK From Dropgalaxy", "Download APK From Dgdrive"]
            for link in links:
                link_text = link.text
                if link_text in additional_link_texts:
                    href = link.get_attribute('href')
                    if "uploadrar" in href:
                        dl_link = uploadrar(href)
                        print(f"{dl_link}")
                        break
                    if "devuploads" in href:
                        dl_link = devuploads(href)
                        print(f"{dl_link}")
                        break

        if dl_link is None:
            continue
        dl_link_final = uploadrar_upload(dl_link)
        if dl_link_final is not None:
            try:
                store_links(title, img_link, post_link, requires, "overview", app_mod_info, dl_link, dl_link_final,
                            size, app_desp,
                            vt_link=virus_scan_link, play_link=play_link, app_name=app_name, save_metadata=False)
                input("asd")
            except:
                continue
        print(app_name + "\n")
        print("****" * 5)
    driver.quit()


a2z_apps()
