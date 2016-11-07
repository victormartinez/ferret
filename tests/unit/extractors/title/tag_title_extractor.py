# -*- coding: utf-8 -*-
import pytest
from ferret.extractors.title_extractor import TitleCandidateExtractor


def _get_tag_title_extractor(html):
    return TitleCandidateExtractor(html)


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
    ("pt/amab-desembargadora-heloisa-graddi-recebe-medalha-thome-de-souza-na-proxima-quinta-22.html", "Desembargadora Heloisa Graddi recebe Medalha Thomé de Souza na próxima quinta (22)"),
    ("pt/al-rj-alerj-ordem-do-dia-terca-feira-20-09-16-15h.html", "ALERJ – ORDEM DO DIA – TERÇA-FEIRA (20/09/16) – 15H"),
    ("pt/al-sp-procon-movel-atendera-populacao-no-estacionamento-da-assembleia.html", "Procon Móvel atenderá população no estacionamento da Assembleia"),
    ("pt/amab-desembargadora-heloisa-graddi-recebe-medalha-thome-de-souza-na-proxima-quinta-22.html", "Desembargadora Heloisa Graddi recebe Medalha Thomé de Souza na próxima quinta (22)"),
    ("pt/amagis-diretoria-da-amagis-marca-movimento-em-defesa-da-magistratura-para-o-dia-4-de-outubro.html", "Diretoria da Amagis marca Movimento em Defesa  da Magistratura para o dia 4 de outubro"),
    ("pt/amatra-05-a-contabilidade-judicial-daquilo-que-o-dinheiro-nao-compra.html", "1 Juízes do trabalho do Tribunal Regional do Trabalho da 4ª Região. Presidente e diretor da Associação dos Magistrados da Justiça do Trabalho da 4ª Região (AMATRA IV)."),
    ("pt/amb-preservacao-da-memoria-e-da-saude-sao-temas-do-congresso-de-pensionistas-da-magistratura.html", "Preservação da memória e da saúde são temas do Congresso de Pensionistas da Magistratura"),
    ("pt/ambito-juridico-rede-de-drogarias-nao-pode-exigir-dobra-de-jornada-no-regime-de-12-x-36.html", "Rede de drogarias não pode exigir dobra de jornada no regime de 12 x 36"),
    ("pt/anpt-nao-vamos-jogar-a-dignidade-dos-trabalhadores-no-lixo.html", "“Não vamos jogar a dignidade dos trabalhadores no lixo”"),
    ("pt/apbc-nota-conjunta-esclarecimentos-sobre-nota-da-frentas.html", "NOTA CONJUNTA - esclarecimentos sobre nota da Frentas"),
    ("pt/cd_-comissao-amplia-prazo-para-quitar-credito-rural-obtido-por-meio-de-fundos-de-financiamento.html", "Comissão amplia prazo para quitar crédito rural obtido por meio de fundos de financiamento"),
    ("pt/cgu-fiscalizacao-do-ministerio-da-transparencia-resulta-em-punicoes-no-mato-grosso.html", "Fiscalização do Ministério da Transparência resulta em punições no Mato Grosso"),
    ("pt/cnj-semana-da-execucao-mobiliza-justica-trabalhista-no-rio-grande-do-norte.html", "Semana da Execução mobiliza Justiça Trabalhista no Rio Grande do Norte"),
    ("pt/cnmp-cddf-realiza-reuniao-para-desenvolvimento-da-politica-de-atuacao-resolutiva-do-mp.html", "CDDF realiza reunião para desenvolvimento da Política de Atuação Resolutiva do MP"),
    ("pt/conamp-conamp-e-ex-procuradores-gerais-da-republica-falam-sobre-o-mp-pos-constituicao-de-1988.html", "CONAMP e ex-procuradores-gerais da República falam sobre o MP pós Constituição de 1988      Destaque"),
    ("pt/consultor-juridico-servidor-que-pede-remocao-nao-tem-direito-a-ajuda-de-custo-diz-tnu.html", "Servidor que pede remoção não tem direito a ajuda de custo, diz TNU"),
    ("pt/controle-publico-tribunais-de-contas-elegem-controle-social-e-educacao-como-instrumentos-indispensaveis-no-combate-a-corrupcao.html", "Tribunais de Contas elegem Controle Social e Educação como instrumentos indispensáveis no combate à corrupção"),
    ("pt/correio-forense-policial-militar-que-matou-marido-vai-receber-indenizacao-de-r-95-mil-por-mes.html", "Policial militar que matou marido vai receber ‘indenização’ de R$ 9,5 mil por mês"),
    ("pt/direito-do-estado-governador-de-alagoas-encaminha-a-assembleia-projeto-da-loa-para-2017.html", "Governador de Alagoas encaminha à Assembleia projeto da LOA para 2017"),
    ("pt/direito-domestico-sai-a-nova-versao-do-manual-do-esocial.html", "Sai a nova versão do Manual do eSocial"),
    ("pt/dp-al-defensor-publico-participa-do-64o-conselho-nacional-de-entidades-gerais.html", "Defensor Público participa do 64º Conselho Nacional de Entidades Gerais"),
    ("pt/dp-ms-defensoria-publica-participa-de-simposio-da-oab-ms-sobre-novo-cpc.html", "Defensoria Pública participa de Simpósio da OAB/MS sobre Novo CPC"),
])
def test_tag_title_extractor(test_file_path, expected_title):
    html = _get_contents_of_file("test/resources/{}".format(test_file_path))
    extractor = _get_tag_title_extractor(html)
    assert extractor.extract() == expected_title


