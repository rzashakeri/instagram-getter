import instaloader
import os
import shutil
import main
from telegram import (
    ReplyKeyboardMarkup,
    Update,
    ReplyKeyboardRemove,
    Bot
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

def download_profile_hd(username_corrected,bot,update,username, password):
    try:
        instagram = instaloader.Instaloader(
            title_pattern=f'{username_corrected[1]}')
        instagram.login(username, password)
        bot.sendMessage(update.effective_user.id, "Because you entered, a higher quality photo will be sent")
        bot.sendMessage(update.effective_user.id, "Downloading photos ...")
        instagram.download_profile(
                username_corrected[1], profile_pic_only=True)
        instagram.dirname_pattern = os.path.join(
                os.path.abspath("."), f"{username_corrected[1]}/{username_corrected[1]}.jpg")
        bot.send_photo(chat_id=update.effective_user.id,
                        photo=open(instagram.dirname_pattern, 'rb'))

        path = os.path.join(
                os.path.abspath("."), f"{username_corrected[1]}")

        shutil.rmtree(path)
        main.done(update, CallbackContext)
    except IndexError:
        update.message.reply_text("""        
Please enter an idea in the said format

@username ✔""")
        bot.sendMessage(update.effective_user.id, "And try again using the 'Download Profile' button")
        return main.TYPING_REPLY_FOR_PROFILE 
    
    except instaloader.exceptions.InvalidArgumentException:
        download_profile_sd(username_corrected,bot,update,username, password)
        return main.CHOOSING
    
    except instaloader.exceptions.LoginRequiredException:
        bot.sendMessage(update.effective_user.id, "The username entered is not valid")
        bot.sendMessage(update.effective_user.id, "And try again using the 'Download Profile' button")
        return main.TYPING_REPLY_FOR_PROFILE 

def download_profile_sd(username_corrected,bot,update):
    try:
        instagram = instaloader.Instaloader(
            title_pattern=f'{username_corrected[1]}')
        bot.sendMessage(update.effective_user.id, "Processing ...")
        instagram.download_profile(
                username_corrected[1], profile_pic_only=True)
        bot.sendMessage(update.effective_user.id, "Because you did not enter, a lower quality photo will be sent")
        instagram.dirname_pattern = os.path.join(
                os.path.abspath("."), f"{username_corrected[1]}/{username_corrected[1]}.jpg")
        bot.send_photo(chat_id=update.effective_user.id,
                        photo=open(instagram.dirname_pattern, 'rb'))

        path = os.path.join(
                os.path.abspath("."), f"{username_corrected[1]}")

        shutil.rmtree(path)
        main.done(update, CallbackContext)
        return main.CHOOSING
    except IndexError:
        update.message.reply_text("""        
Please enter an idea in the said format

@username ✔""")
        bot.sendMessage(update.effective_user.id, "And try again using the 'Download Profile' button")
        bot.sendMessage(update.effective_user.id, "To receive a high quality photo, first log in via the 'Login' button")
        return main.TYPING_REPLY_FOR_PROFILE
    
    except instaloader.exceptions.LoginRequiredException:
        bot.sendMessage(update.effective_user.id, "The username entered is not valid")
        bot.sendMessage(update.effective_user.id, "And try again using the 'Download Profile' button")
        return main.TYPING_REPLY_FOR_PROFILE 