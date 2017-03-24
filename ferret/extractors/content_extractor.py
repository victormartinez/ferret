# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import re
from bs4 import BeautifulSoup, Comment
from ferret.cleaner.tag import has_only_one_anchor, remove_unnecessary_attributes
from ferret.cleaner.text import remove_special_chars
from ferret.util.tag import get_ids_and_classes

TAGS_TO_REMOVE = ['script', 'style', 'iframe', 'meta', 'link', 'form', 'noscript', 'object', 'source',
                  'svg', 'use', 'code', 'pre', 'input', 'textarea', 'option', 'select', 'fieldset', 'aside', 'menuitem',
                  'nav', 'footer', 'hr', 'ins', 'button']

UNWANTED_ATTRS_REGEX = "sidebar|widget|social|facebook|comment|tweet|menu|footer|subscribe|foot|nav|google|share|search" \
                       "|form|contact|breadcrumb|banner|advertis|lang|btn|tab|sitemap|instagram|flickr|print" \
                       "|button|pinterest|radio|bread|icon|dusqus|sponsor|popup|modal|pagination" \
                       "|related|scroll|tool|login|sign|next|prev|shop|continue|fb-|messenger|header|meta|twitter|rss|keyword|credit|plugin"

"""
The process of converting divs to paragraphs is inherited from python-goose's code. See the license:
https://github.com/victormartinez/ferret/blob/master/GOOSE-LICENSE.txt
"""


