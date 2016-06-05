# -*- coding: utf-8 -*-
import pytest
from ferret.util.url_parser import extract_sorted_keywords_from_url


@pytest.mark.parametrize("url, expected_keyword_list", [
    ('http://edition.cnn.com/2016/05/12/politics/china-trump-fans/index.html', ['china', 'trump', 'fans']),
    ('http://noticias.r7.com/brasil/qualquer-aumento-de-tributo-sera-temporario-diz-ministro-da-fazenda-13052016', ['qualquer', 'aumento', 'de', 'tributo', 'sera', 'temporario', 'diz', 'ministro', 'da', 'fazenda', '13052016']),
    ('http://www.correio24horas.com.br/detalhe/noticia/apos-protesto-rodoviarios-param-em-fazenda-coutos-e-comercio-fecha/?cHash=59a136e7d3779644ce12948e177f2eae', ['apos', 'protesto', 'rodoviarios', 'param', 'em', 'fazenda', 'coutos', 'e', 'comercio', 'fecha']),
    ('http://noticias.terra.com.br/brasil/politica/impeachment/dilma-afirma-estar-disposta-a-visitar-quem-a-convidar-inclusive-o-papa,ed1eaa981c59b9d784d32ab2e7eccb35fs34696o.html', ['dilma', 'afirma', 'estar', 'disposta', 'a', 'visitar', 'quem', 'a', 'convidar', 'inclusive', 'o', 'papa']),
    ('http://www5.tjba.jus.br/index.php?option=com_content&view=article&id=95869:juizes-servidores-e-policia-militar-discutem-medidas-de-seguranca-para-a-regiao-do-forum-do-imbui&catid=55&Itemid=202', ['juizes', 'servidores', 'e', 'policia', 'militar', 'discutem', 'medidas', 'de', 'seguranca', 'para', 'a', 'regiao', 'do', 'forum', 'do', 'imbui']),
    ('http://www.tst.jus.br/noticias/-/asset_publisher/89Dk/content/tst-mantem-negativa-de-penhora-de-oleo-diesel-para-garantia-de-execucao-contra-petrobras?redirect=http%3A%2F%2Fwww.tst.jus.br%2Fnoticias%3Fp_p_id%3D101_INSTANCE_89Dk%26p_p_lifecycle%3D0%26p_p_state%3Dnormal%26p_p_mode%3Dview%26p_p_col_id%3Dcolumn-2%26p_p_col_count%3D2', ['tst', 'mantem', 'negativa', 'de', 'penhora', 'de', 'oleo', 'diesel', 'para', 'garantia', 'de', 'execucao', 'contra', 'petrobras', '3Dcolumn', '2']),
    ('http://portal.trt15.jus.br/mais-noticias/-/asset_publisher/VlG0/content/2%C2%AA-vara-de-sao-carlos-homologa-acordo-de-r-2-802-749-50-beneficiando-mais-de-2-200-trabalhadores?redirect=http%3A%2F%2Fportal.trt15.jus.br%2Fmais-noticias%3Fp_p_id%3D101_INSTANCE_VlG0%26p_p_lifecycle%3D0%26p_p_state%3Dnormal%26p_p_mode%3Dview%26p_p_col_id%3Dcolumn-2%26p_p_col_count%3D1%26_101_INSTANCE_VlG0_advancedSearch%3Dfalse%26_101_INSTANCE_VlG0_keywords%3D%26_101_INSTANCE_VlG0_delta%3D10%26p_r_p_564233524_resetCur%3Dfalse%26_101_INSTANCE_VlG0_cur%3D1%26_101_INSTANCE_VlG0_andOperator%3Dtrue', ['mais', 'noticias', 'AA', 'vara', 'de', 'sao', 'carlos', 'homologa', 'acordo', 'de', 'r', '2', '802', '749', '50', 'beneficiando', 'mais', 'de', '2', '200', 'trabalhadores', '2Fmais', 'noticias', '3Dcolumn', '2']),
])
def test_correct_extraction_of_keywords(url, expected_keyword_list):
    keyword_list = extract_sorted_keywords_from_url(url)
    assert keyword_list == expected_keyword_list
