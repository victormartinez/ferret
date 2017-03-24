import pytest
from ferret.main import Ferret


def _get_contents_of(file_path):
    try:
        with open(file_path, errors='ignore') as file:
            return file.read()
    except IOError:
        return ''


@pytest.mark.parametrize("website", [
    "abcnews",
    "forbes",
    "foxnews",
    "reuters",
    "thebostonglobe",
    "theeconomist",
    "bbc",
    "cnn",
    "hbr",
    "irishtimes",
    "latimes",
    "mailonline",
    "medium",
    "mtvnews",
    "nationalgeographic",
    "nbcnews",
    "nprnews",
    "nytimes",
    "ozy",
    "techcrunch",
    "theguardian",
    "thehuffingtonpost",
    "theverge",
    "usatoday",
    "washingtonpost",
])
def test_published_date_extraction(website):
    url_file_path = "tests/resources/en/{}/url.txt".format(website)
    date_file_path = "tests/resources/en/{}/date.txt".format(website)
    html_file_path = "tests/resources/en/{}/page.html".format(website)

    url = _get_contents_of(url_file_path)
    html = _get_contents_of(html_file_path)

    expected_date = _get_contents_of(date_file_path)

    ferret = Ferret(url, html)
    article = ferret.get_article()
    extracted_date = article['published_date']
    assert expected_date[:10] == extracted_date[:10]


@pytest.mark.parametrize("website", [
])
def test_there_is_no_date_to_be_extracted(website):
    url_file_path = "tests/resources/en/{}/url.txt".format(website)
    date_file_path = "tests/resources/en/{}/date.txt".format(website)
    html_file_path = "tests/resources/en/{}/page.html".format(website)

    url = _get_contents_of(url_file_path)
    html = _get_contents_of(html_file_path)

    expected_date = _get_contents_of(date_file_path)

    ferret = Ferret(url, html)
    article = ferret.get_article()
    extracted_date = article['published_date']

    assert expected_date == ''
    assert extracted_date == ''
