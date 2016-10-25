# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from ferret.cleaner.cleaner import clean_body
from ferret.cleaner.text import normalize_text
from ferret.util.parser.parser import extract_sorted_keywords_from_url
from ferret.util.parser.title import get_title_element_candidates, calculate_weights_of_candidates, \
    get_open_graph_title_text, get_title_text_from_title_tag


class UrlTitleExtractor:
    def __init__(self, url, html):
        self.url = url
        self.soup = BeautifulSoup(html, 'lxml')

    def extract(self):
        keywords = extract_sorted_keywords_from_url(self.url)
        if not keywords or not str(self.soup.body):
            return None

        title = self.get_best_candidate(keywords)
        return normalize_text(title)

    def get_best_candidate(self, keywords):
        candidates_weights = self._get_candidates_weights()
        for candidate, weight in candidates_weights.items():
            candidates_weights[candidate] += self._calculate_title_weight_by_keyword_matching(candidate, keywords)
        candidates = list(sorted(candidates_weights, key=candidates_weights.__getitem__, reverse=True))
        return candidates[0]

    def _get_candidates_weights(self):
        title_candidates = get_title_element_candidates(self.soup)
        return calculate_weights_of_candidates(title_candidates)

    def _calculate_title_weight_by_keyword_matching(self, candidate, keywords):
        title_words = candidate.lower().split(" ")
        keywords = [x.lower() for x in keywords]
        weight = 0
        for i, key in enumerate(keywords):
            if key in title_words:
                weight += 1
        return weight


class OpenGraphTitleExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def extract(self):
        return get_open_graph_title_text(self.soup)


class TitleElementExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def extract(self):
        return get_title_text_from_title_tag(self.soup)


class TagTitleExtractor:
    def __init__(self, html):
        self.cleaned_soup = BeautifulSoup(clean_body(html), 'lxml')
        self.soup = BeautifulSoup(html, 'lxml')

    def extract(self):
        title_element_candidates = get_title_element_candidates(self.cleaned_soup)
        if not title_element_candidates:
            return None

        if len(title_element_candidates) == 1:
            return title_element_candidates[0].text

        title_weights = calculate_weights_of_candidates(title_element_candidates)
        title_weights = self._calc_by_title_tag(title_weights)
        return self._choose_best_candidate(title_weights)

    def _calc_by_title_tag(self, title_weights):
        title_text = get_title_text_from_title_tag(self.soup)
        if not title_text:
            return title_weights

        for title, weight in title_weights.items():
            title_keywords = [k for k in title_text.split() if k != '']
            title_candidate_keywords = [t for t in title.split() if t != '']
            if set(title_keywords).intersection(title_candidate_keywords):
                new_weight = title_weights.get(title) + 1
                title_weights[title] = new_weight

        return title_weights

    def _choose_best_candidate(self, title_weights):
        candidades_weight = self._filter_less_evaluated_candidates(title_weights)
        if len(candidades_weight) == 1:
            return list(candidades_weight)[0]
        return self._choose_candidate_by_length(title_weights)

    def _filter_less_evaluated_candidates(self, title_weights):
        t_w = title_weights.copy()
        ordered_candidates = sorted(title_weights, key=title_weights.__getitem__, reverse=True)

        highest_value = title_weights[ordered_candidates[0]]
        for k, v in title_weights.items():
            if title_weights[k] < highest_value:
                del (t_w[k])

        return t_w

    def _choose_candidate_by_length(self, title_weights):
        candidates = list(title_weights)
        max_length_candidate = max(candidates, key=len)
        print(max_length_candidate)
        return max_length_candidate.strip()
