import hashlib
import time
from subprocess import call

import requests
from telegram.ext import CallbackContext, Updater

from settings import TOKEN, URL


def bot_loop(context: CallbackContext):
    while True:
        counter = 0
        old_pic_hash = ""

        # Collect pics
        while counter < 10:
            img_data = requests.get(URL).content
            new_pic_hash = hashlib.sha256(img_data).hexdigest()

            if old_pic_hash != new_pic_hash:
                old_pic_hash = new_pic_hash
                with open(f"{counter}.jpg", 'wb') as f:
                    f.write(img_data)
                    counter += 1

            time.sleep(15)

        # Make GIF
        call(["convert", "-delay", "75", "-loop", "1", "*.jpg", "final.gif"])

        # Send GIF to channel
        with open('final.gif', 'rb') as gif:
            context.bot.send_animation(chat_id="@radeox", animation=gif)


def main():
    print("Starting bot...")
    updater = Updater(TOKEN, use_context=True)
    updater.job_queue.run_once(bot_loop, 0)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
