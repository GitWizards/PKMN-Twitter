import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from telegram.ext import Updater, CallbackContext
from settings import URL, TOKEN


firefox_options = Options()
firefox_options.add_argument("--headless")
browser = webdriver.Firefox(options=firefox_options)

old_pic = None


def get_link() -> str:
    global browser

    browser.get(URL)
    time.sleep(5)
    return browser.find_elements(By.TAG_NAME, "img")[0].get_attribute("src")


def send_pic(context: CallbackContext):
    global old_pic

    pic = get_link()
    
    if old_pic != pic:
        old_pic = pic 
        context.bot.sendPhoto(
            chat_id="@pkmn_twitter",
            photo=pic
        )

def main():
    print("Starting bot...")
    updater = Updater(TOKEN, use_context=True)
    job = updater.job_queue
    job.run_repeating(send_pic, interval=15, first=0)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
