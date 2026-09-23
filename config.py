#cop

import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

def getenv_int(name, default):
    value = getenv(name)
    return int(value) if value not in (None, "") else default

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_USERNAME = getenv("OWNER_USERNAME", "Kaito_3_2")
BOT_USERNAME = getenv("BOT_USERNAME", "IAM_MIMBOT")
BOT_NAME = getenv("BOT_NAME", "MIMI X MUSIC")
ASSUSERNAME = getenv("ASSUSERNAME", "Kaito_3_2")

GROQ_API_KEY = getenv("GROQ_API_KEY")
MONGO_DB_URI = getenv("MONGO_DB_URI")
NSFWAPI = getenv("NSFWAPI")

DURATION_LIMIT_MIN = getenv_int("DURATION_LIMIT", 17000)

START_REACTION = getenv("START_REACTION", "🥰")
START_STICKER = getenv("START_STICKER", "CAACAgUAAxkBAAFJa1ZqAwWA5oQWfD3ZEr5MTvNofuUAAYoAAislAALub4hXaV1eM-iaeoY7BA")
BOT_FANCY_NAME = getenv("BOT_FANCY_NAME", "- 𝐃ιƙʂԋαꭙ ϻᴜsɪc")
WEBSITE_URL = getenv("WEBSITE_URL", "https://nex0-1.vercel.app")
OWNER_USERNAME = getenv("OWNER_USERNAME", "Kaito_3_2")
OWNER_NAME = getenv("OWNER_NAME", "- 𝐃ιƙʂԋα")

LOGGER_ID = getenv_int("LOGGER_ID", -1003639584506)
OWNER_ID = getenv_int("OWNER_ID", 6356015122)

PLAYER_VIDEO = "https://files.catbox.moe/qxj5y2.mp4"

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/SUDEEPBOTS/MYRDLMUSIC")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dissertsoul")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+NNVeQYHwW0JlYmM9")
SUPPORT_GROUP = "https://t.me/+NNVeQYHwW0JlYmM9"

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = getenv_int("ASSISTANT_LEAVE_TIME", 9000)
SONG_DOWNLOAD_DURATION = getenv_int("SONG_DOWNLOAD_DURATION", 9999999)
SONG_DOWNLOAD_DURATION_LIMIT = getenv_int("SONG_DOWNLOAD_DURATION_LIMIT", 9999999)

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

PLAYLIST_FETCH_LIMIT = getenv_int("PLAYLIST_FETCH_LIMIT", 25)

TG_AUDIO_FILESIZE_LIMIT = getenv_int("TG_AUDIO_FILESIZE_LIMIT", 5242880000)
TG_VIDEO_FILESIZE_LIMIT = getenv_int("TG_VIDEO_FILESIZE_LIMIT", 5242880000)

DIGAN_1 = "https://i.ibb.co/KcJthYDj/Screenshot-20260409-201341-Telegram.png"
DIGAN_2 = "https://i.ibb.co/B5Xw1YGm/Screenshot-20260409-175833-Telegram.png"
DIGAN_3 = "https://i.ibb.co/vSx43my/Screenshot-20260409-201606-Telegram.png"
DIGAN_4 = "https://i.ibb.co/v4G7bnJR/Screenshot-20260409-201714-Telegram.png"

STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")
STRING6 = getenv("STRING_SESSION6")
STRING7 = getenv("STRING_SESSION7")

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/ah5y0f.jpeg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/gbl1oi.jpeg")
PLAYLIST_IMG_URL = "https://files.catbox.moe/ndqvqk.jpg"
STATS_IMG_URL = "https://files.catbox.moe/do3vuz.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/2vq8oz.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/2vq8oz.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/2vq8oz.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/2vq8oz.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/2vq8oz.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/2vq8oz.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/2vq8oz.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/2vq8oz.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
