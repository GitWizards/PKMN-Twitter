import hashlib
import time
from subprocess import call

import requests
from telegram.ext import CallbackContext, Updater

from settings import TOKEN, URL


def bot_loop(context: CallbackContext):
    counter = 0
    img_data = requests.get(URL).content
    old_pic = hashlib.sha256(img_data).hexdigest()

    # Collect pics
    while counter < 10:
        img_data = requests.get(URL).content
        new_pic = hashlib.sha256(img_data).hexdigest()

        if old_pic != new_pic:
            old_pic = new_pic
            with open(f"{counter}.jpg", 'wb') as f:
                f.write(img_data)
                counter += 1

        time.sleep(15)

    # Make GIF
    call(["convert", "-delay", "100", "-loop", "1", "*.jpg", "final.gif"])

    # Send GIF to channel
    with open('final.gif', 'rb') as gif:
        context.bot.send_animation(chat_id="@pkmn_twitter", animation=gif)


def main():
    print("Starting bot...")
    updater = Updater(TOKEN, use_context=True)
    updater.job_queue.run_repeating(bot_loop, interval=160, first=0)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
