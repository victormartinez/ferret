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
    "bbc",
    "cnn",
    "forbes",
    "foxnews",
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
    "reuters",
    "techcrunch",
    "thebostonglobe",
    "theeconomist",
    "theguardian",
    "thehuffingtonpost",
    "theverge",
    "usatoday",
    "washingtonpost",
])
def test_title_extractor(website):
    url_file_path = "tests/resources/en/{}/url.txt".format(website)
    title_file_path = "tests/resources/en/{}/title.txt".format(website)
    html_file_path = "tests/resources/en/{}/page.html".format(website)

    url = _get_contents_of(url_file_path)
    html = _get_contents_of(html_file_path)

    expected_title = _get_contents_of(title_file_path)

    ferret = Ferret(url, html)
    assert expected_title == ferret.extract_title()
