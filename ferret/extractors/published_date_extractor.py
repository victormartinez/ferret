# -*- coding: utf-8 -*-
import re
import dateparser
from bs4 import BeautifulSoup


class UrlPublishedDateExtractor:
    def __init__(self, url):
        self.url = url

    def extract(self):
        published_date = re.search(r'(\d{4}/\d{2}/\d{2})/?', self.url)
        if not published_date:
            return None

        extracted_date = published_date.group()
        return dateparser.parse(extracted_date,
                                languages=['en'])  # date format used by blogs follow the american pattern


class MetaTagsPublishedDateExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extract(self):
        meta_tags = self.soup.select('meta')
        if not meta_tags:
            return None

        for tag in meta_tags:
            content = tag.attrs['content']
            if content:
                match = re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', content)
                if match:
                    return dateparser.parse(match.group())
        return None


class OpenGraphPublishedDateExtractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def extract(self):
        published_time = self.soup.select('meta[property=article:published_time]')
        if published_time:
            return published_time
        return None


class PatternPublishedDateExtractor:
    # TODO Use lib to recognize date
    DATE_PATTERNS = {
        r'\d{4}/\d{2}/\d{2}': 'en',  # 2016/04/01
        r'\w+\s\d,\s\d{4}': 'en',  # May 1, 2016
        r'\d{2}\s\w{3}\s\d{4}': 'en',  # 01 May 2016

        # 02/02/2016 às 14h10
        # 02/02/2016 às 14h10min
        # 02/02/2016 14h10min
        # 02/02/2016
        # 02/02/2016 - 14h10
        # 02/02/2016 - 14h10min
        #
        # 02/02/2016 às 14:10
        # 02/02/2016 às 14:10:10
        # 02/02/2016 14:10
        # 02/02/2016
        # 02/02/2016 14:10:10
        # 02/02/2016 - 14:10
        # 02/02/2016 - 14:10:10
        #
        # 02.02.2016 às 14:10
        # 02.02.2016 às 14:10:10
        # 02.02.2016 14:10
        # 02.02.2016
        # 02.02.2016 14:10:10
        # 02.02.2016 - 14:10
        # 02.02.2016 - 14:10:10
        #
        # 02.02.2016 às 14h10
        # 02.02.2016 às 14h10min
        # 02.02.2016 14h10
        # 02.02.2016 14h10min
        # 02.02.2016 - 14h10
        # 02.02.2016 - 14h10min
        #
        # 02-02-2016 às 14h10
        # 02-02-2016 às 14h10min
        # 02-02-2016 14h10
        # 02-02-2016 14h10min
        # 02-02-2016 - 14h10
        # 02-02-2016 - 14h10min
        #
        # 02-02-2016 às 14:10
        # 02-02-2016 às 14:10:10
        # 02-02-2016 14:10
        # 02-02-2016
        # 02-02-2016 14:10:10
        # 02-02-2016 - 14:10
        # 02-02-2016 - 14:10:10
        #
        # 5/7/2016 às 21h18
        # And the same above for 02.02.02
        r'\d{1,4}.\d{1,2}.\d{2,4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?': 'pt',

        # 26 de abril de 2012
        # 09 de fevereiro de 2015 às 12:40
        # 09 de fevereiro de 2015 às 12:40:00
        # 09 de fevereiro de 2015 às 12h40
        # 09 de fevereiro de 2015 às 12h40min
        # 13 de março de 2013 - 19:35
        # 13 de março de 2013 - 19:35:00
        # 13 de março de 2013 - 19h35min
        # 5 de julho de 2016 - 11h25
        r'\d{1,2}\sde\s[\wç]+\sde\s\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?': 'pt',

        # Terça, (26 Junho 2012)
        # Terça, (26 Junho 2012 16:02)
        # Terça, (26 Junho 2012 - 16:02)
        # Terça, (26 Junho 2012 às 16:02)
        # Terça, (26 Junho 2012 08:36)
        # Segunda, (25 Junho 2012 15:27)
        # quinta-feira, (22 de julho de 2009)
        r'\d{2}\s(de\s)?[\wç]+\s(de\s)?\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?': 'pt',

        # 2015 - junho - 29
        r'\d{4}\s-\s[\wç]+\s-\s\d{2}': 'pt',
    }

    def __init__(self, html):
        self.html = html

    def extract(self):
        date_candidates = self._extract_date_candidates()
        if len(date_candidates) == 0:
            return None
        return date_candidates[0]

    def _extract_date_candidates(self):
        candidates = []
        for date_pattern in self.DATE_PATTERNS.keys():
            search = re.search(date_pattern, self.html, re.I)
            if search:
                candidates.append(search.group())
        return candidates
