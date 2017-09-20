import json

from langdetect import detect
from toolz import dicttoolz

from .cleaner.text import normalize_text
from .extractors.content_extractor import extract_body_text_from_html
from .extractors.content_extractor import ContentExtractor
from .extractors.published_date_extractor import (
    OpenGraphPublishedDateExtractor,
    UrlPublishedDateExtractor,
    TimeTagExtractor,
    PatternPublishedDateExtractor,
    MetaTagsPublishedDateExtractor,
    PublishedDateNearTitleExtractor
)
from .extractors.title_extractor import (
    OpenGraphTitleExtractor,
    UrlTitleExtractor,
    TitleCandidateExtractor,
    TitleTagExtractor,
    TwitterTitleExtractor
)
from .util.http import get_html


class Ferret:
    def __init__(self, url, html=None, lang=None):
        self.url = self._validate_url(url)
        self.html = self._validate_and_download_html(html, url)
        self.lang = self._validate_and_detect_lang(lang, html)

        self.context = {
            'html': self.html,
            'url': self.url,
            'lang': self.lang
        }
        self.title_extractors = (
            TwitterTitleExtractor,
            OpenGraphTitleExtractor,
            UrlTitleExtractor,
            TitleCandidateExtractor,
            TitleTagExtractor
        )

        self.date_extractors = (
            OpenGraphPublishedDateExtractor,
            UrlPublishedDateExtractor,
            PublishedDateNearTitleExtractor,
            PatternPublishedDateExtractor,
            TimeTagExtractor,
            MetaTagsPublishedDateExtractor
        )

    def _validate_url(self, url):
        if url is None or (url is not None and not isinstance(url, str)):
            raise ValueError("The URL provided is not a string.")
        return url

    def _validate_and_download_html(self, html, url):
        if html is not None and not isinstance(html, str):
            raise ValueError("The HTML provided is not a string.")
        return get_html(url)

    def _validate_and_detect_lang(self, lang, html):
        if lang is not None and not isinstance(lang, str):
            raise ValueError("The LANG provided is not a string.")

        if lang is not None and lang not in ['en', 'pt']:
            raise ValueError('The LANG value must be \'en\' or \'pt\'.')

        cleaned_text = extract_body_text_from_html(html)
        return detect(cleaned_text)

    def get_article(self, output='json'):
        title = self.extract_title(self.context)
        context_with_title = dicttoolz.merge(self.context, {'title': title})

        published_date = self.extract_published_date(context_with_title)
        context_with_date = dicttoolz.merge(context_with_title, {'published_date': published_date})

        content = self.extract_html_content(context_with_date)
        context = dicttoolz.merge(context_with_date, {'content': content})
        if output == 'json':
            return json.dumps(context)
        elif output == 'dict':
            return context
        return context

    def extract_title(self, context=None):
        if context is None:
            context = self.context

        extractors = self._get_extractors(self.title_extractors, context)
        for e in extractors:
            title = e.extract()
            if title:
                return normalize_text(title)
        return ''

    def extract_published_date(self, context=None):
        if context is None:
            context = self.context

        extractors = self._get_extractors(self.date_extractors, context)
        for e in extractors:
            datetime = e.extract()
            if datetime is not None:
                return datetime
        return ''

    def extract_html_content(self, context):
        extractor = ContentExtractor(context)
        return extractor.extract()

    def _get_extractors(self, extractors, context):
        for extractor_instance in extractors:
            extractor = extractor_instance(context)
            if extractor.is_suitable():
                yield extractor
