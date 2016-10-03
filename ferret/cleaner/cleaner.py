# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from ferret.cleaner.comments import remove_comments
from ferret.cleaner.tag import should_remove_tag, remove_id_and_class, remove_unwanted_tags, unwrap_tags, contains_text, \
    has_only_one_anchor
from ferret.cleaner.text import remove_special_chars


def clean_body(html):
    body = BeautifulSoup(html, 'lxml').body
    body = remove_unwanted_tags(body)
    body = unwrap_tags(body)
    body = remove_comments(body)
    body = _remove_tags(body)
    body = _remove_redundant_blocks(body)
    body_str = str(body)
    return remove_special_chars(body_str)


def _remove_tags(body):
    again = False
    for tag in body.find_all(True):
        if not contains_text(tag):
            again = True
            tag.extract()

        if tag.is_empty_element:
            again = True
            tag.extract()

        if has_only_one_anchor(tag):
            again = True
            tag.extract()

        if should_remove_tag(tag):
            again = True
            tag.extract()

        remove_id_and_class(tag)

    if again:
        return _remove_tags(body)
    return body


def _remove_redundant_blocks(body):
    articles = body.select('article')
    if len(articles) >= 1:
        return articles[0]
    return body
