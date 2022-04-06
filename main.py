import psycopg2
import profile
from instaloader import Instaloader, Profile, Post
import logging
from typing import Dict
import instaloader
import hashlib
import post
import story
from telegram import (
    ReplyKeyboardMarkup,
    TelegramError,
    Update,
    ReplyKeyboardRemove,
    Bot,
    User
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# ======= Enable logging ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

global Username
global Password
global instagram
instagram = instaloader.Instaloader()

# ======= add bot token ========

admin_id = 111111 # put your user id in telegram
TOKEN = "Your Token"
bot = Bot(TOKEN)
logger = logging.getLogger(__name__)

# ======== add keyboard =========

CHOOSING, TYPING_REPLY_FOR_PROFILE, GET_LOGIN_DATA, LOGIN, TYPING_REPLY_FOR_POST, TYPING_REPLY_FOR_STORY , TYPING_REPLY_FOR_REELS, TYPING_REPLY_FOR_HIGHLIGHT, CHOOSING_DOWNLOAD_STORY, CHOOSING_ADMIN, USER_COUNT, SEND_MESSAGE_TO_ALL   = range(12)

reply_keyboard = [
    ['Download Post', 'Download Story', 'Download Reels'],
    ['Download Profile', 'Login'],
    ['About']
]

story_keyboard = [
    ['Download Story' , 'Download Highlight'], 
    ['Back']
]

admin_keyboard = [
    ['User Count', 'Send Message To All'],
    ['Back']
]

admin_markup = ReplyKeyboardMarkup(
    admin_keyboard, one_time_keyboard=True, resize_keyboard=True)

story_markup = ReplyKeyboardMarkup(
    story_keyboard, one_time_keyboard=True, resize_keyboard=True)

markup = ReplyKeyboardMarkup(
    reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

# ====== when start bot call this function ========


def start(update: Update, context: CallbackContext) -> int:
    
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    
    connection = psycopg2.connect(database="database name", user="user name", password="password", host="host name", port="5432")
    cursor = connection.cursor()
    query = "CREATE TABLE IF NOT EXISTS user (userId INTEGER PRIMARY KEY,first_name varchar (60),last_family varchar (60));"
    cursor.execute(query)
    try:
        cursor.execute(f'INSERT INTO user (userId,first_name, last_family) Values (%s, %s, %s)',(user_id,first_name,last_name))
    except psycopg2.IntegrityError:
        pass
    connection.commit()
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        f"hi {first_name} welcome to instagram downloader bot\n"
        "\n"
        "You can download anything you want from Instagram through this robot\n"
        "\n"
        "If you want to download posts, stories and rails in high quality, first log in to your Instagram account via the login button and then download your profile or post via the download button.",
        reply_markup=markup,
    )

    return CHOOSING


def choice_download_profile(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your Instagram idea in the following format:\n'
                              "\n"
                              "@username")

    return TYPING_REPLY_FOR_PROFILE


def received_information_profile(update: Update, context: CallbackContext) -> int:

    try:

        username = update.message.text
        username_corrected = username.split('@')

        profile.download_profile_hd(
            username_corrected, bot, update, Username, Password)

        return CHOOSING
    except NameError:
        profile.download_profile_sd(
            username_corrected, bot, update)
        return CHOOSING
    

def choice_download_post(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please send the post link :')

    return TYPING_REPLY_FOR_POST


def received_information_post(update: Update, context: CallbackContext) -> int:
    try:
        global Username
        global Password
    
        message = update.message.text
        link_of_post = message.split('/')
        post.download(link_of_post[4],bot,update,Username, Password)
        return CHOOSING
    except NameError:
        bot.sendMessage(update.effective_user.id, "To download the first post, you must log in via the 'Login' button")
        return CHOOSING
    except IndexError:
        bot.sendMessage(update.effective_user.id, "There is a problem, try again ...")
        return CHOOSING


def choice_download_story_or_highlight(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Do you want to download a regular story or highlight stories ?', reply_markup=story_markup)
    return CHOOSING_DOWNLOAD_STORY


def choice_download_story(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Send the story link :', reply_markup=markup)
    return TYPING_REPLY_FOR_STORY


def choice_download_highlight(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter your Instagram idea in the following format :\n'
                              "\n"
                              "@username", reply_markup=markup)
    return TYPING_REPLY_FOR_HIGHLIGHT


def received_information_story(update: Update, context: CallbackContext) -> int:
    try:
        global Username
        global Password
        message = update.message.text.split('/')
        username = message[4]
        if username == 'highlights':
            bot.sendMessage(update.effective_user.id, "The link entered is incorrect !")
            return CHOOSING
        story.download(username,bot,update,Username, Password)
        return CHOOSING
    except NameError:
        bot.sendMessage(update.effective_user.id, "To download the first story, you must log in via the 'Login' button")
        return CHOOSING
    except IndexError:
        bot.sendMessage(update.effective_user.id, "There is a problem, try again ...")
        return CHOOSING
    except instaloader.exceptions.ProfileNotExistsException:
        bot.sendMessage(update.effective_user.id, "The link entered is incorrect!")
        return CHOOSING


def received_information_highlight(update: Update, context: CallbackContext) -> int:
    try:
        global Username
        global Password
        message = update.message.text.split('@')
        username = message[1]
        story.download_highlight(username,bot,update,Username, Password)
        return CHOOSING
    except NameError:
        bot.sendMessage(update.effective_user.id, "To download the first story, you must log in via the 'Login' button")
        return CHOOSING
    except IndexError:
        bot.sendMessage(update.effective_user.id, "There is a problem, try again ...")
        return CHOOSING
    except instaloader.exceptions.ProfileNotExistsException:
        bot.sendMessage(update.effective_user.id, "The link entered is incorrect!")
        return CHOOSING


def choice_download_reels(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please send the reels link:')
    return TYPING_REPLY_FOR_REELS


def received_information_reels(update: Update, context: CallbackContext) -> int:
    try:
        global Username
        global Password
    
        message = update.message.text
        link_of_post = message.split('/')
        post.download(link_of_post[4],bot,update,Username, Password)
        return CHOOSING
    except NameError:
        bot.sendMessage(update.effective_user.id, "To download the first rails, you must enter through the 'Login' button")
        return CHOOSING
    except IndexError:
        bot.sendMessage(update.effective_user.id, "There is a problem, try again ...")
        return CHOOSING


def done(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(
        " ✔ دانلود شما تموم شد",
        reply_markup=markup,
    )

    return CHOOSING


def back(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(
        "Return to Home",
        reply_markup=markup
    )
    return CHOOSING


def about(update: Update, context: CallbackContext) -> int:
    bot.send_message(update.message.chat.id, """
                    \n You can also help me develop this robot:
                    \n https://github.com/rzashakeri/instagram-downloader-bot
                     """, parse_mode='Markdown')

    return CHOOSING


def connect_instagram(update: Update, context: CallbackContext) -> int:
    bot.sendMessage(update.effective_user.id, "Note that your information is stored as a session in the robot and to ensure you can use a fake account to download quality content")
    update.message.reply_text('Please enter your Instagram username and password in the following format:\n'
                              "\n"
                              "username\n"
                              "password")
    bot.sendMessage(update.effective_user.id, "Enter your username instead of username and your password instead of password")

    return LOGIN


def login_instagram(update: Update, context: CallbackContext) -> int:
    try:
        message = update.message.text.split('\n')
        global Username
        Username = message[0]
        global Password
        Password = message[1]
        if instagram.load_session_from_file(Username, filename=f'sessions/{Username}_{update.effective_user.id}') is None:
            update.message.reply_text(
            "You have already logged in",
            reply_markup=markup,
            )
    except FileNotFoundError:
        try:
            instagram.login(Username,Password)
            update.message.reply_text(
            "You are logged in\nClick the profile download button and download the profile picture in high quality",
            reply_markup=markup,
            )
            instagram.save_session_to_file(filename=f'sessions/{Username}_{update.effective_user.id}')
        except instaloader.BadCredentialsException:
            update.message.reply_text(
            "Please enter your username or password correctly",
            reply_markup=markup,
            )
            return GET_LOGIN_DATA
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            bot.sendMessage(update.effective_user.id, "Two-step verification is enabled, please disable it first and try again later")
            return CHOOSING
    except IndexError:
        bot.sendMessage(update.effective_user.id, "There is a problem, try again ...")
        return CHOOSING
        

    
    return CHOOSING


def admin(update: Update, context: CallbackContext) -> int:
    if update.effective_user.id == admin_id:
        update.message.reply_text('You are logged in as admin', reply_markup=admin_markup)
        return CHOOSING_ADMIN      
    else:
        pass
        return CHOOSING


def user_count(update: Update, context: CallbackContext) -> int:
    connection = psycopg2.connect(database="database name", user="user name", password="password", host="host name", port="5432")
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM user"
    cursor.execute(query)
    user_count = cursor.fetchone()
    bot.sendMessage(update.effective_user.id, f"user count : {user_count[0]}")
    return CHOOSING_ADMIN

def get_message(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Enter the message you want to send to everyone :', reply_markup=admin_markup)
    return SEND_MESSAGE_TO_ALL      

def send_message_to_all(update: Update, context: CallbackContext) -> int:
    connection = psycopg2.connect(database="database name", user="user name", password="password", host="host name", port="5432")
    cursor = connection.cursor()
    query = "SELECT userid FROM user"
    cursor.execute(query)
    users = cursor.fetchall()
    message = update.message.text
    for user in users:
        bot.sendMessage(chat_id=user[0], text=message)
    bot.sendMessage(update.effective_user.id, 'Your message has been successfully sent')
    return CHOOSING_ADMIN
    

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex(
                        '^(Download Profile)$'), choice_download_profile
                ),
                MessageHandler(
                    Filters.regex(
                        '^(About)$'), about
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Login)$'), connect_instagram
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Download Post)$'), choice_download_post
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Download Story)$'), choice_download_story_or_highlight
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Download Reels)$'), choice_download_reels
                ),
                CommandHandler('admin', admin)
            ],
            TYPING_REPLY_FOR_PROFILE: [
                MessageHandler(
                    Filters.text,
                    received_information_profile,
                )
            ],
            LOGIN: [
                MessageHandler(
                    Filters.text,
                    login_instagram,
                )
            ],
            GET_LOGIN_DATA:[
                    MessageHandler(
                    Filters.text,
                    connect_instagram,
                )
            ],
            TYPING_REPLY_FOR_POST:[
                    MessageHandler(
                    Filters.text,
                    received_information_post,
                )
            ],
            TYPING_REPLY_FOR_STORY:[
                    MessageHandler(
                    Filters.text,
                    received_information_story,
                )
            ],
            TYPING_REPLY_FOR_REELS:[
                    MessageHandler(
                    Filters.text,
                    received_information_reels,
                )
            ],
            CHOOSING_DOWNLOAD_STORY:[
                MessageHandler(
                    Filters.regex(
                        '^(Download Story)$'), choice_download_story
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Download Highlight)$'), choice_download_highlight
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Back)$'), back
                )
            ],
            TYPING_REPLY_FOR_HIGHLIGHT:[
                    MessageHandler(
                    Filters.text,
                    received_information_highlight,
                )
            ],
            CHOOSING_ADMIN:[
                MessageHandler(
                    Filters.regex(
                        '^(User Count)$'), user_count
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Back)$'), back
                ),
                MessageHandler(
                    Filters.regex(
                        '^(Send Message To All)$'), get_message
                ) 
            ],
            SEND_MESSAGE_TO_ALL:[
                    MessageHandler(
                    Filters.text,
                    send_message_to_all
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )
    dispatcher.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
