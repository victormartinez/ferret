# -*- coding: utf-8 -*-
from math import ceil
from ferret.cleaner.cleaner import clean_body
from scrapely.htmlpage import HtmlPage, HtmlTag


def extract_text_region_around_title(html):
    html_text = clean_body(html)
    html_page = HtmlPage(body=html_text)
    html_tags = [r for r in html_page.parsed_body if isinstance(r, HtmlTag)]
    index = ceil(len(html_tags) / 3)
    start = html_tags[index].start
    end = html_tags[index * 2].end
    return html_page.body[start:end]
