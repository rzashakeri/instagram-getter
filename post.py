import instaloader
from instaloader import Profile, Post 
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

def download(post_id,bot,update,username, password):
    bot.sendMessage(update.effective_user.id, "Downloading content ...")
    instagram = instaloader.Instaloader()
    instagram.login(username, password)
    instagram.dirname_pattern = os.path.join(
        os.path.abspath("."), f"post/{username}")
    post = Post.from_shortcode(instagram.context, post_id)
    bot.sendMessage(update.effective_user.id, """Content successfully downloaded\nIt will be sent to you in a few moments""")
    directory = os.path.join(
        os.path.abspath("."), f"post/{username}")
    instagram.download_post(post, target = instagram.dirname_pattern)
    bot.sendMessage(update.effective_user.id, "Please wait a moment")
    for filename in os.listdir(directory):
        if filename == f'{post_id}.json.xz':
            pass
        elif filename == f'{post_id}.txt':
            pass
        elif filename.endswith('.mp4'): 
            bot.send_video(chat_id=update.effective_user.id,
                video=open(f'{directory}/{filename}', 'rb'))
            
        elif filename.endswith('.jpg'):
            bot.send_photo(chat_id=update.effective_user.id,
                photo=open(f'{directory}/{filename}', 'rb'))
        
        elif filename.endswith('.webp'):
            bot.send_photo(chat_id=update.effective_user.id,
                photo=open(f'{directory}/{filename}', 'rb'))
        
    shutil.rmtree(directory)
    main.done(update, CallbackContext)