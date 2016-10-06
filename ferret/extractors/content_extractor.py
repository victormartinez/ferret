# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from ferret.cleaner.cleaner import clean_body
from ferret.cleaner.tag import remove_unnecessary_attributes, has_only_one_anchor


class ContentExtractor:
    def __init__(self, html):
        """html, title, """
        self.html_body = clean_body(html)
        self.divToP = re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)", re.I)

    def extract(self):
        body = self._convert_divs_to_paragraph()
        body = self._remove_tags_by_word_ratio(body)
        body = self._label_tags_with_scores(body)
        body = self._remove_elements_by_score(body)
        body = self._remove_title_candidates(body)
        body = self._clean_up_attributes(body)
        body = self._remove_unnecessary_paragraphs(body)
        paragraphs = self._get_paragraphs(body)
        return self._paragraphs_to_string(paragraphs)

    def _convert_divs_to_paragraph(self):
        soup = BeautifulSoup(self.html_body, 'lxml')
        for elem in soup.body.find_all(True):
            if elem.name == 'div':
                s = elem.encode_contents()
                if not self.divToP.search(s.decode()):
                    elem.name = 'p'
        return soup.body

    def _remove_tags_by_word_ratio(self, body):
        number_of_words = len(body.text.split())
        for tag in body.find_all(True):
            parent_tag = tag.parent
            parent_tag_words = len(parent_tag.text.split())
            tag_words = len(tag.text.split())

            parent_word_ratio = 0
            tag_word_ratio = 0
            if number_of_words != 0:
                parent_word_ratio = parent_tag_words / number_of_words
                tag_word_ratio = tag_words / number_of_words

            if parent_word_ratio == tag_word_ratio and parent_tag.name not in ['body', 'html', '[document]', 'article',
                                                                               'b', 'strong', 'h1', 'h2', 'h3', 'h4',
                                                                               'h5', 'h6', 'p', 'a']:
                parent_tag.unwrap()
        return body

    def _label_tags_with_scores(self, body):
        for tag in body.find_all(True):
            tag_text_length = len(tag.text)
            if tag_text_length == 0:
                tag_text_length = 1

            anchors = tag.find_all('a')
            anchor_text_length = 0
            for a in anchors:
                anchor_text_length += len(a.text)

            anchor_ratio = anchor_text_length / tag_text_length
            punctuation_score = tag.text.count('.') + tag.text.count(',') + tag.text.count('!') + tag.text.count('?')
            punct_ratio = 0
            number_of_words = len(tag.text.split())
            if number_of_words != 0:
                punct_ratio = punctuation_score / len(tag.text.split())

            tag.attrs.update(
                {
                    'anchor': round(anchor_ratio, 4),
                    'punctuation': round(punct_ratio, 4),
                    'words': len(tag.text.split()),
                    'sentences': len(tag.text.split('.')),
                    'paragraphs': len(tag.select('p'))
                }
            )
        return body

    def _remove_elements_by_score(self, body):
        for tag in body.find_all('div'):
            parag_ratio = tag.attrs['paragraphs']
            if parag_ratio == 0:
                tag.extract()

        for p in body.find_all('p'):
            punct_ratio = p.attrs['punctuation']
            if punct_ratio == 0 and not p.select('b, strong, h1, h2, h3, h4, h5, h6') and len(p.text) < 25:
                p.extract()

        return body

    def _clean_up_attributes(self, body):
        for e in body.find_all(True):
            remove_unnecessary_attributes(e)
        return body

    def _remove_title_candidates(self, body):
        h1 = body.find('h1')
        if h1:
            h1.extract()
        return body

    def _remove_unnecessary_paragraphs(self, body):
        for p in body.find_all('p'):
            if has_only_one_anchor(p):
                p.extract()
        return body

    def _get_paragraphs(self, body):
        return [p for p in body.find_all('p')]

    def _paragraphs_to_string(self, paragraphs):
        parags = ''
        for p in paragraphs:
            parags += str(p)

        return parags
