import pytest
from ferret.main import Ferret


def _get_contents_of(file_path):
    try:
        with open(file_path, errors='ignore') as file:
            return file.read()
    except IOError:
        return ''


@pytest.mark.parametrize("website", [
    "al-sp",
    "mps",
    "portal-justificando",
    "senado",
    "unafe",
    "anda",
    "iape",
    "trf-2",
    "veja",
    "agencia-brasil",
    "agu",
    "ajufergs",
    "al-to",
    "cd",
    "cgu",
    "cnj",
    "consultor-juridico",
    "dp-al",
    "dp-mg",
    "dp-rs",
    "dp-to",
    "g1",
    "ibdfam",
    "ibdp-direito-previdenciario",
    "jf",
    "jurisway",
    "mp-pr",
    "mp-rs",
    "oab-ba",
    "oab-ma",
    "oab-pe",
    "oab-se",
    "oab-sp",
    "oab-to",
    "pndt",
    "rf",
    "tce-sc",
    "tce-se",
    "tj-ms",
    "tj-sc",
    "tre-ap",
    "tre-ce",
    "tre-df",
    "tre-es",
    "tre-go",
    "tre-ma",
    "tre-ms",
    "tre-mt",
    "tre-pa",
    "tre-pb",
    "tre-pi",
    "tre-rn",
    "tre-ro",
    "tre-se",
    "tre-sp",
    "tre-to",
    "trt-6",
    "tse",
    "ultima-instancia",
    "uol",
    "bndes",
    "tce-ms",
    "coad",
    "al-ma",
    "amagis",
    "espaco-vital",
    "fenasj",
    "tech-tudo",
    "sbt",
    "exame",
    "gazeta-do-povo",
    "epoca",
    "direito-do-estado",
    "dias-brasil-adv",
    "oab-es",
    "oab-go",
    "sefaz-sc",
    "sefaz-sp",
    "tj-rj",
    "trt-10",
    "trt-3",
    "computer-world",
    "jornal-ordem-rs",
    "oab-df",
    "tj-ce",
    "sefaz-to",
    "enm",
    "trt-24",
    "dp-rj",
    "oab-sc",
    "al-rj",
    "amab",
    "jf-al",
    "oab-ce",
    "oab-ms",
    "tre-ac",
    "tre-al",
    "trf-1",
    "dp-ms",
    "amb",
    "csjt",
    "tj-go",
    "tre-rj",
    "tre-rs",
    "trf-4",
    "stm",
    "trt-4",
    "oab-mg",
    "carta-forense",
    "oab-mt",
    "tj-sp",
    "al-rs",
    "oab-rs",
    "tce-ce",
    "tj-mg",
    "tj-pr",
    "tj-df",
    "dp-sp",
    "ambito-juridico",
    "juristas",
    "internet-legal",
    "folhapolitica",
    "amatra-05",
    "apeminas",
    "lfg",
    "oab",
    "tre-mg",
    "tre-pr",
    "tre-rr",
    "stf",
    "al-mt",
    "al-pb",
    "anamatra",
    "apbc",
    "cnmp",
    "mp-df",
    "mpf",
    "pgr",
    "pr-rs",
    "sintese",
    "abojeris",
    "oab-al",
    "al-ms",
    "tj-es",
    "dp-df",
    "direito-domestico",
    "direito-legal",
    "iaf",
    "imaster",
    "trt-13",
    "correio-forense",
    "tst",
    "mpt-prt4",
    "mpt-prt5",
    "trt-7",
    "aba",
    "dpu",
    "yahoo",
    "ajufe",
    "al-go",
    "tcu",
    "tre-sc",
    "correio_da_bahia",
    "al-ac",
    "al-ce",
    "mp-am",
    "sebrae-sp",
    "sindjufe-go",
    "trt-2",
    "trt-20",
    "estadao",
    "conamp",
    "mp-pb",
    "iab",
    "stj",
    "abrampa",
    "tce-rs",
    "trf-3",
    "controle-publico",
    "folha",
    "al-am",
    "mj",
    "msn",

    # Failing Tests
    "sefaz-rs",
    "mpt",
    "mp-mt",
    "trf-5",
    "olhar-digital",
    "anpt",
    "dp-mt",
    "inst-rui-barbosa",
    "oab-rn",
    "observatorio-eco",
    "r7",
    "tce-ba",
    "tce-ma",
    "terra",
    "trt-14",
    "trt-15",
])
def test_published_date_extraction(website):
    url_file_path = "tests/resources/pt/{}/url.txt".format(website)
    date_file_path = "tests/resources/pt/{}/date.txt".format(website)
    html_file_path = "tests/resources/pt/{}/page.html".format(website)

    url = _get_contents_of(url_file_path)
    html = _get_contents_of(html_file_path)

    expected_date = _get_contents_of(date_file_path)

    ferret = Ferret(url, html)
    article = ferret.get_article()
    extracted_date = article['published_date']
    assert expected_date[:10] == extracted_date[:10]


@pytest.mark.parametrize("website", [
    "acat",
    "dp-pe",
    "age-mg",
])
def test_there_is_no_date_to_be_extracted(website):
    url_file_path = "tests/resources/pt/{}/url.txt".format(website)
    date_file_path = "tests/resources/pt/{}/date.txt".format(website)
    html_file_path = "tests/resources/pt/{}/page.html".format(website)

    url = _get_contents_of(url_file_path)
    html = _get_contents_of(html_file_path)

    expected_date = _get_contents_of(date_file_path)

    ferret = Ferret(url, html)
    article = ferret.get_article()
    extracted_date = article['published_date']

    assert expected_date == ''
    assert extracted_date == ''
