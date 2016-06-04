# -*- coding: utf-8 -*-
import re


def extract_sorted_keywords_in_url(url):
    title_by_hyphens = re.search(r'(\w*-(-*)?\w+)+', url)
    if title_by_hyphens is None or len(title_by_hyphens.group()) == 0:
        return None
    keywords = title_by_hyphens.group().split('-')  # stop words tend to have less characters
    cleaned_keywords = [x for x in keywords if x != '']  # the list might have empty entries
    cleaned_keywords.sort(key=len, reverse=True)
    return cleaned_keywords