class ContentExtractor:
    def __init__(self, context):
        self.context = context
        self.div_to_p = re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)", re.I)

    def is_suitable(self):
        return True

    def extract(self):
        body = BeautifulSoup(self.context.get('html'), 'html5lib').body
        body = self._remove_unwanted_tags(body)
        body = self._remove_comments(body)
        body = self._convert_elements_to_paragraph(body)
        body = self._label_tags_with_scores(body)
        body = self._choose_by_density(body)
        body = self._remove_by_score(body)
        body = self._remove_noisy_tags(body)
        body = self._remove_redundant_blocks(body)
        body = self._remove_unwanted_tags(body)
        body = self._clean_scores(body)
        body = self._clean_up_attributes(body)
        body = self._remove_title_from_text(body, self.context.get('title'))
        body = self._fix_image_paths(body)
        return remove_special_chars(str(body))

    def _remove_unwanted_tags(self, body):
        for elem in body.select(','.join(TAGS_TO_REMOVE)):
            elem.decompose()
        return body

    def _remove_comments(self, body):
        comments = body.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        return body

    def _convert_elements_to_paragraph(self, body):
        for elem in body.find_all(True):
            if elem.name == 'div':
                s = elem.encode_contents()
                if not self.div_to_p.search(s.decode()):
                    elem.name = 'p'

            if elem.name == 'font':
                elem.name = 'p'

        return body

    def _label_tags_with_scores(self, body):
        for tag in body.find_all(True):
            scores = {
                'anchor': self._get_anchor_ratio(tag),
                'punctuation': self._get_punctuation_ratio(tag),
                'words': len(tag.text.split()),
                'sentences': len(tag.text.split('.')) - 1,
                'paragraphs': len(tag.select('p'))
            }
            if tag.attrs:
                tag.attrs.update(scores)
            else:
                tag.attrs = scores
        return body

    def _get_anchor_ratio(self, tag):
        text_length = len(remove_special_chars(tag.text))
        anchors_length = sum(len(remove_special_chars(a.text)) for a in tag.find_all('a'))

        if anchors_length == 0:
            return 0
        return round(anchors_length / float(text_length), 4)

    def _get_punctuation_ratio(self, tag):
        tag_text = remove_special_chars(tag.text)

        words_count = len(tag_text.split())
        punct_count = sum(tag_text.count(symbol) for symbol in ['.', ',', '!', '?', ':', ';'])

        if words_count == 0:
            return 0
        return round(punct_count / float(words_count), 4)

    def _choose_by_density(self, body):
        candidate = None
        for tag in body.find_all(True):
            if not candidate:
                candidate = tag
                continue

            candidate_sentences = candidate.attrs.get('sentences')
            tag_sentences = tag.attrs.get('sentences')
            if candidate_sentences < tag_sentences:
                candidate = tag
                continue

            candidate_punctuation = candidate.attrs.get('punctuation')
            tag_punctuation = tag.attrs.get('punctuation')
            if candidate_sentences == tag_sentences:
                if candidate_punctuation < tag_punctuation:
                    candidate = tag

        if candidate:
            return candidate
        return body

    def _remove_by_score(self, body):
        highest_sentence_score = 0
        for elem in body.select('div'):
            attrs = elem.attrs
            if not attrs:
                continue

            if attrs.get('sentences') > highest_sentence_score:
                highest_sentence_score = attrs.get('sentences')

        for elem in body.select('div'):
            attrs = elem.attrs
            if not attrs:
                continue

            if attrs.get('anchor') > 0.6 and ((attrs.get('sentences') / highest_sentence_score) <= 0.1):
                elem.decompose()

            if attrs.get('words') == 0:
                elem.decompose()

        for p in body.select('p'):
            not_contains_article_element = not len(p.select('b, strong, h1, h2, h3, h4, h5, h6, img, figure, picture'))
            not_contains_text = not len(p.text)
            if not_contains_article_element and not_contains_text:
                p.extract()

            attrs = p.attrs
            if not attrs:
                continue

            if attrs.get('paragraphs') == 0 and not_contains_text and not_contains_article_element and not p.a:
                p.extract()

        return body

    def _remove_noisy_tags(self, body):
        again = False
        for tag in body.find_all(True):
            if tag.name in ['img', 'figure', 'figcaption', 'caption', 'picture']:
                continue

            if self.__should_remove(tag):
                again = True
                tag.extract()

            not_contains_text = len(tag.text.strip()) == 0
            not_contains_img = len(tag.find_all('img')) == 0
            if not_contains_text and not_contains_img:
                again = True
                tag.extract()

            if tag.is_empty_element:
                again = True
                tag.extract()

            if has_only_one_anchor(tag) and tag.parent and tag.parent.name != 'p':
                again = True
                tag.extract()

        if again:
            return self._remove_noisy_tags(body)
        return body

    def __should_remove(self, tag):
        should = False
        attrs = get_ids_and_classes(tag)
        for attr in attrs:
            if re.search(UNWANTED_ATTRS_REGEX, attr):
                should = True

        return should

    def _remove_redundant_blocks(self, body):
        articles = body.select('article')
        if len(articles) >= 1:
            return BeautifulSoup(str(articles[0]), 'lxml').body
        return body

    def _clean_scores(self, body):
        for tag in body.find_all(True):
            keys = list(tag.attrs.keys())
            for attr in keys:
                if attr in ['words', 'anchor', 'sentences', 'punctuation', 'paragraphs']:
                    del tag.attrs[attr]
        return body

    def _clean_up_attributes(self, body):
        for e in body.find_all(True):
            remove_unnecessary_attributes(e)
        return body

    def _remove_title_from_text(self, body, title_str):
        if not title_str:
            return body

        found = body.find(text=title_str)
        if found:
            found.extract()
        else:
            h1 = body.select_one('h1')
            if h1:
                h1.extract()
        return body

    def _fix_image_paths(self, body):
        for img in body.select('img'):
            src = img.attrs.get('src', None)
            if src:
                source = urljoin(self.context.get('url'), src)
                img.attrs['src'] = source

        for anchor in body.select('a'):
            href = anchor.attrs.get('href', None)
            if href:
                source = urljoin(self.context.get('url'), href)
                anchor.attrs['href'] = source
        return body


def extract_body_text_from_html(html):
    body = BeautifulSoup(html, 'lxml').body
    for elem in body.select('script,style,link,source'):
        elem.extract()
    return remove_special_chars(str(body.get_text()))


def simple_clean(html):
    body = BeautifulSoup(html, 'lxml').body
    for elem in body.select('script,style,link,source'):
        elem.extract()
    return remove_special_chars(str(body))
