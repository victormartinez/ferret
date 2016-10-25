# -*- coding: utf-8 -*-
from math import ceil
from bs4 import BeautifulSoup
from ferret.cleaner.cleaner import clean_body
from scrapely import HtmlPage
import re


def extract_sorted_keywords_from_url(url):
    title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', url, re.M | re.I)
    if len(title_by_hyphens or '') == 0:
        return None

    keywords = []
    for index, tuple in enumerate(title_by_hyphens):
        (first_match, second_match) = tuple
        words = first_match.split('-')
        cleaned_keywords = [x for x in words if x != '-' and x != '']  # the list might have empty entries
        keywords.extend(cleaned_keywords)

    # stop words tend to have less characters
    keywords.sort(key=len, reverse=True)
    return keywords


def extract_text_region_around_title_2(html, title):
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.body.text
    body_length = len(html)
    for index in range(0, body_length):
        if title in html[0:index]:
            return html[0:index + 400]
    return ''


def extract_text_region_around_title(html, title):
    cleaned_html = clean_body(html)
    soup = BeautifulSoup(cleaned_html, 'html.parser')
    body = soup.body
    decoded_body = body.decode()
    body_length = len(decoded_body)
    for index in range(0, body_length):
        partial_html = decoded_body[0:index]
        if title in partial_html:
            return decoded_body[0:index + 700]
    return ''


def extract_text_region_around_title_3(html):
    html_text = clean_body(html)
    html_page = HtmlPage(body=html_text)
    index = ceil(len(html_page.parsed_body) / 3)
    start = html_page.parsed_body[index].start
    end = html_page.parsed_body[(index * 2)].end  # TODO: Analyse the necessity of + ceil(index/2)
    return html_page.body[start:end]
