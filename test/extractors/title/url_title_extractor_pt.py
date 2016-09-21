# -*- coding: utf-8 -*-
import pytest
from ferret.extractors.title_extractor import UrlTitleExtractor


def _get_url_title_extractor(url, html):
    return UrlTitleExtractor(url, html)


def _get_contents_of_file(path):
    with open(path, 'r') as content_file:
        return content_file.read()


@pytest.mark.parametrize("test_file_path,url_page,expected_title", [
    ('pt/abdc-novas-regras-da-ans-obrigam-planos-de-saude-a-qualificar-atendimento.html', 'http://abradecont.org.br/noticias/novas-regras-da-ans-obrigam-planos-de-saude-a-qualificar-atendimento/', 'Novas regras da ANS obrigam planos de saúde a qualificar atendimento'),
    ("pt/age-mg-rejeitado-pedido-de-danos-morais-coletivos-decorrentes-das-condicoes-do-sistema-carcerario.html", "http://www.age.mg.gov.br/comunicacao/banco-de-noticias/2407-rejeitado-pedido-de-danos-morais-coletivos-decorrentes-das-condicoes-do-sistema-carcerario", "Rejeitado pedido de danos morais coletivos decorrentes das condições do sistema carcerário"),
    ("pt/agencia-brasil-ministros-do-stf-veem-condicoes-para-reforma-politica-apos-eleicoes-municipais.html", "http://agenciabrasil.ebc.com.br/politica/noticia/2016-09/ministros-do-stf-veem-condicoes-para-reforma-politica-apos-eleicoes", "Ministros do STF veem condições para reforma política após eleições municipais"),
    ("pt/agencia-brasil-ministros-do-stf-veem-condicoes-para-reforma-politica-apos-eleicoes-municipais.html", "http://agenciabrasil.ebc.com.br/politica/noticia/2016-09/ministros-do-stf-veem-condicoes-para-reforma-politica-apos-eleicoes", "Ministros do STF veem condições para reforma política após eleições municipais"),
    ("pt/ajufe-5a-edicao-da-expedicao-da-cidadania-atende-ribeirinhos-do-delta-do-parnaiba-pi-a-partir-desta-segunda-feira.html", "http://www.ajufe.org/imprensa/noticias/5-edicao-da-expedicao-da-cidadania-atende-ribeirinhos-do-delta-do-parnaiba-pi-a-partir-desta-segunda-feira/", "5ª edição da Expedição da Cidadania atende ribeirinhos do Delta do Parnaíba/PI a partir desta segunda-feira"),
    ("pt/al-ce-servidores-voluntarios-da-al-realizam-trabalho-no-lar-amigos-de-jesus.html", "http://www.al.ce.gov.br/index.php/ultimas-noticias/item/56930-1909-ci-voluntarios-prosa", "Servidores voluntários da AL realizam trabalho no Lar Amigos de Jesus"),
    ("pt/anamatra-cnj-institui-politica-nacional-de-seguranca-do-poder-judiciario.html", "http://www.anamatra.org.br/index.php/noticias/cnj-institui-politica-nacional-de-seguranca-do-poder-judiciario", "CNJ institui Política Nacional de Segurança do Poder Judiciário"),
    ("pt/apeminas-medalha-juscelino-kubitschek.html", "http://apeminas.org.br/medalha-juscelino-kubitschek/", "Medalha Juscelino Kubitschek"),
    ("pt/cd_-comissao-amplia-prazo-para-quitar-credito-rural-obtido-por-meio-de-fundos-de-financiamento.html", "http://www2.camara.leg.br/camaranoticias/noticias/AGROPECUARIA/516481-COMISSAO-AMPLIA-PRAZO-PARA-QUITAR-CREDITO-RURAL-OBTIDO-POR-MEIO-DE-FUNDOS-DE-FINANCIAMENTO.html", "Comissão amplia prazo para quitar crédito rural obtido por meio de fundos de financiamento"),
    ("pt/cgu-fiscalizacao-do-ministerio-da-transparencia-resulta-em-punicoes-no-mato-grosso.html", "http://www.cgu.gov.br/noticias/2016/09/fiscalizacao-do-ministerio-da-transparencia-resulta-em-punicoes-no-mato-grosso", "Fiscalização do Ministério da Transparência resulta em punições no Mato Grosso"),
    ("pt/cnj-semana-da-execucao-mobiliza-justica-trabalhista-no-rio-grande-do-norte.html", "http://www.cnj.jus.br/noticias/judiciario/83463-semana-da-execucao-mobiliza-justica-trabalhista-no-rio-grande-do-norte", "Semana da Execução mobiliza Justiça Trabalhista no Rio Grande do Norte"),
    ("pt/cnmp-cddf-realiza-reuniao-para-desenvolvimento-da-politica-de-atuacao-resolutiva-do-mp.html", "http://www.cnmp.mp.br/portal_2015/todas-as-noticias/9684-cddf-realiza-reuniao-para-desenvolvimento-da-politica-de-atuacao-resolutiva-do-mp", "CDDF realiza reunião para desenvolvimento da Política de Atuação Resolutiva do MP"),
    ("pt/consultor-juridico-servidor-que-pede-remocao-nao-tem-direito-a-ajuda-de-custo-diz-tnu.html", "http://www.conjur.com.br/2016-set-19/servidor-remocao-nao-direito-ajuda-custo-tnu", "Servidor que pede remoção não tem direito a ajuda de custo, diz TNU"),
    ("pt/controle-publico-tribunais-de-contas-elegem-controle-social-e-educacao-como-instrumentos-indispensaveis-no-combate-a-corrupcao.html", "http://www.controlepublico.org.br/institucional/noticias/4213-tribunais-de-contas-elegem-controle-social-e-educacao-como-instrumentos-indispensaveis-no-combate-a-corrupcao", "Tribunais de Contas elegem Controle Social e Educação como instrumentos indispensáveis no combate à corrupção"),
    ("pt/direito-do-estado-governador-de-alagoas-encaminha-a-assembleia-projeto-da-loa-para-2017.html", "http://www.direitodoestado.com.br/noticias/governador-de-alagoas-encaminha-a-assembleia-projeto-da-loa-para-2017", "Governador de Alagoas encaminha à Assembleia projeto da LOA para 2017"),
    ("pt/dp-al-defensor-publico-participa-do-64o-conselho-nacional-de-entidades-gerais.html", "http://www.defensoria.al.gov.br/sala-de-imprensa/noticias2/defensor-publico-participa-do-64o-conselho-nacional-de-entidades-gerais", "Defensor Público participa do 64º Conselho Nacional de Entidades Gerais"),
    ("pt/direito-domestico-sai-a-nova-versao-do-manual-do-esocial.html", "http://direitodomestico.jornaldaparaiba.com.br/noticias/sai-nova-versao-do-manual-do-esocial/", "Sai a nova versão do Manual do eSocial"),
    ("pt/direito-legal-impeachment-como-devera-agir-o-supremo-tribunal-federal.html", "http://www.direitolegal.org/artigos/impeachment-como-devera-agir-o-supremo-tribunal-federal/", "Impeachment: como deverá agir o Supremo Tribunal Federal?"),

    # TODO: Normalize space
    ("pt/carta-forense-vigilantes-do-peso-nao-indenizarao-orientadora-por-exigir-manutencao-do-peso.html", "http://www.cartaforense.com.br/conteudo/noticias/vigilantes-do-peso-nao-indenizarao-orientadora-por-exigir-manutencao-do-peso/16962", "TRABALHO  Vigilantes do Peso não indenizarão orientadora por exigir manutenção do peso"),
])
def test_title_extractor(test_file_path, url_page, expected_title):
    html = _get_contents_of_file("../../resources/{}".format(test_file_path))
    extractor = _get_url_title_extractor(url_page, html)
    assert extractor.extract() == expected_title

