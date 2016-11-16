# -*- coding: utf-8 -*-
import dateparser
import re


def replace_str_by_number(str_date):
    for month, number in DATE_REPLACEMENTS:
        if re.search(month, str_date, re.I):
            return re.sub(month, number, str_date)
    return str_date


def date_replace_1(date_str):
    return date_str.replace('de', '/')


def date_replace_2(date_str):
    return date_str.replace('às', '')


def date_replace_3(date_str):
    return date_str.replace('|', '')


def date_replace_4(date_str):
    return date_str.replace('h', ':')


def date_replace_5(date_str):
    return date_str.replace(' /', '/')


def date_replace_6(date_str):
    return date_str.replace(' ', '')


def date_replace_7(date_str):
    return date_str.replace('//', '/')


def date_replace_8(date_str):
    return date_str.replace('min', '')


def date_replace_9(date_str):
    return date_str.replace('-/', '-')


def date_replace_10(date_str):
    return date_str.replace('/-', '-')


DATE_PATTERNS = [

    # 2016/04/0
    (r'\d{4}/\d{2}/\d{2}', []),

    # May 1, 201: []
    (r'\w+\s\d,\s\d{4}', []),

    # 01 May 201: []
    (r'\d{2}\s\w{3}\s\d{4}', []),

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
    # 02/02/2016 14:10:10
    # 02/02/2016 - 14:10
    # 02/02/2016 - 14:10:10
    #
    # 02.02.2016 às 14:10
    # 02.02.2016 às 14:10:10
    # 02.02.2016 14:10
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
    (r'\d{1,4}.\d{1,2}.\d{2,4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?', [date_replace_4, date_replace_8]),

    # 26 de abril de 2012
    # 09 de fevereiro de 2015 às 12:40
    # 09 de fevereiro de 2015 às 12:40:00
    # 09 de fevereiro de 2015 às 12h40
    # 09 de fevereiro de 2015 às 12h40min
    # 13 de março de 2013 - 19:35
    # 13 de março de 2013 - 19:35:00
    # 13 de março de 2013 - 19h35min
    # 5 de julho de 2016 - 11h25
    (r'(?<!\d)\d{1,2}\sde\s[\wç]+\sde\s\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?',
     [replace_str_by_number, date_replace_1, date_replace_7, date_replace_2, date_replace_4, date_replace_8]),

    # Terça, (26 Junho 2012)
    # Terça, (26 Junho 2012 16:02)
    # Terça, (26 Junho 2012 - 16:02)
    # Terça, (26 Junho 2012 às 16:02)
    # Terça, (26 Junho 2012 08:36)
    # Segunda, (25 Junho 2012 15:27)
    # quinta-feira, (22 de julho de 2009)
    (r'\d{2}\s(de\s)?[\wç]+\s(de\s)?\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?', []),

    # 2016-10-25 19:57:02
    (r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', []),

    (r'\d{2}-\w+-\d{4}', []),

    (r'\d{2}/\d{2}/\d{4}', []),

    # 2016 - outubro - 25
    (r'\d{4}\s?-\s?[\wç]+\s?-\s?\d{2}', [replace_str_by_number, date_replace_6, date_replace_9, date_replace_10]),

    # 24 Out 2016 19:02
    (r'\d{2}\s[\wç]{3}\s\d{4}\s\d{2}:\d{2}', [replace_str_by_number, date_replace_5]),
]

DATE_REPLACEMENTS = [
    (r'janeiro|january|jan', '/01/'),
    (r'fevereiro|february|fev|feb', '/02/'),
    (r'mar[çc]o|march|mar', '/03/'),
    (r'abril|april|abr|apr', '/04/'),
    (r'maio|may|mai', '/05/'),
    (r'junho|june|jun', '/06/'),
    (r'julho|july|jul', '/07/'),
    (r'agosto|august|aug', '/08/'),
    (r'setembro|september|sep', '/09/'),
    (r'outubro|october|out|oct', '/10/'),
    (r'novembro|november|nov', '/11/'),
    (r'dezembro|december|dez|dec', '/12/'),
]


def find_and_parse_into_date(text_fragment):
    fragment = text_fragment.lower()
    candidates = []
    for t in DATE_PATTERNS:
        regex, replacement_strategies = t
        match = re.search(regex, fragment, re.I)
        if match:
            candidate = match.group()
            if _is_candidade_valid(candidate):
                date_str = apply_strategies(candidate, replacement_strategies)
                candidates.append(date_str)

    if len(candidates):
        return candidates[0]
    return None


def apply_strategies(str_date, replacement_functions):
    new_str_date = str_date
    for function in replacement_functions:
        new_str_date = function(new_str_date)
    return new_str_date


def _is_candidade_valid(candidate):
    return candidate.count('/') == 2 or candidate.count('.') == 2 or candidate.count('-') == 2 or candidate.count(
        '/') == 2 or candidate.count('de') == 2 or candidate.count(':') == 2 or _string_contains_month(candidate)


def _string_contains_month(candidate):
    regex = r'janeiro|january|jan|fevereiro|february|fev|feb|mar[çc]o|march|mar|abril|april|abr|apr|maio|may|mai|junho|june|jun|julho|july|jul|agosto|august|aug|setembro|september|sep|outubro|october|out|oct|novembro|november|nov|dezembro|december|dez|dec'
    return re.search(regex, candidate, re.I)


def parse_to_date(date_str, lang):
    try:
        datetime = dateparser.parse(date_str, languages=[lang])
        if datetime:
            return datetime
    except ValueError:
        return dateparser.parse(date_str)
