# -*- coding: utf-8 -*-
import re


def extract_sorted_keywords_in_url(url):
    title_by_hyphens = re.findall(r'(\w*-(-*)\w+)', url, re.M | re.I)
    if len(title_by_hyphens or '') == 0:
        return None

    keywords = []
    for index, tuple in enumerate(title_by_hyphens):
        (first_match, second_match) = tuple
        words = first_match.split('-')
        cleaned_keywords = [x for x in words if x != '-' and x != ''] # the list might have empty entries
        keywords.extend(cleaned_keywords)

    return keywords
