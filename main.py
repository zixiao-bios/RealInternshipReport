from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import keyboard
import random
import time
from requests_html import HTMLSession, HTML

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

start_url = "https://www.runoob.com/"
LANGUAGE = "chinese"
SENTENCES_COUNT = 50

page_num = 78
year = 2021
month = 9
date = 27
max_date = 30


def delete_and_write(content):
    text = str(content)
    for i in range(len(text)):
        keyboard.press_and_release("backspace")
    keyboard.write(text)


def move(direction, distance):
    for i in range(distance):
        keyboard.press_and_release(direction)


def refresh_datetime():
    global date, month, max_date
    date += 1
    if date > max_date:
        date = 1
        month += 1


def generate_paragraph(url):
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    # parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    build_str = "\t"
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        sentence = str(sentence).replace("尝试一下 » ", "")
        if random.random() < 0.5:
            build_str += "\n\t"
        build_str += sentence
    return build_str


def get_second_url_list(first_page_url):
    url = first_page_url
    url_list = [url]
    session = HTMLSession()
    while True:
        r = session.get(url)
        html = HTML(html=r.text)
        next_link = html.find(".next-design-link", first=True)
        if len(next_link.absolute_links) == 0:
            break
        print(next_link.text, next_link.absolute_links)
        for next_url in next_link.absolute_links:
            url = next_url
            url_list.append(url)
    return url_list


def get_first_url_set(home_url):
    url_set = set()
    session = HTMLSession()
    r = session.get(home_url)
    html = HTML(html=r.text)
    item_list = html.find(".item-1")
    for item in item_list:
        for url in item.absolute_links:
            url_set.add(url)
    return url_set


if __name__ == '__main__':
    first_url_set = get_first_url_set(start_url)
    second_url_list = get_second_url_list(first_url_set.pop())
    i = 0
    print("5秒后开始写入……")
    time.sleep(5)
    for i in range(page_num):
        # input datetime
        delete_and_write(year)
        move("right", 4)
        delete_and_write(month)
        move("right", 4)
        delete_and_write(date)
        move("down", 1)
        time.sleep(0.2)

        # input text
        text = ""
        while len(text) < 400:
            if i == len(second_url_list):
                # get new second_url_list and reset i
                second_url_list = get_second_url_list(first_url_set.pop())
                i = 0
            text += generate_paragraph(second_url_list[i])
            i += 1
        keyboard.write(text)
        time.sleep(0.2)

        # move to next page
        move("down", 4)
        move("left", 10)
        time.sleep(0.2)
