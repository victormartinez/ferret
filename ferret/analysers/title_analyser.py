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


def calculate_title_weight_by_tag(title_candidates):
    title_weight = {}
    for candidate in title_candidates:
        if candidate.get_text() and DEFAULT_TITLE_WEIGHTS[candidate.name]:
            title_weight[candidate.get_text().strip()] = DEFAULT_TITLE_WEIGHTS.get(candidate.name)
    return title_weight


def calculate_title_weight_by_keyword_matching(title, keywords):
    title_words = title.lower().split(" ")
    keywords = [x.lower() for x in keywords]
    weight = 0
    for i, key in enumerate(keywords):
        if key in title_words:
            weight += 1
    return weight
