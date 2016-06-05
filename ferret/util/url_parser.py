# -*- coding: utf-8 -*-
import dateparser
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

    return keywords


def extract_date_from_url(url):
    published_date = re.search(r'(\d{4}/\d{2}/\d{2})/', url)
    if not published_date:
        return None

    extracted_date = published_date.group()
    return dateparser.parse(extracted_date, languages=['en'])  # date format used by blogs follow the american pattern
