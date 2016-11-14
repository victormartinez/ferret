# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from ferret.cleaner.cleaner import Cleaner
from ferret.cleaner.tag import remove_unnecessary_attributes, has_only_one_anchor
from urllib.parse import urljoin


class ContentExtractor:
    def __init__(self, context):
        self.context = context
        self.cleaner = Cleaner(context.get('html'))
        self.divToP = re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)", re.I)

    def extract(self):
        cleaned_html = self.cleaner.get_cleaned_body()
        body = self._convert_divs_to_paragraph(cleaned_html)
        body = self._remove_parent_tags(body)
        body = self._label_tags_with_scores(body)
        body = self._remove_elements_by_score(body)
        body = self._remove_title_candidates(body)
        body = self._clean_up_attributes(body)
        body = self._fix_image_paths(body)
        body = self._label_tags_should_keep(body)
        # body = self._remove_unnecessary_paragraphs(body)
        # body = self._format_into_paragraphs(body)
        return self._get_final_content(body)

    def _convert_divs_to_paragraph(self, html):
        soup = BeautifulSoup(html, 'lxml')
        for elem in soup.body.find_all(True):
            if elem.name == 'div':
                s = elem.encode_contents()
                if not self.divToP.search(s.decode()):
                    elem.name = 'p'
        return soup.body

    def _remove_parent_tags(self, body):
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

            tags = ['body', 'html', '[document]', 'article', 'b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'figcaption', 'figure', 'picture']
            if parent_word_ratio == tag_word_ratio and parent_tag.name not in tags:
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
        for p in body.find_all('p'):
            does_not_have_children = len(p.find_all(True)) == 0
            if does_not_have_children and p.attrs.get('punctuation') == 0.0:
                p.extract()

        for tag in body.find_all('span'):
            if tag.parent.name in ['article', 'body'] and tag.attrs.get('punctuation') == 0:
                tag.extract()

        # for tag in body.find_all('div'):
        #     parag_ratio = tag.attrs['paragraphs']
        #     if parag_ratio == 0:
        #         tag.extract()
        #
        # for p in body.find_all('p'):
        #     punct_ratio = p.attrs['punctuation']
        #     if punct_ratio == 0 and not p.select('b, strong, h1, h2, h3, h4, h5, h6') and len(p.text) < 25:
        #         p.extract()

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

    # def _format_into_paragraphs(self, body):
    #     soup = BeautifulSoup(str(body), 'html5lib')
    #     # figcaption, span, caption
    #     for tag in soup.select('figure,picture,img'):
    #         if (tag.parent.name != 'p' or tag.parent.parent.name != 'p') and (tag.parent.name not in ['figure', 'picture', 'img']):
    #             new_tag = soup.new_tag("p")
    #             tag.wrap(new_tag)
    #
    #             next_tag = tag.find_next()
    #             if next_tag and next_tag.name in ['span', 'caption', 'figcaption']:
    #                 new_tag.append(next_tag)
    #
    #     return soup.body

    def _remove_unnecessary_paragraphs(self, body):
        for p in body.find_all('p'):
            if has_only_one_anchor(p):
                p.extract()
        return body

    def _get_final_content(self, body):
        elements = [e for e in body.find_all(True, {'class': 'keep-tag'})]
        parags = ''
        for e in elements:
            remove_unnecessary_attributes(e)
            parags += str(e)
        return parags

    def _label_tags_should_keep(self, body):
        for tag in body.find_all(True):
            if tag.name == 'p':
                tag.attrs.update({'class': 'keep-tag'})

            if tag.parent.name == 'p':
                continue

            if tag.parent.name in ['caption', 'figcaption', 'figure', 'picture', 'img']:
                continue

            if tag.name in ['caption', 'figcaption', 'figure', 'picture', 'img']:
                tag.attrs.update({'class': 'keep-tag'})

            prev_sibling = tag.find_previous_sibling()
            if prev_sibling and prev_sibling.name in ['caption', 'figcaption', 'figure', 'picture', 'img']:
                tag.attrs.update({'class': 'keep-tag'})

        return body

    def _fix_image_paths(self, body):
        for img in body.select('img'):
            src = img.attrs['src']
            source = urljoin(self.context.get('url'), src)
            img.attrs['src'] = source

        for anchor in body.select('a'):
            href = anchor.attrs['href']
            source = urljoin(self.context.get('url'), href)
            anchor.attrs['href'] = source
        return body
