# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment
import re

TAGS_TO_REMOVE = ['script', 'style', 'iframe', 'meta', 'link', 'form', 'embed', 'noscript', 'object', 'source',
                  'svg', 'use', 'code', 'pre', 'input', 'textarea', 'option', 'select', 'fieldset', 'aside', 'menuitem',
                  'nav', 'footer', 'hr']

TAGS_TO_UNWRAP = ['font']

UNWANTED_ATTRS_REGEX = "sidebar|widget|social|facebook|comment|tweet|menu|footer|subscribe|foot|nav|google|share|search" \
                       "|form|contact|search|breadcrumb|banner|advertisement|lang|btn|tab|sitemap|instagram|flickr|print" \
                       "|button|pinterest|radio|box|bread|portlet|icon|dusqus|sponsor|popup|modal|pagination|page|promo" \
                       "|related|scroll|tool|login|sign|next|prev|old|new"


def normalize_text(text):
    result = ' '.join([s for s in text.split(' ') if s != ''])
    result = result.replace('\n', '')
    result = result.replace('\t', '')
    result = result.replace('\r', '')
    return result.strip()


def _get_flatten_attr_list(tag):
    attrs = tag.attrs
    if 'id' in attrs:
        ids = attrs['id']
        if isinstance(ids, list):
            for subitem in ids:
                yield subitem
        else:
            yield ids

    if 'class' in attrs:
        classes = attrs['class']
        if isinstance(classes, list):
            for subitem in classes:
                yield subitem
        else:
            yield classes


def clean_body(html):
    again = False
    body = BeautifulSoup(html, 'lxml').body
    for tag in body.find_all(True):
        if tag.name in TAGS_TO_REMOVE:
            again = True
            tag.extract()

        if tag.name in TAGS_TO_UNWRAP:
            again = True
            tag.unwrap()

        if len(tag.text.strip()) == 0:
            again = True
            tag.extract()

        if tag.is_empty_element:
            again = True
            tag.extract()

        if len(list(tag.children)) == 1 and tag.next.name == 'a':
            again = True
            tag.extract()

        if re.search(UNWANTED_ATTRS_REGEX, tag.name):
            again = True
            tag.extract()

        attrs = _get_flatten_attr_list(tag)
        for attr in attrs:
            if re.search(UNWANTED_ATTRS_REGEX, attr):
                again = True
                tag.extract()

    comments = body.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        again = True
        comment.extract()

    result = str(body).replace('\n', '')
    result = result.replace('\t', '')
    result = result.replace('\r', '')

    if again:
        return clean_body(result)
    else:
        return str(result)
