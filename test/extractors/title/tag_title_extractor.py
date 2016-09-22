# -*- coding: utf-8 -*-
import pytest
from ferret.extractors.title_extractor import TagTitleExtractor


def _get_og_title_extractor(html):
    return TagTitleExtractor(html)


def _get_contents_of_file(path):
    with open(path, 'r') as content_file:
        return content_file.read()

@pytest.mark.parametrize("test_file_path,expected_title", [
    ("pt/portal-justificando-a-reforma-trabalhisa-propoe-uma-nova-forma-de-escravidao.html", "A Reforma Trabalhisa propõe uma nova forma de escravidão"),
    ("pt/tj-mg-unidades-do-cejusc-sao-inauguradas-em-sabara-e-em-coronel-fabriciano.html", "Unidades do Cejusc são inauguradas em Sabará e em Coronel Fabriciano"),
    ("pt/tj-sc-empresa-aerea-indeniza-casal-que-pagou-assento-conforto-mas-viajou-apertado-ate-miami.html", "Empresa aérea indeniza casal que pagou assento conforto mas viajou apertado até Miami"),
    ("pt/tre-pa-justica-eleitoral-do-para-inicia-geracao-de-midia-para-urnas-eletronicas.html", "Justiça Eleitoral do Pará inicia geração de mídia para urnas eletrônicas"),
    ("pt/tre-pr-tre-pr-decide-sobre-o-tempo-participacao-de-apoiadores-no-horario-eleitoral.html", "TRE-PR decide sobre o tempo participação de apoiadores no horário eleitoral"),
    ("pt/al-pb-aprovado-projeto-libera-profissionais-de-educacao-fisica-nas-academias.html", "Aprovado projeto libera profissionais de Educação Física nas academias"),
    ("pt/amab-desembargadora-heloisa-graddi-recebe-medalha-thome-de-souza-na-proxima-quinta-22.html", "Desembargadora Heloisa Graddi recebe Medalha Thomé de Souza na próxima quinta (22)")
])
def test_tag_title_extractor(test_file_path, expected_title):
    html = _get_contents_of_file("test/resources/{}".format(test_file_path))
    extractor = _get_og_title_extractor(html)
    assert extractor.extract() == expected_title
