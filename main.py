import time
from subprocess import call

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from telegram.ext import CallbackContext, Updater

from settings import TOKEN, URL

# Initialize the webdriver
firefox_options = Options()
firefox_options.add_argument("--headless")
browser = webdriver.Firefox(options=firefox_options)


def get_link() -> str:
    global browser

    browser.get(URL)
    time.sleep(10)
    return browser.find_elements(By.TAG_NAME, "img")[0].get_attribute("src")


def save_pic(image_url: str, filename: str) -> None:
    img_data = requests.get(image_url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)


def bot_loop(context: CallbackContext):
    counter = 0
    old_pic = pic = get_link()
    save_pic(pic, f"{counter}.jpg")

    # Collect pics
    while counter < 10:
        pic = get_link()
        if pic != old_pic:
            counter += 1
            old_pic = pic
            save_pic(pic, f"{counter}.jpg")

    # Make GIF
    call(["convert", "-delay", "100", "-loop", "1", "*.jpg", "final.gif"])

    # Send GIF to channel
    with open('final.gif', 'rb') as gif:
        context.bot.send_animation(chat_id="@pkmn_twitter", animation=gif)


def main():
    print("Starting bot...")
    updater = Updater(TOKEN, use_context=True)
    job = updater.job_queue
    updater.start_polling()
    while True:
        job.run_once(bot_loop, 0)

        if job.jobs():
            time.sleep(160)


if __name__ == "__main__":
    main()
