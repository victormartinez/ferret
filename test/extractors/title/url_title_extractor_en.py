# -*- coding: utf-8 -*-
from ferret.extractors.title_extractor import UrlTitleExtractor


def _get_url_title_extractor(url, html):
    return UrlTitleExtractor(url, html)


def _get_contents_of_file(path):
    with open(path, 'r') as content_file:
        return content_file.read()


def test_cnn_news_extraction():
    url = 'http://edition.cnn.com/2016/05/12/politics/china-trump-fans/index.html'
    content = _get_contents_of_file('test/resources/en/cnn-2016-05-12-politics-china-trump-fans.html')
    title_extractor = _get_url_title_extractor(url, content)
    title = title_extractor.extract(content)
    assert title == u"Meet Donald Trump's Chinese fans"