@pytest.mark.parametrize("test_file_path,expected_title", [
    ("pt/al-rs-em-audiencia-com-sartori-regina-pede-regulamentacao-da-lei-dos-caes-de-aluguel.html", None),
    ("pt/anamatra-cnj-institui-politica-nacional-de-seguranca-do-poder-judiciario.html", None),
    ("pt/apeminas-medalha-juscelino-kubitschek.html", "18 de setembro de 2016"),
    ("pt/bndes-conselho-do-ppi-aprova-novo-valor-minimo-de-r-1791-bilhao-para-leilao-da-celg-d.html", "Áreas de Atuação"),
    ("pt/carta-forense-vigilantes-do-peso-nao-indenizarao-orientadora-por-exigir-manutencao-do-peso.html", None),
    ("pt/coad-termina-em-30-de-setembro-o-prazo-de-entrega-da-ditr-2016.html", "Lembrar minha senha"),
    ("pt/dp-mg-revista-da-tarde-desta-terca-20-09-vai-falar-sobre-o-casamento-comunitario-em-santa-luzia.html", "Defensoria Pública de Minas Gerais"),
    ("pt/dp-df-primeira-turma-de-mediadores-da-defensoria-recebe-certificacao.html", None),
    ("pt/direito-legal-impeachment-como-devera-agir-o-supremo-tribunal-federal.html", "Carregando. Por favor, aguarde!"),
    # ("pt/dias-brasil-adv-heinz-deve-indenizar-ex-motorista-que-foi-colocado-em-lista-discriminatoria.html", "Heinz deve indenizar ex-motorista que foi colocado em “lista discriminatória”"),
    # ("pt/csjt-trt-es-e-ouro-no-indice-de-processos-julgados-no-periodo-de-janeiro-a-maio-de-2016.html", "TRT-ES é ouro no Índice de Processos Julgados no período de janeiro a maio de 2016 - Todas as Notícias - CSJT")
])
def test_tag_title_extractor_goes_wrong(test_file_path, expected_title):
    html = _get_contents_of_file("test/resources/{}".format(test_file_path))
    extractor = _get_tag_title_extractor(html)
    assert extractor.extract() == expected_title
