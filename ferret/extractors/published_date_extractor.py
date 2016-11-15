import dateparser
import re
from bs4 import BeautifulSoup
from ferret.extractors.content_extractor import extract_body_text_from_html
from ferret.cleaner.text import normalize_text
from ferret.util.date import find_and_parse_into_date, parse_to_date
from math import ceil


class UrlPublishedDateExtractor:
    def __init__(self, context):
        self.context = context
        self.regex = r'(\d{4}/\d{2}/\d{2})/'

    def is_suitable(self):
        published_date = re.match(self.regex, self.context.get('url'))
        return published_date is not None

    def extract(self):
        published_date = re.search(self.regex, self.context.get('url'))
        datetime = parse_to_date(published_date.group(), self.context.get('lang'))
        if not datetime:
            return None

        if datetime.tzinfo:
            return datetime.isoformat()[:-6]
        return datetime.isoformat()


class MetaTagsPublishedDateExtractor:
    def __init__(self, context):
        self.context = context

    def is_suitable(self):
        soup = BeautifulSoup(self.context.get('html'), 'html.parser')
        meta_tags = soup.select('meta')
        return meta_tags

    def extract(self):
        soup = BeautifulSoup(self.context.get('html'), 'html.parser')
        meta_tags = soup.select('meta')
        for tag in meta_tags:
            content = tag.attrs.get('content')
            if not content:
                continue

            match = re.match(r'\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}', content)
            if content and match:
                # It's not necessary to use the lang once the meta tag brings the timezone
                datetime = dateparser.parse(match.group())
                if not datetime:
                    return None

                if datetime.tzinfo:
                    return datetime.isoformat()[:-6]
                return datetime.isoformat()
        return None


class TimeTagExtractor:
    def __init__(self, context):
        self.context = context

    def is_suitable(self):
        time_tag = self._get_time_tag()
        return time_tag and time_tag.get('datetime')

    def _get_time_tag(self):
        soup = BeautifulSoup(self.context.get('html'), 'lxml')
        return soup.select_one('time')

    def extract(self):
        date_str = self._get_time_tag().get('datetime')
        datetime = parse_to_date(date_str, self.context.get('lang'))
        if not datetime:
            return None

        if datetime.tzinfo:
            return datetime.isoformat()[:-6]
        return datetime.isoformat()


class OpenGraphPublishedDateExtractor:
    def __init__(self, context):
        self.context = context

    def is_suitable(self):
        soup = BeautifulSoup(self.context.get('html'), 'lxml')
        date_tag = soup.select_one('meta[property=article:published_time]')
        return date_tag and date_tag.get('content')

    def extract(self):
        soup = BeautifulSoup(self.context.get('html'), 'lxml')
        published_time = soup.select_one('meta[property=article:published_time]')
        if not published_time:
            return None

        # It's not necessary to use the lang once the meta tag brings the timezone
        datetime = dateparser.parse(published_time.get('content'))
        if not datetime:
            return None

        if datetime.tzinfo:
            return datetime.isoformat()[:-6]
        return datetime.isoformat()


class PublishedDateNearTitleExtractor:
    def __init__(self, context):
        self.context = context

    def is_suitable(self):
        text = extract_body_text_from_html(self.context.get('html'))
        title = self.context.get('title')
        return len(text) and len(title) and len(text) > len(title) and title in text

    def extract(self):
        offset = 500
        text = normalize_text(extract_body_text_from_html(self.context.get('html')))
        start_index = self._get_start_index(text, 500)
        end_index = self._get_end_index(text, 500)
        date = self.extract_date(text, start_index, end_index, offset)
        if date is None:
            return None

        datetime = parse_to_date(date, self.context.get('lang'))
        if not datetime:
            return None

        if datetime.tzinfo:
            return datetime.isoformat()[:-6]
        return datetime.isoformat()

    def _get_start_index(self, text, offset):
        title_start_index = text.index(self.context.get('title'))
        if title_start_index < offset:
            return 0
        return title_start_index - offset

    def _get_end_index(self, text, offset):
        title_start_index = text.index(self.context.get('title'))
        length_until_title_ends = title_start_index + len(self.context.get('title'))
        return length_until_title_ends + offset

    def extract_date(self, text, start_index, end_index, offset):
        fragment = text[start_index:end_index]
        candidate = find_and_parse_into_date(fragment)
        if candidate is not None:
            return candidate

        if len(fragment) >= len(text):
            return None

        next_start_index = self._get_next_start_index(start_index, offset)
        next_end_index = end_index + offset
        return self.extract_date(text, next_start_index, next_end_index, offset)

    def _get_next_start_index(self, start_index, offset):
        next_start_index = start_index - offset
        if next_start_index < 0:
            return 0
        return next_start_index


class PatternPublishedDateExtractor:
    def __init__(self, context):
        self.context = context

    def is_suitable(self):
        return True

    def extract(self):
        text = normalize_text(normalize_text(extract_body_text_from_html(self.context.get('html'))))
        start_index = ceil(len(text) / 3)
        date = self.extract_date(text, start_index, start_index)
        if not date:
            return None

        datetime = parse_to_date(date, self.context.get('lang'))
        if not datetime:
            return None

        if datetime.tzinfo:
            return datetime.isoformat()[:-6]
        return datetime.isoformat()

    def extract_date(self, text, start_index, end_index):
        offset_up = 200
        offset_down = 100

        fragment = text[start_index:end_index]
        candidate = find_and_parse_into_date(fragment)
        if candidate:
            return candidate

        if len(fragment) >= len(text):
            return None

        next_start_index = self._get_next_start_index(start_index, offset_up)
        next_end_index = end_index + offset_down
        return self.extract_date(text, next_start_index, next_end_index)

    def _get_next_start_index(self, start_index, offset):
        next_start_index = start_index - offset
        if next_start_index < 0:
            return 0
        return next_start_index
