from ferret.cleaner.cleaner import extract_body_text_from_html
from ferret.cleaner.text import normalize_text
from ferret.extractors.published_date_extractor import OpenGraphPublishedDateExtractor, UrlPublishedDateExtractor, \
    TimeTagExtractor, PatternPublishedDateExtractor, MetaTagsPublishedDateExtractor, PublishedDateNearTitleExtractor
from ferret.extractors.title_extractor import OpenGraphTitleExtractor, UrlTitleExtractor, TitleCandidateExtractor, \
    TitleTagExtractor
from ferret.util.http import get_html
from langdetect import detect
from toolz import dicttoolz


class Ferret:
    def __init__(self, url, html=None, lang=None):
        if html is not None and not isinstance(html, str):
            raise ValueError("HTML must be a string.")

        self.basic_context = {'html': self._get_html(url, html), 'url': url, 'lang': self._get_lang(lang, html)}
        self.title_extractors = (
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

    def _get_html(self, url, html):
        return html if html is not None else get_html(url)

    def _get_lang(self, lang, html):
        if not lang:
            cleaned_text = extract_body_text_from_html(html)
            return detect(cleaned_text)
        return lang

    def get_article(self):
        title = self.extract_title(self.basic_context)
        context_with_title = dicttoolz.merge(self.basic_context, {'title': title})

        published_date = self.extract_published_date(context_with_title)
        context_with_date = dicttoolz.merge(context_with_title, {'published_date': published_date})

        content = self.extract_html_content(context_with_date)
        return dicttoolz.merge(context_with_date, {'content': content})

    def extract_title(self, context=None):
        if context is None:
            context = self.basic_context

        extractors = self._get_extractors(self.title_extractors, context)
        for e in extractors:
            title = e.extract()
            if title:
                return normalize_text(title)
        return ''

    def extract_published_date(self, context=None):
        if context is None:
            context = self.basic_context

        extractors = self._get_extractors(self.date_extractors, context)
        for e in extractors:
            datetime = e.extract()
            if datetime is not None:
                return datetime
        return ''

    def extract_html_content(self, context):
        return ''

    def _get_extractors(self, extractors, context):
        for extractor_instance in extractors:
            extractor = extractor_instance(context)
            if extractor.is_suitable():
                yield extractor
