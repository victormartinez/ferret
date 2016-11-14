# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment
from ferret.cleaner.tag import should_remove_tag, contains_text, \
    has_only_one_anchor
from ferret.cleaner.text import remove_special_chars

TAGS_TO_REMOVE = ['script', 'style', 'iframe', 'meta', 'link', 'form', 'noscript', 'object', 'source',
                  'svg', 'use', 'code', 'pre', 'input', 'textarea', 'option', 'select', 'fieldset', 'aside', 'menuitem',
                  'nav', 'footer', 'hr']

TAGS_TO_UNWRAP = ['font']

UNWANTED_ATTRS_REGEX = "sidebar|widget|social|facebook|comment|tweet|menu|footer|subscribe|foot|nav|google|share|search" \
                       "|form|contact|breadcrumb|banner|advertis|lang|btn|tab|sitemap|instagram|flickr|print" \
                       "|button|pinterest|radio|bread|icon|dusqus|sponsor|popup|modal|pagination" \
                       "|related|scroll|tool|login|sign|next|prev|shop|continue|fb-|messenger|header|meta|twitter|rss|keyword|credit|plugin"


class Cleaner:
    def __init__(self, html):
        self.html = html
        self.body = BeautifulSoup(html, 'html5lib').body

    def get_cleaned_body(self):
        self._remove_unwanted_tags()
        self._unwrap_tags()
        self._remove_comments()
        self._remove_noisy_tags()
        self._remove_redundant_blocks()
        return remove_special_chars(str(self.body))

    def _remove_unwanted_tags(self):
        for elem in self.body.select(','.join(TAGS_TO_REMOVE)):
            elem.extract()

    def _unwrap_tags(self):
        for elem in self.body.select(','.join(TAGS_TO_UNWRAP)):
            elem.unwrap()

    def _remove_comments(self):
        comments = self.body.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    def _remove_noisy_tags(self):
        self.body = self.__remove_tags(self.body)

    def __remove_tags(self, body):
        again = False
        for tag in body.find_all(True):
            if tag.name in ['img', 'figure', 'figcaption', 'caption', 'picture']:
                continue

            if should_remove_tag(tag):
                again = True
                tag.extract()

            if not contains_text(tag):
                again = True
                tag.extract()

            if tag.is_empty_element:
                again = True
                tag.extract()

            if has_only_one_anchor(tag):
                if tag.parent and tag.parent.name != 'p':
                    again = True
                    tag.extract()

        if again:
            return self.__remove_tags(body)
        return body

    def _remove_redundant_blocks(self):
        articles = self.body.select('article')
        if len(articles) >= 1:
            self.body = BeautifulSoup(str(articles[0]), 'lxml').body


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
