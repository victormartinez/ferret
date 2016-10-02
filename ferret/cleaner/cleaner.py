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
    body = _remove_noise_by_weight(body)
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


def _remove_noise_by_weight(body):
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

        # for tag in soup.find_all('div'):
        #     punct_ratio = tag.attrs['punct']
        #     if punct_ratio == 0:
        #         tag.extract()
        #
        #     parag_ratio = tag.attrs['parag']
        #     if parag_ratio == 0:
        #         tag.extract()

        # if round(punct_ratio, 4) < 0.1:
        #     tag.extract()

    return body
