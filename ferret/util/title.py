# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from toolz import dicttoolz

DEFAULT_TITLE_WEIGHTS = {
    'h1': 8,
    'h2': 7,
    'h3': 6,
    'h4': 5,
    'h5': 4,
    'h6': 3,
    'b': 0,
    'strong': 0
}


def get_title_element_candidates(html):
    soup = BeautifulSoup(html, 'lxml').body
    tags = ",".join(DEFAULT_TITLE_WEIGHTS.keys())
    elements = soup.select(tags)
    for e in elements:
        anchor = e.select('a')
        if len(anchor) > 1:
            elements.remove(e)
        if len(e.text) == 1:
            elements.remove(e)
    return [e for e in elements if len(e.get_text().strip())]


def get_text_from_dc_title_tag(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    title = soup.select_one("meta[dc:title]")
    if title:
        return title.text
    return ''


def get_text_from_meta_title(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    title = soup.select_one("meta[name=title]")
    if title and title.get('content'):
        return title.get('content').strip()
    return None


def get_score_candidates(html):
    elements = get_title_element_candidates(html)
    title_score = {}
    for candidate in elements:
        title_score[candidate.get_text().strip()] = DEFAULT_TITLE_WEIGHTS.get(candidate.name)
    return dicttoolz.keyfilter(lambda k: len(k), title_score)
