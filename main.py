import os
import re

import numpy as np

from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from wordcloud_fa import WordCloudFa
from twython import Twython

GENERAL_MASK_IMAGE_PATH = '/Users/OmidKia/Documents/twitter_word_cloud/general.png'
NIKE_MASK_IMAGE_PATH = '/Users/OmidKia/Documents/twitter_word_cloud/nike.png'
FINGER_MASK_IMAGE_PATH = '/Users/OmidKia/Documents/twitter_word_cloud/finger.png'
TWITTER_MASK_IMAGE_PATH = '/Users/OmidKia/Documents/twitter_word_cloud/03-twitter-512.png'
PERSIAN_STOPWORDS = set(map(str.strip, open(os.path.join('/Users/OmidKia/Documents/twitter_word_cloud/persian_stopwords')).readlines()))


def init():
    username: str = input("Enter username: ")
    timeline_count: int = int(input("Enter timeline count: "))
    print("Please wait...")
    raw_string = initiate_raw_string(username=username, timeline_count=timeline_count)
    # regex = create_regex(raw_string=raw_string)
    regex = create_regex_fa(raw_string=raw_string)
    words = trim_words(regex)
    # finalize(words=words)
    finalize_fa(words=words)


def initiate_raw_string(username, timeline_count):
    APP_KEY = "3QHyJeJ39qDMwwRimrb5dBPI6"
    APP_SECRET_KEY = "JVSRJmozriLjf7xfzOCR8XzyAvQSR7buz1FaC14zeI8g13dCiI"
    twitter = Twython(app_key=APP_KEY, app_secret=APP_SECRET_KEY)
    user_timeline = twitter.get_user_timeline(screen_name=username, count=1)
    last_id = user_timeline[0]['id'] - 1
    for i in range(16):
        batch = twitter.get_user_timeline(screen_name=username, count=timeline_count, max_id=last_id)
        user_timeline.extend(batch)
        last_id = user_timeline[-1]['id'] - 1

    raw_tweets = []
    for tweets in user_timeline:
        raw_tweets.append(tweets['text'])

    raw_string = ''.join(raw_tweets)
    return raw_string


def create_regex_fa(raw_string):
    print("raw string =", raw_string)
    no_links = re.sub(r'http\S+', '', raw_string)
    no_special_characters = re.sub('[^\u0621-\u0624\u0626-\u063A\u0641-\u0642\u0644-\u0648\u064B-\u0652\u067E\u0686'
                                   '\u0698\u06AF\u06CC\u06A9\u0654\u0670\u200c} ]+', '', no_links)
    print("regex = ", no_special_characters)
    return no_special_characters


def create_regex(raw_string):
    print("raw string =", raw_string)
    no_links = re.sub(r'http\S+', '', raw_string)
    no_unicode = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
    regex = re.sub('[^A-Za-z ]+', '', no_links)
    print("regex = ", regex)
    return regex


def trim_words(regex):
    words = regex.split(" ")
    words = [w for w in words if len(w) > 3]  # ignore a, an, be, ...
    words = [w.lower() for w in words]
    words = [w for w in words if w not in PERSIAN_STOPWORDS]
    print("words length=", words.__len__())
    print("words =", words)
    clear_string = " ".join(words)
    print("clear_string=", clear_string.__len__())
    print("clear_string =", clear_string)
    return clear_string


def mask_with_image(image_path):
    mask = np.array(Image.open(image_path))
    return mask


def finalize(words):
    mask = mask_with_image(TWITTER_MASK_IMAGE_PATH)
    wc = WordCloud(mask=mask, background_color="white")
    clean_string = ','.join(words)
    print("clean string =", clean_string)
    wc.generate(clean_string)
    image = wc.to_image()
    image.save('wordcloud.png')
    image.show()
    print("Operation completed")


def finalize_fa(words):
    mask = mask_with_image(FINGER_MASK_IMAGE_PATH)
    stop_words = set(PERSIAN_STOPWORDS)
    wc = WordCloudFa(persian_normalize=True,
                     mask=mask,
                     no_reshape=False,
                     background_color="white",
                     include_numbers=False,
                     max_words=5000,
                     width=2000,
                     height=4000)
    wc.add_stop_words(stop_words)
    wc.generate(words)
    image = wc.to_image()
    filename: str = input("Enter file name: ")
    image.save(filename + '.png')
    image.show()
    print("Operation completed")


if __name__ == '__main__':
    init()
