# -*- coding: utf-8 -*-
from ferret.extractors.title_extractor import UrlTitleExtractor

titleExtractor = UrlTitleExtractor()


def _get_contents_of_file(path):
    with open(path, 'r') as content_file:
        return content_file.read().decode('utf8')


def test_stj_news_extraction():
    url = 'http://www.stj.jus.br/sites/STJ/default/pt_BR/Comunica%C3%A7%C3%A3o/Notícias/Notícias/Fórum-debateu-por-três-dias-boas-práticas-de-gestão-para-o-Judiciário'
    content = _get_contents_of_file('test/resources/pt/stj-forum-debateu-por-tres-dias-boas-praticas-de-gestao-para-o-judiciario.html')
    title = titleExtractor.extract(content, url)
    assert title == u"Fórum debateu por três dias boas práticas de gestão para o Judiciário"


def test_stj_news_extraction_with_encoded_url():
    url = 'http://www.stj.jus.br/sites/STJ/default/pt_BR/Comunica%C3%A7%C3%A3o/Not%C3%ADcias/Not%C3%ADcias/F%C3%B3rum-debateu-por-tr%C3%AAs-dias-boas-pr%C3%A1ticas-de-gest%C3%A3o-para-o-Judici%C3%A1rio'
    content = _get_contents_of_file('test/resources/pt/stj-forum-debateu-por-tres-dias-boas-praticas-de-gestao-para-o-judiciario.html')
    title = titleExtractor.extract(content, url)
    assert title == u"Fórum debateu por três dias boas práticas de gestão para o Judiciário"


def test_g1_news_extraction():
    url = 'http://g1.globo.com/mundo/noticia/2016/06/referendo-sai-em-2017-se-oposicao-cumprir-requisitos-diz-maduro.html'
    content = _get_contents_of_file('test/resources/pt/g1-referendo-sai-em-2017-se-oposicao-cumprir-requisitos-diz-maduro.html')
    title = titleExtractor.extract(content, url)
    assert title == u"Referendo sai em 2017 se oposição 'cumprir requisitos', diz Maduro"
