# -*- coding: utf-8 -*-
from math import ceil
from ferret.cleaner.cleaner import clean_body
from scrapely.htmlpage import HtmlPage


def extract_text_region_around_title(html):
    html_text = clean_body(html)
    html_page = HtmlPage(body=html_text)
    index = ceil(len(html_page.parsed_body) / 3)
    start = html_page.parsed_body[index].start
    end = html_page.parsed_body[(index * 2)].end  # TODO: Analyse the necessity of + ceil(index/2)
    return html_page.body[start:end]
