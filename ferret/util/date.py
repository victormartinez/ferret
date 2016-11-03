# -*- coding: utf-8 -*-
import re

DATE_PATTERNS = [

    r'\d{4}/\d{2}/\d{2}',  # 2016/04/01
    r'\w+\s\d,\s\d{4}',  # May 1, 2016
    r'\d{2}\s\w{3}\s\d{4}',  # 01 May 2016

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
    r'\d{1,4}.\d{1,2}.\d{2,4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?',

    # 26 de abril de 2012
    # 09 de fevereiro de 2015 às 12:40
    # 09 de fevereiro de 2015 às 12:40:00
    # 09 de fevereiro de 2015 às 12h40
    # 09 de fevereiro de 2015 às 12h40min
    # 13 de março de 2013 - 19:35
    # 13 de março de 2013 - 19:35:00
    # 13 de março de 2013 - 19h35min
    # 5 de julho de 2016 - 11h25
    r'(?<!\d)\d{1,2}\sde\s[\wç]+\sde\s\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?',

    # Terça, (26 Junho 2012)
    # Terça, (26 Junho 2012 16:02)
    # Terça, (26 Junho 2012 - 16:02)
    # Terça, (26 Junho 2012 às 16:02)
    # Terça, (26 Junho 2012 08:36)
    # Segunda, (25 Junho 2012 15:27)
    # quinta-feira, (22 de julho de 2009)
    r'\d{2}\s(de\s)?[\wç]+\s(de\s)?\d{4}(\s?(às|-)?\s(\d{2}[:h]\d{2}(min)?(:\d{2})?))?',

    # 2015 - junho - 29
    r'\d{4}\s-\s[\wç]+\s-\s\d{2}',

    # 2016-10-25 19:57:02
    r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}',

    r'\d{2}-\w+-\d{4}',

    r'\d{2}/\d{2}/\d{4}',

    # 2016 - outubro - 25
    r'\d{4}\s?-\s?[\wç]+\s?-\s?\d{2}'
]

DATE_REPLACEMENTS = [
    (r'janeiro|january', '01'),
    (r'fevereiro|february', '02'),
    (r'mar[çc]o|march', '03'),
    (r'abril|april', '04'),
    (r'maio|may', '05'),
    (r'junho|june', '06'),
    (r'julho|july', '07'),
    (r'agosto|august', '08'),
    (r'setembro|september', '09'),
    (r'outubro|october', '10'),
    (r'novembro|november', '11'),
    (r'dezembro|december', '12'),
]


def parse_into_friendly_string(str_date):
    new_date = str_date.lower()
    for month, number in DATE_REPLACEMENTS:
        if re.search(month, str_date, re.I):
            new_date = re.sub(month, number, new_date)

    return new_date.replace('de', '').replace('às', '').replace('|', '').replace('h', ':').strip()
