import random
from requests_html import HTMLSession, HTML

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from docx import Document
from docx.document import Document as Doc
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.shared import Pt
from docx.oxml.ns import qn

start_url = "https://www.runoob.com/"
LANGUAGE = "chinese"
SENTENCES_COUNT = 50

str_replace = [
    ["您", ""],
    ["你", ""],
    ["我们", "我"],
    ["教程", "笔记"],
    ["尝试一下 » ", ""],
]


def refresh_datetime():
    global date, month, max_date
    date += 1
    if date > max_date:
        date = 1
        month += 1


def generate_text_list(url):
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    # parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    paragraph_list = []
    build_str = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        build_str += str(sentence)
        if random.random() < 0.5:
            paragraph_list.append(str_processing(build_str))
            build_str = ""
    return paragraph_list


def get_next_url(last_page_url):
    session = HTMLSession()
    r = session.get(last_page_url)
    html = HTML(html=r.text)
    next_link = html.find(".next-design-link", first=True)
    if len(next_link.absolute_links) == 0:
        return None
    print(next_link.text, next_link.absolute_links)
    for next_url in next_link.absolute_links:
        return next_url


def get_topic_url_set(home_url):
    url_set = set()
    session = HTMLSession()
    r = session.get(home_url)
    html = HTML(html=r.text)
    item_list = html.find(".item-1")
    for item in item_list:
        for url in item.absolute_links:
            url_set.add(url)
    return url_set


def str_processing(s):
    for each in str_replace:
        s = s.replace(each[0], each[1])
    return s


if __name__ == '__main__':
    # init doc
    doc: Doc
    doc = Document()
    styles = doc.styles
    style = styles.add_style("表头", WD_STYLE_TYPE.PARAGRAPH)
    style.hidden = False
    style.quick_style = True
    style.priority = 1

    print("正在爬取网页：")
    topic_url_set = get_topic_url_set(start_url)
    page_url = get_next_url(topic_url_set.pop())
    text_len = 0
    while text_len < 40000:
        # input text
        while page_url is None:
            # find another topic
            page_url = get_next_url(topic_url_set.pop())
        for text in generate_text_list(page_url):
            text_len += len(text)
            doc.add_paragraph(text)
        # goto next webpage
        page_url = get_next_url(page_url)
    doc.save("real internship report.docx")
