# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import re
from bs4 import BeautifulSoup
from ferret.extractors.content_extractor import ContentExtractor
from ferret.cleaner.tag import remove_unnecessary_attributes, has_only_one_anchor


class OldContentExtractor:
    def __init__(self, context):
        self.context = context
        self.cleaner = ContentExtractor(context.get('html'))
        self.divToP = re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)", re.I)

    def extract(self):
        cleaned_html = self.cleaner.get_cleaned_body()


        body = BeautifulSoup(cleaned_html, 'html.parser')
        body = self._remove_title_candidates(body, self.context.get('title'))

        parags = ''
        for p in body.find_all('p'):
            parags += str(p)
        return parags

        # body = self._label_tags_should_keep(body)
        # body = self._remove_elements_by_score(body)
        # body = self._remove_div_sidebards(body)
        # body = self._clean_up_attributes(body)
        # body = self._fix_image_paths(body)
        # body = self._remove_unnecessary_paragraphs(body)
        # body = self._format_into_paragraphs(body)
        # return str(self._get_final_content(body))

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

    def _remove_div_sidebards(self, body):
        for div in body.select("div"):
            style = div.attrs.get('style')
            if not style:
                continue

            is_float = 'float' in style and 'right' in style
            high_anchor_density = div.attrs.get('anchor') > 0.7
            low_punctuation = div.attrs.get('punctuation') < 0.1
            if is_float and high_anchor_density and low_punctuation:
                div.extract()

        return body

    def _clean_up_attributes(self, body):
        for e in body.find_all(True):
            remove_unnecessary_attributes(e)
        return body

    def _remove_title_candidates(self, body, title_candidate_str):
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
        for tag in body.find_all(True):
            attrs = tag.attrs
            if not attrs:
                tag.extract()

            if 'keep-tag' not in str(attrs.get('class')):
                tag.extract()

        # elements = [e for e in body.find_all(True, {'class': 'keep-tag'})]
        # parags = ''
        # for e in elements:
        #     remove_unnecessary_attributes(e)
        #     parags += str(e)
        # print('########')
        # print(parags)
        # print('########')
        return body

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
