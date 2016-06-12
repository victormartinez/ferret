# -*- coding: utf-8 -*-
import dateparser
from bs4 import BeautifulSoup
from ferret.util.url_parser import extract_date_from_url
import re


class UrlPublishedDateExtractor(object):

    def extract(self, url):
        return extract_date_from_url(url)


class MetaTagsPublishedDateExtractor(object):

    def extract(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        meta_tags = soup.select('meta')
        if not meta_tags:
            return None

        for tag in meta_tags:
            content = tag.attrs['content']
            if content:
                match = re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', content)
                if match:
                    return dateparser.parse(match.group())
        return None


class PatternPublishedDateExtractor(object):

    DATE_PATTERNS = {
        r'\d{4}/\d{2}/\d{2}': 'en',                                          # 2016/04/01
        r'\w+\s\d,\s\d{4}': 'en',                                            # May 1, 2016
        r'\d{2}\s\w{3}\s\d{4}': 'en',                                        # 01 May 2016

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
        # And the same above for 02.02.02
        r'\d{2,4}.\d{2}.\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?': 'pt',



        # 26 de abril de 2012
        # 09 de fevereiro de 2015 às 12:40
        # 09 de fevereiro de 2015 às 12:40:00
        # 09 de fevereiro de 2015 às 12h40
        # 09 de fevereiro de 2015 às 12h40min
        # 13 de março de 2013 - 19:35
        # 13 de março de 2013 - 19:35:00
        # 13 de março de 2013 - 19h35min

        r'\d{2}\sde\s[\wç]+\sde\s\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?': 'pt',


        # Terça, 26 Junho 2012
        # Terça, 26 Junho 2012 16:02
        # Terça, 26 Junho 2012 - 16:02
        # Terça, 26 Junho 2012 às 16:02
        # Terça, 26 Junho 2012 08:36
        # Segunda, 25 Junho 2012 15:27
        # quinta-feira, 22 de julho de 2009
        r'[\wç-]+,\s\d{2}\s(de\s)?[\wç]+\s(de\s)?\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?': 'pt',

        # 2015 - junho - 29
        r'\d{4}\s-\s[\wç]+\s-\s\d{2}': 'pt',
    }

    def extract(self, html):
        for date_pattern in self.DATE_PATTERNS.keys():
            search = re.search(date_pattern, html, re.I)
            if search:
                return search.group()
        return ''
