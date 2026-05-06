from __future__ import annotations

from datetime import datetime
from typing import Any

from backend.services.prazos_obrigacoes_service import calcular_vencimento, gerar_alertas_vencimento

CATALOG_VERSION = 1


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def base_item(
    codigo: str,
    nome: str,
    descricao: str,
    regimes: list[str],
    periodicidade: str,
    prazo_regra: str,
    orgao_responsavel: str,
    sistema_canal: str,
    multa_atraso: str,
    objetivos: list[str],
    grupos_blocos: list[str],
    campos: list[dict[str, Any]],
    validacoes: list[str],
    integracoes: list[str],
    penalidades: list[str],
    *,
    prazo_dia: int | None = None,
    prazo_mes: int | None = None,
    referencia_base: str | None = None,
    uf_especifica: str | None = None,
    antecipa_se_nao_util: bool = True,
    ativo: bool = True,
) -> dict[str, Any]:
    return {
        "codigo": codigo,
        "nome": nome,
        "descricao": descricao,
        "regimes": regimes,
        "periodicidade": periodicidade,
        "prazo_regra": prazo_regra,
        "prazo_dia": prazo_dia,
        "prazo_mes": prazo_mes,
        "referencia_base": referencia_base,
        "uf_especifica": uf_especifica,
        "antecipa_se_nao_util": antecipa_se_nao_util,
        "orgao_responsavel": orgao_responsavel,
        "sistema_canal": sistema_canal,
        "multa_atraso": multa_atraso,
        "objetivos": objetivos,
        "grupos_blocos": grupos_blocos,
        "campos": campos,
        "validacoes": validacoes,
        "integracoes": integracoes,
        "penalidades": penalidades,
        "ativo": ativo,
        "version": CATALOG_VERSION,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }


