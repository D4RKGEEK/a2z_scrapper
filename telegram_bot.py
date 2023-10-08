from telethon.sync import TelegramClient
from telethon import events
import mss
import pyautogui
import subprocess
import os
import time
from datetime import datetime

scripts_running = False
ss_running = False

api_id = 706263
api_hash = '8dd3aa475c6c1ca8d82f0b9cdc4ad6c3'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=BOT_TOKEN)
from PIL import Image
import io

scripts_path = r'X:\a2z'
running_scripts = {}

async def list_files_in_directory(chat_id, directory_path):
    try:
        files = os.listdir(directory_path)
        file_list = "\n".join(files)
        await client.send_message(chat_id, f"Files in the directory:\n{file_list}")
    except Exception as e:
        await client.send_message(chat_id, f"Error listing files: {str(e)}")

script_mapping = {
    '1': 'main.py',
    '2': 'main2.py',
    '3': 'scan_down.py',
}

def terminate_running_scripts():
    for script_filename, process in running_scripts.items():
        try:
            process.terminate()
        except Exception as e:
            print(f"Error terminating {script_filename}: {str(e)}")

async def run_script_and_send_screenshot(chat_id, script_filename):
    global scripts_running

    # Build the full path to the script
    script_path = os.path.join(scripts_path, script_filename)

    try:
        scripts_running = True

        # Run the script in a separate shell and store the process object
        process = subprocess.Popen(['start', 'cmd', '/c', 'python', script_path], shell=True)
        running_scripts[script_filename] = process

        await client.send_message(chat_id, f"Running {script_filename}...")
    except subprocess.CalledProcessError as e:
        response_msg = f"Error running {script_filename}: {e}"
        await client.send_message(chat_id, response_msg)
    except Exception as e:
        print(f"Error: {str(e)}")

async def capture_and_send_screenshot(chat_id, if_single=False):
    if if_single:
        with mss.mss() as sct:
            screenshot = sct.shot(output="screenshot.png")
        with open("screenshot.png", "rb") as file:
            img_byte_array = io.BytesIO(file.read())
        message = await client.send_file(chat_id, img_byte_array, caption="Screenshot")
        os.remove("screenshot.png")
        await asyncio.sleep(10)
        await client.delete_messages(chat_id, [message])
    else:
        pyautogui.press("F11")
        global scripts_running
        scripts_running = True

        try:
            with mss.mss() as sct:
                screenshot = sct.shot(output="screenshot.png")
            with open("screenshot.png", "rb") as file:
                img_byte_array = io.BytesIO(file.read())
            message = await client.send_file(chat_id, img_byte_array, caption="Screenshot")

            os.remove("screenshot.png")

            await asyncio.sleep(10)
            await client.delete_messages(chat_id, [message])
        except Exception as e:
            print(f"Error: {str(e)}")

@client.on(events.NewMessage)
async def handle_message(event):
    global ss_running
    try:
        message = event.message.message
        chat_id = event.message.chat_id
        print(chat_id)

        if message in script_mapping:
            script_filename = script_mapping[message]
            await run_script_and_send_screenshot(chat_id, script_filename)
        elif message == '/ss_loop':
            if not ss_running:
                ss_running = True
                await client.send_message(chat_id, "Starting screenshot loop...")
                while ss_running:
                    await capture_and_send_screenshot(chat_id)
                    time.sleep(5)
                await client.send_message(chat_id, "Screenshot loop stopped.")
        elif message == '/ss':
            await client.send_message(chat_id, "Capturing a single screenshot...")
            await capture_and_send_screenshot(chat_id, if_single=True)
        elif message == '/dir':
            current_month = datetime.now().strftime('%B')
            db_folder = 'DB'
            month_folder = os.path.join(db_folder, current_month)
            day_folder = os.path.join(month_folder, datetime.now().strftime('%d %b %Y'))

            await list_files_in_directory(chat_id, day_folder)
# Add a new event handler for the /stop command
        elif message == '/stop':
            global scripts_running
            if scripts_running:
                scripts_running = False
                await client.send_message(chat_id, "Stopping all running scripts...")
                terminate_running_scripts()  # Terminate running scripts
            if ss_running:
                ss_running = False
                await client.send_message(chat_id, "Stopping screenshot loop...")
            else:
                await client.send_message(chat_id, "No scripts or screenshot loop are currently running.")


    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    import asyncio
    client.run_until_disconnected()
