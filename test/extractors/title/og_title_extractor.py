# -*- coding: utf-8 -*-
import pytest
from ferret.extractors.title_extractor import OpenGraphTitleExtractor


def _get_og_title_extractor(html):
    return OpenGraphTitleExtractor(html)


def _get_contents_of_file(path):
    with open(path, 'r') as content_file:
        return content_file.read()


@pytest.mark.parametrize("test_file_path,expected_title", [
    ("pt/abdc-novas-regras-da-ans-obrigam-planos-de-saude-a-qualificar-atendimento.html", "Novas regras da ANS obrigam planos de saúde a qualificar atendimento"),
    ("pt/aba-esdras-dantas-visita-oab-ms.html", "Esdras Dantas visita OAB/MS"),
    ("pt/agencia-brasil-ministros-do-stf-veem-condicoes-para-reforma-politica-apos-eleicoes-municipais.html", "Ministros do STF veem condições para reforma política após eleições municipais"),
    ("pt/abrampa-empresa-deve-adotar-medidas-de-recuperacao-de-area-degradada-da-serra-da-piedade.html", "Empresa deve adotar medidas de recuperação de área degradada da Serra da Piedade"),
    ("pt/ultima-instancia-justica-mantem-prisao-preventiva-de-coronel-suspeito-de-abuso-de-crianca-no-rio.html", "Justiça mantém prisão preventiva de coronel suspeito de abuso de criança no Rio"),
    ("pt/unafe-anafe-participa-de-sessao-solene-em-homenagem-a-advocacia-na-camara-dos-deputados.html", "ANAFE participa de sessão solene em homenagem à advocacia na Câmara dos Deputados"),
    ("pt/oab-ce-pesquisa-ilimitada-de-diarios-oficiais-esta-disponivel-para-advogados-e-advogadas.html", "Pesquisa ilimitada de Diários Oficiais está disponível para advogados e advogadas"),
    ("pt/tj-go-corte-especial-realizara-sessao-extraordinaria-nesta-segunda-feira-19.html", "Corte Especial realizará sessão extraordinária nesta segunda-feira, 19"),
    ("pt/tj-ms-negado-recurso-de-detenta-que-cometeu-homicidio-qualificado-na-prisao.html", "Negado recurso de detenta que cometeu homicídio qualificado na prisão"),
    ("pt/oab-al-marcha-de-defesa-animal-oab-alagoas-reune-defensores-e-cobra-punicao-para-crimes-de-maus-tratos.html", "Ordem dos Advogados do Brasil Seccional Alagoas"),
    ("pt/tre-sc-tre-sc-realiza-audiencias-para-preparacao-das-urnas-eletronicas.html", "TRE-SC realiza audiências para preparação das urnas eletrônicas"),
    ("pt/trf-2-responsabilidade-solidaria-cdl-responde-por-divida-de-estabelecimento-associado-com-os-correios.html", "Responsabilidade solidária: CDL responde por dívida de estabelecimento associado com os Correios • TRF2"),
    ("pt/senado-senado-retoma-votacao-de-medidas-provisorias-nesta-terca-feira.html", "Senado retoma votação de medidas provisórias nesta terça-feira"),
    ("pt/stm-a-exemplo-do-stm-cerca-de-60-dos-tribunais-ja-contam-com-planejamento-voltado-a-praticas-sustentaveis.html", "STM - A exemplo do STM, cerca de 60% dos tribunais já contam com planejamento voltado a práticas sustentáveis"),
    ("pt/agu-derrubadas-mais-de-80-liminares-de-candidatos-que-concorriam-ao-revalida-sem-diploma.html", "Derrubadas mais de 80 liminares de candidatos que concorriam ao Revalida sem diploma"),
    ("pt/al-ce-servidores-voluntarios-da-al-realizam-trabalho-no-lar-amigos-de-jesus.html", "Servidores voluntários da AL realizam trabalho no Lar Amigos de Jesus"),
    ("pt/aasp-agencia-brasil-diario-oficial-publica-resolucao-que-altera-o-simples-nacional.html", "AASP :: Associação dos Advogados de São Paulo"),
    ("pt/al-ma-deputado-adriano-sarney-repoe-a-verdade-sobre-os-numeros-do-ideb.html", "Assembleia Legislativa do Estado do Maranhão - Deputado Adriano Sarney repõe a verdade sobre os números do IDEB"),
    ("pt/amab-desembargadora-heloisa-graddi-recebe-medalha-thome-de-souza-na-proxima-quinta-22.html", "Desembargadora Heloisa Graddi recebe Medalha Thomé de Souza na próxima quinta (22)"),
    ("pt/amatra-05-a-contabilidade-judicial-daquilo-que-o-dinheiro-nao-compra.html", "A Contabilidade Judicial daquilo que o dinheiro não compra"),
    ("pt/amagis-diretoria-da-amagis-marca-movimento-em-defesa-da-magistratura-para-o-dia-4-de-outubro.html", "Notícias da AMAGIS | AMAGIS - Associação dos Magistrados Mineiros"),
    ("pt/amb-preservacao-da-memoria-e-da-saude-sao-temas-do-congresso-de-pensionistas-da-magistratura.html", "AMB  |  Preservação da memória e da saúde são temas do Congresso de Pensionistas da Magistratura"),
    ("pt/al-sp-procon-movel-atendera-populacao-no-estacionamento-da-assembleia.html", "Procon Móvel atenderá população no estacionamento da Assembleia "),
    ("pt/cd_-comissao-amplia-prazo-para-quitar-credito-rural-obtido-por-meio-de-fundos-de-financiamento.html", "Comissão amplia prazo para quitar crédito rural obtido por meio de fundos de financiamento"),
    ("pt/cnj-semana-da-execucao-mobiliza-justica-trabalhista-no-rio-grande-do-norte.html", "Semana da Execução mobiliza Justiça Trabalhista no Rio Grande do Norte"),
    ("pt/coad-termina-em-30-de-setembro-o-prazo-de-entrega-da-ditr-2016.html", "COAD - Termina em 30 de setembro o prazo de entrega da DITR 2016"),
    ("pt/conamp-conamp-e-ex-procuradores-gerais-da-republica-falam-sobre-o-mp-pos-constituicao-de-1988.html", "CONAMP e ex-procuradores-gerais da República falam sobre o MP pós Constituição de 1988"),
    ("pt/controle-publico-tribunais-de-contas-elegem-controle-social-e-educacao-como-instrumentos-indispensaveis-no-combate-a-corrupcao.html", "Tribunais de Contas elegem Controle Social e Educação como instrumentos indispensáveis no combate à corrupção"),
    ("pt/correio-forense-policial-militar-que-matou-marido-vai-receber-indenizacao-de-r-95-mil-por-mes.html", "Policial militar que matou marido vai receber ‘indenização’ de R$ 9,5 mil por mês"),
    ("pt/direito-do-estado-governador-de-alagoas-encaminha-a-assembleia-projeto-da-loa-para-2017.html", "Governador de Alagoas encaminha à Assembleia projeto da LOA para 2017"),
    ("pt/direito-domestico-sai-a-nova-versao-do-manual-do-esocial.html", "Sai a nova versão do Manual do eSocial - Direito Doméstico"),
    ("pt/direito-legal-impeachment-como-devera-agir-o-supremo-tribunal-federal.html", "Impeachment: como deverá agir o Supremo Tribunal Federal? | Direito Legal Org"),
    ("pt/dp-df-primeira-turma-de-mediadores-da-defensoria-recebe-certificacao.html", "Primeira turma de Mediadores da Defensoria recebe certificação"),
    ("pt/dp-rj-hc-obtido-pela-dprj-garante-acesso-de-caicara-a-condominio-de-luxo.html", "HC obtido pela DPRJ garante acesso de caiçara a condomínio de luxo"),
    ("pt/dp-rs-audiencia-publica-promovida-pela-defensoria-publica-apresenta-diagnostico-sobre-a-violencia-policial-em-porto-alegre-e-na-regiao-metropolitana.html", "Audiência pública promovida pela Defensoria Pública apresenta diagnóstico sobre a violência policial em Porto Alegre e na região metropolitana "),
    ("pt/emporio-do-direito-azar-no-jogo-azar-no-amor-azar-ate-no-azar-por-saile-barbara-barreto.html", "Azar no jogo, azar no amor, azar até no azar… – Por Saíle Bárbara Barreto"),
    ("pt/fenasj-dia-22-sera-realizada-assembleia-regional-em-lages.html", "PORTAL FENAJUD | Dia 22 será realizada Assembleia Regional em Lages"),
    ("pt/iab-rita-cortez-e-celso-soares-participam-de-solenidade-na-oab-rj.html", "Rita Cortez e Celso Soares participam de solenidade na OAB/RJ - Instituto dos Advogados Brasileiros | IAB"),
    ("pt/espaco-vital-consorcio-de-empresas-e-condenado-em-acao-de-trabalhador-que-teve-que-dormir-ao-relento.html", "Consórcio de empresas é condenado em ação de trabalhador que teve que dormir ao relento  - Espaço Vital"),
    ("pt/folhapolitica-gilmar-mendes-ataca-lewandowski-e-o-deixa-em-situacao-constrangedora-o-stf-nao-deve-se-envolver-em-conchavos-veja.html", "Gilmar Mendes ataca Lewandowski e o deixa em situação constrangedora: 'O STF não deve se envolver em conchavos'; veja"),
    ("pt/iaf-mte-concede-certidao-de-registro-sindical-ao-iaf-sindical.html", "MTE CONCEDE CERTIDÃO DE REGISTRO SINDICAL AO IAF SINDICAL - IAF - Instituto dos Auditores Fiscais"),
    ("pt/iape-revisao-de-aposentadoria-formula-85-95.html", "Revisão de Aposentadoria - Fórmula 85/95 - IAPE Advogados"),
    ("pt/ibdp-direito-previdenciario-trf2-garante-aposentadoria-especial-a-coveiro.html", "TRF2 garante aposentadoria especial a coveiro"),
    ("pt/inst-rui-barbosa-presidente-sebastiao-helvecio-e-homenageado-com-medalha-do-merito-do-mpmg.html", "Presidente Sebastião Helvecio é homenageado com Medalha do Mérito do MPMG"),
    ("pt/jf-al-comissao-socioambiental-da-jfal-lanca-projeto-para-reducao-de-papel-a4-e-impressao.html", "Comissão Socioambiental da JFAL lança projeto para redução de papel A4 e impressão"),
    ("pt/jf_-tnu-decide-que-nao-e-devida-ajuda-de-custo-no-caso-de-remocao-a-pedido-de-procurador-federal.html", "TNU decide que não é devida ajuda de custo no caso de remoção a pedido de procurador federal"),
    ("pt/jornal-ordem-rs-artigo-do-presidente-nacional-da-oab-tolerancia.html", "Artigo do presidente nacional da OAB: tolerância - JO"),
    ("pt/jurisway-estado-pagara-prejuizo-de-homem-cujo-veiculo-foi-abalroado-por-viatura-durante-blitz.html", " Estado pagará prejuízo de homem cujo veículo foi abalroado por viatura durante blitz "),
    ("pt/tre-rj-eleitor-tem-ate-esta-quinta-feira-22-para-solicitar-2a-via-do-titulo.html", "Eleitor tem até esta quinta-feira (22) para solicitar 2ª via do título "),
])
def test_og_title_extractor(test_file_path, expected_title):
    html = _get_contents_of_file("../../resources/{}".format(test_file_path))
    extractor = _get_og_title_extractor(html)
    assert extractor.extract() == expected_title


@pytest.mark.parametrize("test_file_path,expected_title", [
    ("pt/trt-4-comeca-semana-da-execucao-no-trt-rs.html", None),
    ("pt/tce-ce-iniciada-2a-fase-da-selecao-para-provimento-de-cargo-em-comissao-do-mp-junto-ao-tce-ceara.html", None),
])
def test_og_title_extractor_gets_none(test_file_path, expected_title):
    html = _get_contents_of_file("../../resources/{}".format(test_file_path))
    extractor = _get_og_title_extractor(html)
    assert extractor.extract() == expected_title