CATALOGO_OBRIGACOES = [
    base_item(
        "ESOCIAL",
        "eSocial",
        "Escrituração digital das obrigações trabalhistas, previdenciárias e fiscais.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "mensal",
        "Até o dia 15 do mês seguinte",
        "RFB / MTE",
        "Portal eSocial / Web Services",
        "Multas por atraso, omissão e inconsistência cadastral.",
        ["Unificar eventos trabalhistas", "Base para DCTFWeb e FGTS Digital"],
        ["S-1000", "S-1200", "S-1202", "S-1210", "S-1299"],
        [{"nome": "cpf_cnpj", "tipo": "documento", "obrigatorio": True}, {"nome": "competencia", "tipo": "mes_ano", "obrigatorio": True}, {"nome": "fechamento_s1299", "tipo": "booleano", "obrigatorio": True}],
        ["cpf/cnpj valido", "competencia AAAA-MM", "S-1299 apos eventos periodicos"],
        ["eSocial", "DCTFWeb", "FGTS Digital"],
        ["multa por atraso", "multa por informacao incorreta"],
        prazo_dia=15,
    ),
    base_item(
        "FGTSDIGITAL",
        "FGTS Digital",
        "Apuracao e recolhimento do FGTS com base nos eventos do eSocial.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "mensal",
        "Até o dia 20 do mês seguinte",
        "MTE / Caixa",
        "Portal FGTS Digital",
        "Multa e encargos por atraso no recolhimento.",
        ["Recolher FGTS por empregado", "Conferir encargos rescisórios"],
        ["Recolhimento mensal", "Rescisao", "Parcelamento"],
        [{"nome": "base_fgts", "tipo": "moeda", "obrigatorio": True}, {"nome": "aliquota", "tipo": "percentual", "obrigatorio": True}],
        ["depende de eSocial fechado", "aliquota 8%", "aprendiz 2%"],
        ["eSocial", "FGTS Digital"],
        ["multa de mora", "juros SELIC"],
        prazo_dia=20,
    ),
    base_item(
        "DCTFWEB",
        "DCTFWeb",
        "Declaracao de debitos e creditos tributarios federais previdenciarios.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "mensal",
        "Até o dia 15 do mês seguinte",
        "RFB",
        "Portal DCTFWeb",
        "Multa minima por atraso e multa proporcional por falta de entrega.",
        ["Consolidar debitos previdenciarios", "Gerar DARF numerado"],
        ["Fechamento mensal", "Pagamentos", "Parcelamentos"],
        [{"nome": "competencia", "tipo": "mes_ano", "obrigatorio": True}, {"nome": "eSocial_fechado", "tipo": "booleano", "obrigatorio": True}, {"nome": "efd_reinf_fechada", "tipo": "booleano", "obrigatorio": True}],
        ["depende de eSocial", "depende de EFD-Reinf", "cpf/cnpj validados"],
        ["eSocial", "EFD-Reinf", "DCTFWeb"],
        ["multa R$ 200 inativa", "multa R$ 500 ativa"],
        prazo_dia=15,
    ),
    base_item(
        "EFDREINF",
        "EFD-Reinf",
        "Escrituração fiscal digital de retenções e outras informações fiscais.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "mensal",
        "Até o dia 15 do mês seguinte",
        "RFB",
        "Portal EFD-Reinf / Web Services",
        "Multa por atraso na transmissão e inconsistencia de retencoes.",
        ["Informar retenções", "Base para DCTFWeb"],
        ["R-1000", "R-2010", "R-2020", "R-2099", "R-9011"],
        [{"nome": "competencia", "tipo": "mes_ano", "obrigatorio": True}, {"nome": "evento_periodico", "tipo": "booleano", "obrigatorio": True}],
        ["R-9011 apos eventos do periodo", "retencao INSS 11%", "campos condicionais por evento"],
        ["eSocial", "DCTFWeb", "EFD-Reinf"],
        ["multa por atraso", "multa por inconsistencias"],
        prazo_dia=15,
    ),
    base_item(
        "DCTFMENSAL",
        "DCTF Mensal",
        "Declaracao mensal de debitos e creditos tributarios federais.",
        ["lucro_real", "lucro_presumido", "todos"],
        "mensal",
        "Até o dia 15 do mês seguinte",
        "RFB",
        "Portal e-CAC",
        "Multa por atraso e declaracao sem movimento quando aplicavel.",
        ["Conciliar debitos e DARFs", "Controlar tributos federais"],
        ["Apuracao mensal", "Sem movimento"],
        [{"nome": "competencia", "tipo": "mes_ano", "obrigatorio": True}, {"nome": "debito_total", "tipo": "moeda", "obrigatorio": True}],
        ["nao se aplica ao Simples Nacional", "conciliar debitos com DARFs"],
        ["e-CAC", "SPED", "ERP"],
        ["multa minima", "multa progressiva"],
        prazo_dia=15,
    ),
    base_item(
        "EFDCONTRIB",
        "EFD Contribuições",
        "Escrituração do PIS/Pasep e Cofins com base no regime de tributação.",
        ["lucro_real", "lucro_presumido"],
        "mensal",
        "Até o dia 10 do mês seguinte",
        "RFB",
        "PVA SPED",
        "Multa por atraso e inconsistência na apuracao.",
        ["Apurar PIS/Cofins", "Consolidar receitas e creditos"],
        ["Bloco A", "Bloco C", "Bloco D", "Bloco M", "Bloco P"],
        [{"nome": "receita_bruta", "tipo": "moeda", "obrigatorio": True}, {"nome": "pis", "tipo": "moeda", "obrigatorio": True}, {"nome": "cofins", "tipo": "moeda", "obrigatorio": True}],
        ["lucro real: PIS 1,65% Cofins 7,6%", "lucro presumido: PIS 0,65% Cofins 3%"],
        ["SPED", "ERP fiscal"],
        ["multa por atraso", "multa por omissao"],
        prazo_dia=10,
    ),
    base_item(
        "EFDICMSIPI",
        "EFD ICMS / IPI",
        "Escrituração fiscal digital estadual com apuração de ICMS e IPI.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "mensal",
        "Prazo variável por UF",
        "SEFAZ",
        "Portal estadual / PVA",
        "Multa estadual por atraso e inconsistência de blocos.",
        ["Apurar ICMS", "Apurar IPI", "Integrar notas e estoque"],
        ["Bloco 0", "Bloco C", "Bloco D", "Bloco H", "Bloco K"],
        [{"nome": "uf", "tipo": "uf", "obrigatorio": True}, {"nome": "competencia", "tipo": "mes_ano", "obrigatorio": True}],
        ["prazo parametrizavel por UF", "pode variar por estado"],
        ["SEFAZ", "ERP", "NFe"],
        ["multa estadual", "restricao de credito"],
        prazo_dia=25,
    ),
    base_item(
        "PGDASD",
        "PGDAS-D",
        "Apuracao do Simples Nacional com calculo de aliquota efetiva.",
        ["simples_nacional"],
        "mensal",
        "Até o dia 20 do mês seguinte",
        "RFB",
        "Portal PGDAS-D",
        "Multa por atraso no recolhimento e inconsistência do faturamento.",
        ["Calcular aliquota efetiva", "Separar anexos", "Emitir DAS"],
        ["Anexo I", "Anexo III", "Anexo IV", "Anexo V"],
        [{"nome": "rbt12", "tipo": "moeda", "obrigatorio": True}, {"nome": "folha", "tipo": "moeda", "obrigatorio": True}],
        ["aliquota efetiva", "Fator R >= 28% anexo III"],
        ["PGDAS-D", "DAS"],
        ["multa por atraso", "juros SELIC"],
        prazo_dia=20,
    ),
    base_item(
        "DIRBI",
        "DIRBI",
        "Declaracao de Incentivos, Renuncias, Beneficios e Imunidades de natureza tributaria.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "mensal",
        "Até o dia 20 do mês seguinte",
        "RFB",
        "e-CAC / DIRBI",
        "Multa por omissao de beneficios e informacoes incorretas.",
        ["Declarar beneficios fiscais", "Apurar renuncias"],
        ["Beneficios federais", "Incentivos", "Imunidades"],
        [{"nome": "beneficio", "tipo": "texto", "obrigatorio": True}, {"nome": "valor_beneficio", "tipo": "moeda", "obrigatorio": True}],
        ["valor beneficio = tributo sem beneficio - tributo pago"],
        ["e-CAC", "ERP fiscal"],
        ["multa por omissao", "multa por informacao falsa"],
        prazo_dia=20,
    ),
    base_item(
        "SPEDECD",
        "SPED ECD",
        "Escrituração Contábil Digital anual.",
        ["lucro_real", "lucro_presumido"],
        "anual",
        "Até o último dia útil de maio do ano seguinte",
        "RFB",
        "PVA ECD",
        "Multa por atraso na escrituração contábil.",
        ["Validar balanco", "Validar livro diario", "Assinar digitalmente"],
        ["Livro Diario", "Livro Razao", "Balanco", "DRE"],
        [{"nome": "ativo", "tipo": "moeda", "obrigatorio": True}, {"nome": "passivo", "tipo": "moeda", "obrigatorio": True}, {"nome": "pl", "tipo": "moeda", "obrigatorio": True}],
        ["Ativo = Passivo + PL"],
        ["PVA ECD", "Certificado digital"],
        ["multa por atraso", "multa por inconsistencias contabeis"],
        prazo_mes=5,
        referencia_base="ano_anterior",
    ),
    base_item(
        "SPEDECF",
        "SPED ECF",
        "Escrituração Contábil Fiscal anual.",
        ["lucro_real", "lucro_presumido"],
        "anual",
        "Até o último dia útil de julho do ano seguinte",
        "RFB",
        "PVA ECF",
        "Multa por atraso e por informação inexata.",
        ["Confrontar LALUR", "Apurar IRPJ/CSLL", "Compensar prejuizo fiscal"],
        ["Lalur", "Lacs", "Bloco J"],
        [{"nome": "ecd_gerada", "tipo": "booleano", "obrigatorio": True}, {"nome": "prejuizo_fiscal", "tipo": "moeda", "obrigatorio": False}],
        ["depende de ECD", "compensacao limitada a 30%"],
        ["ECD", "PVA ECF"],
        ["multa por atraso", "multa por omissao"],
        prazo_mes=7,
        referencia_base="ano_anterior",
    ),
    base_item(
        "DEFIS",
        "DEFIS",
        "Declaração de Informações Socioeconômicas e Fiscais do Simples Nacional.",
        ["simples_nacional"],
        "anual",
        "Até 31 de março do ano seguinte",
        "RFB",
        "Portal do Simples Nacional",
        "Multa por atraso e inconsistências com PGDAS-D.",
        ["Consolidar faturamento", "Cruzar com PGDAS-D e eSocial"],
        ["DEFIS"],
        [{"nome": "receita_bruta_anual", "tipo": "moeda", "obrigatorio": True}, {"nome": "qtde_empregados", "tipo": "inteiro", "obrigatorio": True}],
        ["concilia com PGDAS-D", "concilia com eSocial"],
        ["PGDAS-D", "eSocial", "Simples Nacional"],
        ["multa por atraso", "multa por informacao falsa"],
        prazo_mes=3,
        prazo_dia=31,
        referencia_base="ano_anterior",
    ),
    base_item(
        "DIMOB",
        "DIMOB",
        "Declaração de Informações sobre Atividades Imobiliárias.",
        ["lucro_real", "lucro_presumido", "todos"],
        "anual",
        "Até o último dia útil de fevereiro do ano seguinte",
        "RFB",
        "PVA DIMOB",
        "Multa por atraso e inconsistência de operação imobiliária.",
        ["Informar intermediação imobiliária", "Receber dados de locação"],
        ["Imoveis", "Locacao", "Intermediacao"],
        [{"nome": "cpf_cnpj_contratante", "tipo": "documento", "obrigatorio": True}, {"nome": "valor_operacao", "tipo": "moeda", "obrigatorio": True}],
        ["operacoes imobiliarias", "contratos e valores"],
        ["Imobiliarias", "ERP comercial"],
        ["multa por atraso", "multa por omissao"],
        prazo_mes=2,
        referencia_base="ano_anterior",
    ),
    base_item(
        "DMED",
        "DMED",
        "Declaração de Serviços Médicos e de Saúde.",
        ["lucro_real", "lucro_presumido", "todos"],
        "anual",
        "Até o último dia útil de fevereiro do ano seguinte",
        "RFB",
        "PVA DMED",
        "Multa por atraso e dados de pacientes inconsistente.",
        ["Informar pagamentos de saude", "Conferir CPF do beneficiario"],
        ["Atendimentos", "Planos de saude"],
        [{"nome": "cpf_beneficiario", "tipo": "documento", "obrigatorio": True}, {"nome": "valor_servico", "tipo": "moeda", "obrigatorio": True}],
        ["cpf/cnpj valido", "dados de saude e reembolso"],
        ["PVA DMED", "ERP clinico"],
        ["multa por atraso", "multa por inconsistencias"],
        prazo_mes=2,
        referencia_base="ano_anterior",
    ),
    base_item(
        "DITR",
        "DITR",
        "Declaração do Imposto sobre a Propriedade Territorial Rural.",
        ["todos"],
        "anual",
        "Até o último dia útil de setembro",
        "RFB",
        "e-CAC / ITR",
        "Multa por atraso e dados de imóvel rural incorretos.",
        ["Informar imóvel rural", "Apurar ITR"],
        ["Imovel rural", "Area tributavel", "Grau de utilizacao"],
        [{"nome": "nirf", "tipo": "texto", "obrigatorio": True}, {"nome": "area_total", "tipo": "moeda", "obrigatorio": True}],
        ["imoveis rurais", "NIRF validado"],
        ["e-CAC", "Cadastro rural"],
        ["multa por atraso", "multa por area incorreta"],
        prazo_mes=9,
    ),
    base_item(
        "DOI",
        "DOI",
        "Declaração sobre Operações Imobiliárias.",
        ["todos"],
        "eventual",
        "Até o dia 10 do mês seguinte ao evento",
        "RFB",
        "Cartorio / e-CAC",
        "Multa por falta de informação ou atraso no evento.",
        ["Informar compra, venda e transferencia de imoveis"],
        ["Registro imobiliario"],
        [{"nome": "data_evento", "tipo": "data", "obrigatorio": True}, {"nome": "valor_operacao", "tipo": "moeda", "obrigatorio": True}],
        ["evento imobiliario", "documentacao do registro"],
        ["Cartorio", "e-CAC"],
        ["multa por atraso", "multa por omissao"],
        prazo_dia=10,
    ),
    base_item(
        "FUNRURAL",
        "FUNRURAL",
        "Apuracao e recolhimento do FUNRURAL para produtores e agroindustrias.",
        ["todos"],
        "mensal",
        "Até o dia 20 do mês seguinte",
        "RFB",
        "Portal e-CAC / Guia",
        "Multa e juros por atraso no recolhimento rural.",
        ["Apurar receita bruta rural", "Recolher contribuicao previdenciaria"],
        ["Receita rural", "Folha rural"],
        [{"nome": "receita_rural", "tipo": "moeda", "obrigatorio": True}, {"nome": "folha_rural", "tipo": "moeda", "obrigatorio": False}],
        ["rural only", "contribuicao previdenciaria"],
        ["e-CAC", "ERP rural"],
        ["multa por atraso", "juros SELIC"],
        prazo_dia=20,
    ),
    base_item(
        "DECLAN",
        "DECLAN",
        "Declaração Anual do Movimento Econômico e Fiscal estadual.",
        ["lucro_real", "lucro_presumido", "simples_nacional", "todos"],
        "anual",
        "Prazo parametrizável por UF",
        "SEFAZ",
        "Portal estadual",
        "Multa estadual por atraso e omissão.",
        ["Consolidar movimento estadual", "Base para o indice municipal"],
        ["Movimento economico", "Receita por UF"],
        [{"nome": "uf", "tipo": "uf", "obrigatorio": True}, {"nome": "movimento", "tipo": "moeda", "obrigatorio": True}],
        ["prazo variavel por UF", "parametrização estadual"],
        ["SEFAZ", "Contabilidade"],
        ["multa estadual", "restricao cadastral"],
        prazo_dia=30,
    ),
    base_item(
        "DEREMIT",
        "DeRE / MIT",
        "Registros e manifestos de comercio exterior e controles correlatos.",
        ["lucro_real", "lucro_presumido", "todos"],
        "mensal",
        "Até o dia 15 do mês seguinte",
        "RFB / MDIC",
        "Portal comercio exterior",
        "Multa e bloqueios operacionais por atraso.",
        ["Conferir operacoes de exportacao/importacao", "Gerar manifestos"],
        ["Comex", "Manifestos", "Registros"],
        [{"nome": "ncm", "tipo": "texto", "obrigatorio": True}, {"nome": "valor_cif", "tipo": "moeda", "obrigatorio": True}],
        ["comercio exterior", "cnaes correlatos"],
        ["Siscomex", "ERP comercio exterior"],
        ["multa por atraso", "bloqueio aduaneiro"],
        prazo_dia=15,
    ),
    base_item(
        "IBGE",
        "IBGE",
        "Pesquisas e declarações estatísticas obrigatórias conforme enquadramento.",
        ["todos"],
        "eventual",
        "Prazo definido por campanha / pesquisa",
        "IBGE",
        "Sistema IBGE",
        "Multa por omissão de respostas estatísticas.",
        ["Responder pesquisas obrigatorias", "Manter cadastro estatistico atualizado"],
        ["Campanhas", "Pesquisas", "Questionarios"],
        [{"nome": "codigo_pesquisa", "tipo": "texto", "obrigatorio": True}, {"nome": "status_resposta", "tipo": "texto", "obrigatorio": True}],
        ["campanha ativa", "prazo definido por notificacao"],
        ["IBGE", "Cadastro economico"],
        ["multa por omissao", "multa por atraso"],
        prazo_dia=15,
        antecipa_se_nao_util=False,
    ),
]


