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

def download(Username,bot,update,username, password):
    bot.sendMessage(update.effective_user.id, "Downloading story ...")
    instagram = instaloader.Instaloader()
    instagram.login(username, password)
    userid = instaloader.Profile.from_username(instagram.context, Username).userid
    instagram.dirname_pattern = os.path.join(
        os.path.abspath("."), f"story/{username}")
    directory = os.path.join(
            os.path.abspath("."), f"story/{username}")
    for story in instagram.get_stories(userids=[userid]):
        for item in story.get_items():
            instagram.download_storyitem(item, 'story')
    bot.sendMessage(update.effective_user.id, "The story was successfully downloaded")
    for filename in os.listdir(directory):
                if filename == f'{instagram.filename_pattern}.json.xz':
                    pass
                elif filename == f'{instagram.filename_pattern}.txt':
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
            
def download_highlight(my_username,bot,update,Username, Password):
    bot.sendMessage(update.effective_user.id, "Downloading highlight ...")
    instagram = instaloader.Instaloader()
    instagram.login(Username, Password)
    profile = Profile.from_username(instagram.context, username=my_username)
    instagram.dirname_pattern = os.path.join(
        os.path.abspath("."), f"highlight/{my_username}")
    directory = os.path.join(
            os.path.abspath("."), f"highlight/{my_username}")
    for highlight in instagram.get_highlights(user=profile):
        # highlight is a Highlight object
        for item in highlight.get_items():
            # item is a StoryItem object
            instagram.download_storyitem(item, '{}/{}'.format(highlight.owner_username, highlight.title))


    bot.sendMessage(update.effective_user.id, "Highlight successfully downloaded")
    for filename in os.listdir(directory):
                if filename == f'{instagram.filename_pattern}.json.xz':
                    pass
                elif filename == f'{instagram.filename_pattern}.txt':
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