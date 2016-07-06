# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment

TAGS_TO_REMOVE = ['script', 'style', 'iframe', 'meta', 'link', 'form', 'embed', 'noscript', 'object', 'video', 'source',
                  'svg', 'use', 'code', 'pre', 'img']


def clean_body(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_doc = soup.body
    for tag in body_doc.find_all(True):
        if tag.name in TAGS_TO_REMOVE:
            tag.extract()

        try:
            tag.attrs.clear()
        except Exception:
            pass

        if len(tag.text.strip()) == 0:
            tag.extract()

        if tag.is_empty_element:
            tag.extract()

    comments = body_doc.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    result = str(body_doc).replace('\n', '')
    result = result.replace('\t', '')
    result = result.replace('\r', '')
    result = result.replace('  ', ' ')
    return result
