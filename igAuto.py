from instagrapi import Client
import schedule
import time
import random
import logging
from datetime import datetime
# ---------------------------
# CONFIGURATION
# ---------------------------
USERNAME = "your_username"
PASSWORD = "your_password"
HASHTAGS = ["nature", "travel", "photography", "art", "food", "fitness"]
PHOTO_PATH = "photo.jpg"
CAPTION = "Hello, Instagram! #automation"
LIKE_MIN = 3
LIKE_MAX = 8
FOLLOW_MIN = 2
FOLLOW_MAX = 5
DELAY_MIN = 4   # min delay between actions (seconds)
DELAY_MAX = 10  # max delay between actions (seconds)

LOG_FILE = "insta_bot_log.txt"
DAY_START = 8    # 8 AM
DAY_END = 22     # 10 PM
# ---------------------------
# SETUP LOGGING
# ---------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# ---------------------------
# LOGIN
# ---------------------------
cl = Client()
try:
    cl.login(USERNAME, PASSWORD)
    logging.info("Logged in successfully")
except Exception as e:
    logging.error(f"Login failed: {e}")
    exit()
# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def human_delay():
    time.sleep(random.randint(DELAY_MIN, DELAY_MAX))
def like_posts():
    selected_hashtag = random.choice(HASHTAGS)
    like_amount = random.randint(LIKE_MIN, LIKE_MAX)
    logging.info(f"Liking {like_amount} posts for #{selected_hashtag}")
    try:
        medias = cl.hashtag_medias_recent(selected_hashtag, amount=like_amount)
        for media in medias:
            cl.media_like(media.id)
            logging.info(f"Liked post: {media.pk}")
            human_delay()
    except Exception as e:
        logging.error(f"Error liking posts for #{selected_hashtag}: {e}")
def follow_users():
    selected_hashtag = random.choice(HASHTAGS)
    follow_amount = random.randint(FOLLOW_MIN, FOLLOW_MAX)
    logging.info(f"Following {follow_amount} users for #{selected_hashtag}")
    try:
        medias = cl.hashtag_medias_recent(selected_hashtag, amount=follow_amount)
        for media in medias:
            cl.user_follow(media.user.pk)
            logging.info(f"Followed user: {media.user.username}")
            human_delay()
    except Exception as e:
        logging.error(f"Error following users for #{selected_hashtag}: {e}")
def upload_photo():
    if random.random() < 0.5:  # 50% chance to post a photo each session
        try:
            cl.photo_upload(PHOTO_PATH, CAPTION)
            logging.info(f"Photo uploaded successfully: {PHOTO_PATH}")
        except Exception as e:
            logging.error(f"Failed to upload photo: {e}")
def is_daytime():
    now = datetime.now().hour
    return DAY_START <= now < DAY_END
def run_all_tasks():
    if is_daytime():
        logging.info("Starting human-like Instagram automation")
        like_posts()
        follow_users()
        upload_photo()
        logging.info("Completed this session")
    else:
        logging.info("Outside daytime hours. Skipping automation.")
# ---------------------------
# SCHEDULING
# ---------------------------
# Run the bot at random intervals between 3 to 6 hours
def schedule_next_run():
    next_run_hours = random.randint(3, 6)
    logging.info(f"Next run scheduled in {next_run_hours} hours")
    schedule.clear()
    schedule.every(next_run_hours).hours.do(run_all_tasks).tag("automation")
# Initial scheduling
schedule_next_run()
run_all_tasks()  # run once at start
# ---------------------------
# KEEP SCRIPT RUNNING
# ---------------------------
while True:
    schedule.run_pending()
    time.sleep(60)
