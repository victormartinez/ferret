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
        self.url = url
        self.html = html
        self.lang = lang

        self._validate()
        self._download_html()
        self._detect_language()

        self.context = {'html': self.html, 'url': url, 'lang': self.lang}
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

    def _validate(self):
        if self.url is None or (self.url is not None and not isinstance(self.url, str)):
            raise ValueError("The URL provided is not a string.")

        if self.html is not None and not isinstance(self.html, str):
            raise ValueError("The HTML provided is not a string.")

        if self.lang is not None and not isinstance(self.lang, str):
            raise ValueError("The LANG provided is not a string.")

        if self.lang is not None and self.lang not in ['en', 'pt']:
            raise ValueError('The LANG value must be \'en\' or \'pt\'.')

    def _download_html(self):
        if self.html is None:
            self.html = get_html(self.url)

    def _detect_language(self):
        if not self.lang:
            cleaned_text = extract_body_text_from_html(self.html)
            self.lang = detect(cleaned_text)

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
