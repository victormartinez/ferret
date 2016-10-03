# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from ferret.cleaner.cleaner import clean_body


class ContentExtractor:
    def __init__(self, html):
        """html, title, """
        self.html_body = clean_body(html)
        self.divToP = re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)", re.I)

    def extract(self):
        body = self._convert_divs_to_paragraph()
        body = self._label_tags_with_scores(body)
        body = self._remove_elements_by_score(body)
        body = self._clean_up_scores(body)
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

    def _label_tags_with_scores(self, body):
        count = len(body.text.split())
        for tag in body.find_all(True):

            parent_tag = tag.parent
            palavras_parent = len(parent_tag.text.split())
            palavras = len(tag.text.split())

            word_ratio_parent = 0
            word_ratio = 0
            if count != 0:
                word_ratio_parent = palavras_parent / count
                word_ratio = palavras / count

            if word_ratio_parent == word_ratio and parent_tag.name not in ['body', 'html', '[document]', 'article']:
                parent_tag.unwrap()

        for tag in body.find_all(True):
            anchors = tag.find_all('a')
            text_length = len(tag.text)

            if text_length == 0:
                text_length = 1

            anchor_text_length = 0
            for a in anchors:
                anchor_text_length += len(a.text)

            pontuacao = tag.text.count('.') + tag.text.count(',') + tag.text.count('!') + tag.text.count('?')

            anchor_ratio = anchor_text_length / text_length
            punct_ratio = 0
            words_count = len(tag.text.split())
            if words_count != 0:
                punct_ratio = pontuacao / len(tag.text.split())

            tag.attrs.update(
                {
                    'anchor': round(anchor_ratio, 4),
                    'punct': round(punct_ratio, 4),
                    'words': len(tag.text.split()),
                    'sentences': len(tag.text.split('.')),
                    'parag': len(tag.select('p'))
                }
            )
        return body

    def _remove_elements_by_score(self, body):
        for tag in body.find_all('div'):
            parag_ratio = tag.attrs['parag']
            if parag_ratio == 0:
                tag.extract()

                #     parag_ratio = tag.attrs['parag']
                #     if parag_ratio == 0:
                #         tag.extract()

                # if round(punct_ratio, 4) < 0.1:
                #     tag.extract()

        for p in body.find_all('p'):
            punct_ratio = p.attrs['punct']
            if punct_ratio == 0:
                p.extract()

        return body

    def _clean_up_scores(self, body):
        for e in body.find_all(True):
            for attr in ['anchor', 'punct', 'words', 'sentences', 'parag']:
                del e.attrs[attr]
        return body

    def _get_paragraphs(self, body):
        return [p for p in body.find_all('p')]

    def _paragraphs_to_string(self, paragraphs):
        parags = ''
        for p in paragraphs:
            parags += str(p)

        return parags