def ensure_obrigacoes_indexes(db) -> None:
    for collection_name, index_spec in [
        ("obrigacoes_catalogo", [("codigo", 1)]),
        ("obrigacoes_empresas", [("dedupe_key", 1)]),
        ("obrigacoes_prazos", [("dedupe_key", 1)]),
        ("obrigacoes_campos", [("codigo", 1)]),
        ("obrigacoes_validacoes", [("codigo", 1)]),
        ("obrigacoes_integracoes", [("codigo", 1)]),
        ("obrigacoes_penalidades", [("codigo", 1)]),
    ]:
        try:
            db[collection_name].create_index(index_spec, unique=True)
        except Exception:
            pass


def _upsert(db, collection_name: str, query: dict[str, Any], payload: dict[str, Any]) -> None:
    payload = {**payload, "updated_at": now_iso()}
    try:
        existing = db[collection_name].find_one(query)
        if existing:
            db[collection_name].update_one(query, {"$set": payload})
        else:
            db[collection_name].update_one(query, {"$set": {**query, **payload}}, upsert=True)
    except Exception:
        pass


def _seed_catalog_collections(db, item: dict[str, Any]) -> None:
    _upsert(db, "obrigacoes_catalogo", {"codigo": item["codigo"]}, item)
    _upsert(db, "obrigacoes_campos", {"codigo": item["codigo"]}, {"codigo": item["codigo"], "campos": item["campos"], "version": item["version"]})
    _upsert(db, "obrigacoes_validacoes", {"codigo": item["codigo"]}, {"codigo": item["codigo"], "validacoes": item["validacoes"], "version": item["version"]})
    _upsert(db, "obrigacoes_integracoes", {"codigo": item["codigo"]}, {"codigo": item["codigo"], "integracoes": item["integracoes"], "version": item["version"]})
    _upsert(db, "obrigacoes_penalidades", {"codigo": item["codigo"]}, {"codigo": item["codigo"], "penalidades": item["penalidades"], "multa_atraso": item["multa_atraso"], "version": item["version"]})
    _upsert(db, "obrigacoes_prazos", {"codigo": item["codigo"]}, {"codigo": item["codigo"], "periodicidade": item["periodicidade"], "prazo_regra": item["prazo_regra"], "prazo_dia": item.get("prazo_dia"), "prazo_mes": item.get("prazo_mes"), "referencia_base": item.get("referencia_base"), "uf_especifica": item.get("uf_especifica"), "version": item["version"]})


