from os import environ
from pymongo import MongoClient
from logging import StreamHandler, getLogger, basicConfig, ERROR, INFO
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv, dotenv_values
from os.path import exists
from os import system, getcwd, remove
from sys import exit
from subprocess import run as subprocess_run
from shutil import rmtree


###############------init aria------###############
subprocess_run(["chmod", "+x", "aria.sh"])
subprocess_run("./aria.sh", shell=True)

###############------Logging------###############
# if exists("Logging.txt"):
#     with open("Logging.txt", "r+") as f_d:
#         f_d.truncate(0)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "Logging.txt", maxBytes=50000000, backupCount=10, encoding="utf-8"
        ),
        StreamHandler(),
    ],
)

getLogger("telethon").setLevel(ERROR)
getLogger("pyrogram").setLevel(ERROR)
LOGGER = getLogger()


###############------Import_Config------###############
if not exists('./userdata/botconfig.env'):
    CONFIG_FILE_URL = environ.get("CONFIG_FILE_URL", False)
    if CONFIG_FILE_URL and str(CONFIG_FILE_URL).startswith("http"):
        LOGGER.info(f"🔶Downloading Config File From URL {CONFIG_FILE_URL}")
        system(f"wget -O config.env {str(CONFIG_FILE_URL)}")
    if exists('config.env'):
        LOGGER.info(f"🔶Importing Config File")
        load_dotenv('config.env')
else:
    LOGGER.info(f"🔶Importing Bot Config File")
    env_dict = dict(dotenv_values("./userdata/botconfig.env"))
    for key in env_dict:
        environ[key] = str(env_dict[key])


###############------Get_Data_From_MongoDB------###############
def get_mongo_data(MONGODB_URI, BOT_USERNAME, id, colz):
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[BOT_USERNAME]
        col = mongo_db[colz]
        LOGGER.info(f"🔶Getting Data From Database From MongoDB With Database Name {BOT_USERNAME} And ID {id}")
        item_details = col.find({"id" : id})
        data = False
        for item in item_details:
                data = item.get('data')
        if data:
            LOGGER.info("🟢Data Found In Database")
            return data
        else:
            LOGGER.info("🟡Data Not Found In Database")
            return "{}"


###############------Config_Section------###############
class Config:
    VERSION = '3.0'
    try:
        API_ID = int(environ.get("API_ID","10811400"))
    except:
        LOGGER.info("🔶Invalid Config")
        if exists('./userdata/botconfig.env'):
            remove('./userdata/botconfig.env')
        exit()
    API_HASH = environ.get("API_HASH","191bf5ae7a6c39771e7b13cf4ffd1279")
    TOKEN = environ.get("TOKEN","6570881117:AAF3ulbA0ztNfF1rSdp7cb5nZ_4hzIDAm5U")
    USE_PYROGRAM = True
    USE_SESSION_STRING = environ.get("USE_SESSION_STRING", False)
    SESSION_STRING = environ.get("SESSION_STRING","")
    RUNNING_TASK_LIMIT = int(environ.get("RUNNING_TASK_LIMIT","10"))
    AUTO_SET_BOT_CMDS = eval(environ.get("AUTO_SET_BOT_CMDS","False"))
    HEROKU_APP_NAME = environ.get("HEROKU_APP_NAME", False)
    HEROKU_API_KEY = environ.get("HEROKU_API_KEY", False)
    FINISHED_PROGRESS_STR = environ.get("FINISHED_PROGRESS_STR", '■')
    UNFINISHED_PROGRESS_STR = environ.get("UNFINISHED_PROGRESS_STR", '□')
    TIMEZONE = environ.get("TIMEZONE", 'Asia/Kolkata')
    try:
        AUTH_GROUP_ID = int(environ.get("AUTH_GROUP_ID","-1001913031994"))
    except:
        LOGGER.info("🔶Auth Group ID Not Found, Pyrogram Download and Upload Will Not Work In Group")
        AUTH_GROUP_ID = False
    NAME = "Nik66Bots"
    DOWNLOAD_DIR = f"{getcwd()}/downloads"
    OWNER_ID = int(environ.get("OWNER_ID","6469754522"))
    SUDO_USERS = [int(x) for x in environ.get("SUDO_USERS","6469754522").split(" ")]
    ALLOWED_CHATS = SUDO_USERS.copy()
    SAVE_TO_DATABASE = eval(environ.get("SAVE_TO_DATABASE","True"))
    if SAVE_TO_DATABASE:
        MONGODB_URI = environ.get("MONGODB_URI","mongodb+srv://NEWMULTI24BOT:NEWMULTI24BOT@cluster0.vcgihkj.mongodb.net/?retryWrites=true&w=majority")
        COLLECTION_NAME = "USER_DATA"
        SAVE_ID = "Nik66"
        DATA = eval(get_mongo_data(MONGODB_URI, NAME, SAVE_ID, COLLECTION_NAME))
    else:
        LOGGER.info("🔶Not Using MongoDB Database")
        DATA = {}
    LOGGER = LOGGER
    try:
        RESTART_NOTIFY_ID = int(environ.get("RESTART_NOTIFY_ID","-1001534512063"))
        LOGGER.info("🔶Restart Notification ID Found")
    except:
        RESTART_NOTIFY_ID = False
        LOGGER.info("🔶Restart Notification ID Not Found")


if exists(Config.DOWNLOAD_DIR):
    LOGGER.info("🔶Clearing Download Directory.")
    rmtree(Config.DOWNLOAD_DIR)
