# -*- coding: utf-8 -*-

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


def get_title_element_candidates(soup):
    tags = ",".join(DEFAULT_TITLE_WEIGHTS.keys())
    elements = soup.body.select(tags)
    for e in elements:
        if e.select('a'):
            elements.remove(e)
        if len(e.text) == 1:
            elements.remove(e)
    return elements


def get_title_text_from_title_tag(soup):
    titles = soup.select("title")
    if titles:
        return titles[0].text
    return None


def get_open_graph_title_text(soup):
    titles = soup.select('meta[property=og:title]')
    if titles and titles[0]['content']:
        return titles[0]['content'].strip()
    return None


def calculate_weights_of_candidates(title_candidates):
    title_weight = {}
    for candidate in title_candidates:
        if candidate.get_text() and DEFAULT_TITLE_WEIGHTS[candidate.name]:
            title_weight[candidate.get_text().strip()] = DEFAULT_TITLE_WEIGHTS.get(candidate.name)
    return title_weight