def seed_obrigacoes_acessorias(db, force: bool = False) -> dict[str, Any]:
    ensure_obrigacoes_indexes(db)
    collection = db["obrigacoes_catalogo"]
    existing_total = collection.count_documents({})
    if existing_total and not force:
        return {"seeded": False, "total": existing_total, "version": CATALOG_VERSION}

    for item in CATALOGO_OBRIGACOES:
        _seed_catalog_collections(db, item)

    return {"seeded": True, "total": len(CATALOGO_OBRIGACOES), "version": CATALOG_VERSION}


def _company_regime(company: dict[str, Any]) -> str:
    regime = str(company.get("regime_tributario") or company.get("regime") or company.get("perfil") or "").strip().lower()
    if regime in {"simples", "simplesnacional"}:
        return "simples_nacional"
    if regime in {"lucro_real", "lucroreal"}:
        return "lucro_real"
    if regime in {"lucro_presumido", "lucropresumido"}:
        return "lucro_presumido"
    return regime or "todos"


def sync_obrigacoes_for_empresa(db, company: dict[str, Any], competencia: str | None = None) -> dict[str, Any]:
    from backend.services.prazos_obrigacoes_service import (
        calcular_status,
        calcular_vencimento,
        gerar_alertas_vencimento,
        is_obrigacao_aplicavel,
    )

    catalog = list(db["obrigacoes_catalogo"].find({"ativo": {"$ne": False}}))
    if not competencia:
        competencia = datetime.utcnow().strftime("%Y-%m")
    empresa_id = str(company.get("id") or company.get("_id") or "")
    regime = _company_regime(company)
    uf = str(company.get("uf") or company.get("estado") or company.get("uf_empresa") or "").strip().upper() or None
    cnae = str(company.get("cnae") or company.get("cnae_principal") or "").strip() or None
    created = 0
    updated = 0
    alerts = 0
    applicable_keys: set[str] = set()

    for item in catalog:
        if not is_obrigacao_aplicavel(item, regime, uf=uf, cnae=cnae):
            continue
        vencimento = calcular_vencimento(item, competencia, uf=uf)
        status = calcular_status(vencimento, entregue=False, dispensada=False, nao_aplicavel=False)
        dedupe_key = f"{empresa_id}:{item['codigo']}:{competencia}"
        applicable_keys.add(dedupe_key)
        payload = {
            "dedupe_key": dedupe_key,
            "empresa_id": empresa_id,
            "empresa_nome": company.get("razao_social") or company.get("nome_fantasia") or company.get("nome") or "",
            "cnpj": company.get("cnpj"),
            "uf": uf,
            "cnae": cnae,
            "regime": regime,
            "obrigacao_codigo": item["codigo"],
            "obrigacao_nome": item["nome"],
            "periodicidade": item["periodicidade"],
            "competencia": competencia,
            "vencimento": vencimento.isoformat() if vencimento else None,
            "status": status,
            "prioridade": "alta" if status in {"atrasada", "vence_hoje", "vencendo"} else "normal",
            "orgao_responsavel": item["orgao_responsavel"],
            "sistema_canal": item["sistema_canal"],
            "campos": item["campos"],
            "validacoes": item["validacoes"],
            "integracoes": item["integracoes"],
            "penalidades": item["penalidades"],
            "codigo_catalogo": item["codigo"],
            "updated_at": now_iso(),
            "created_at": now_iso(),
        }
        existing = db["obrigacoes_empresas"].find_one({"dedupe_key": dedupe_key})
        if existing:
            db["obrigacoes_empresas"].update_one({"dedupe_key": dedupe_key}, {"$set": payload}, upsert=True)
            updated += 1
        else:
            db["obrigacoes_empresas"].insert_one(payload)
            created += 1

        db["obrigacoes"].update_one({"dedupe_key": dedupe_key}, {"$set": payload}, upsert=True)
        db["eventos"].update_one(
            {"dedupe_key": f"evento:{dedupe_key}"},
            {"$set": {
                "dedupe_key": f"evento:{dedupe_key}",
                "tipo": "obrigacao",
                "empresa_id": empresa_id,
                "obrigacao_codigo": item["codigo"],
                "competencia": competencia,
                "status": status,
                "vencimento": payload["vencimento"],
                "updated_at": now_iso(),
                "created_at": now_iso(),
            }},
            upsert=True,
        )
        alert_result = gerar_alertas_vencimento(db, payload)
        alerts += int(alert_result.get("created", 0))

    try:
        existing_items = list(db["obrigacoes_empresas"].find({"empresa_id": empresa_id, "competencia": competencia}))
        for existing_item in existing_items:
            if str(existing_item.get("dedupe_key") or "") in applicable_keys:
                continue
            update_fields = {"status": "nao_aplicavel", "ativo": False, "updated_at": now_iso()}
            db["obrigacoes_empresas"].update_one({"dedupe_key": existing_item.get("dedupe_key")}, {"$set": update_fields})
            db["obrigacoes"].update_one({"dedupe_key": existing_item.get("dedupe_key")}, {"$set": update_fields})
    except Exception:
        pass

    return {"empresa_id": empresa_id, "regime": regime, "competencia": competencia, "created": created, "updated": updated, "alerts": alerts}


def sync_obrigacoes_for_all_empresas(db, competencia: str | None = None) -> dict[str, Any]:
    summary = {"created": 0, "updated": 0, "alerts": 0, "empresas": 0}
    for company in db["empresas"].find({}):
        summary["empresas"] += 1
        result = sync_obrigacoes_for_empresa(db, company, competencia=competencia)
        summary["created"] += result["created"]
        summary["updated"] += result["updated"]
        summary["alerts"] += result["alerts"]
    return summary
