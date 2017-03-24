import pytest
from ferret.extractors.content_extractor import ContentExtractor


def _get_contents_of(file_path):
    try:
        with open(file_path) as file:
            return file.read()
    except IOError:
        return None


@pytest.mark.parametrize("language,website_acronym", [
    ("pt", "r7"),
    ("pt", "terra"),
])
def test_content_extractor(language, website_acronym):
    html_file_path = "tests/resources/{}/{}/page.html".format(language, website_acronym)
    html = _get_contents_of(html_file_path)

    expected_content_file_path = "tests/resources/{}/{}/content.html".format(language, website_acronym)
    expected_content = _get_contents_of(expected_content_file_path)

    extractor = ContentExtractor(html)
    extracted_content = extractor.extract()
    print(extracted_content)
    assert extracted_content == expected_content
