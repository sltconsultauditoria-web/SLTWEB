from pymongo import MongoClient
from datetime import date

# Configuração do cliente MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["consultslt_db"]

# Dados das obrigações
obrigacoes = [
    {
        "nome": "eSocial",
        "regime_tributario": ["Lucro Real", "Lucro Presumido", "Simples Nacional"],
        "periodicidade": "Mensal",
        "prazo_entrega": "Até o dia 15 do mês seguinte (antecipa se não útil)",
        "orgao_responsavel": "Receita Federal do Brasil (RFB) / Ministério do Trabalho e Emprego (MTE)",
        "sistema_canal": "Portal eSocial (esocial.gov.br) — Web Services ou Portal Web",
        "multa_atraso": "R$ 402,53 a R$ 105.000,00 por infração conforme gravidade (CLT / IN MTE)",
        "descricao": "O eSocial é o Sistema de Escrituração Digital das Obrigações Fiscais, Previdenciárias e Trabalhistas. Unifica o envio de informações relativas a trabalhadores pelos empregadores ao governo federal.",
        "objetivos": [
            "Registrar vínculos empregatícios (admissão, demissão, afastamentos)",
            "Declarar folha de pagamento mensal (remunerações, descontos, encargos)",
            "Informar eventos de saúde e segurança do trabalho (SST)",
            "Registrar monitor de contratação de autônomos (RPA)",
            "Informar contribuições previdenciárias patronais e do empregado",
            "Substituir obrigações trabalhistas legadas (RAIS, CAGED, GFIP parcial)"
        ],
        "estrutura": [
            {"grupo": "Tabelas", "descricao": "Cadastros e tabelas (S-1000 a S-1070): empregador, estabelecimentos, rubricas, lotações, cargos"},
            {"grupo": "Não Periódicos", "descricao": "Eventos por ocorrência (S-2190 a S-2400): admissão, demissão, afastamento, aviso prévio"},
            {"grupo": "Periódicos", "descricao": "Eventos mensais (S-1200 a S-1299): remuneração, contribuições, FGTS"},
            {"grupo": "SST", "descricao": "Saúde e Segurança (S-2210 a S-2260): CAT, exames, monitoramento biológico"},
            {"grupo": "Fechamento", "descricao": "S-1299: Fechamento de período — obrigatório ao final do mês"}
        ],
        "campos_tags": [
            {"campo": "S-1000", "descricao": "Informações do Empregador (CNPJ, regime, dados cadastrais)", "tipo": "XML", "obrigatorio": True},
            {"campo": "S-1020", "descricao": "Tabela de Lotações Tributárias", "tipo": "XML", "obrigatorio": True},
            {"campo": "S-1070", "descricao": "Tabela de Processos Administrativos/Judiciais", "tipo": "XML", "obrigatorio": False},
            {"campo": "S-2200", "descricao": "Cadastramento Inicial e Admissão de Trabalhador", "tipo": "XML", "obrigatorio": True},
            {"campo": "S-2205", "descricao": "Alteração de Dados Cadastrais do Trabalhador", "tipo": "XML", "obrigatorio": False},
            {"campo": "S-2230", "descricao": "Afastamento Temporário (atestado, licença, etc.)", "tipo": "XML", "obrigatorio": False},
            {"campo": "S-2299", "descricao": "Desligamento (Demissão)", "tipo": "XML", "obrigatorio": False},
            {"campo": "S-1200", "descricao": "Remuneração do Trabalhador (Contribuição Previdenciária)", "tipo": "XML", "obrigatorio": True},
            {"campo": "S-1210", "descricao": "Pagamentos de Rendimentos do Trabalho", "tipo": "XML", "obrigatorio": True},
            {"campo": "S-1299", "descricao": "Fechamento dos Eventos Periódicos", "tipo": "XML", "obrigatorio": True}
        ],
        "validacoes": [
            "CNPJ deve estar ativo na Receita Federal",
            "CPF do trabalhador deve ser válido e sem restrições",
            "Data de admissão não pode ser posterior à data de envio",
            "Competência deve ser informada no formato AAAA-MM",
            "Evento S-1299 (fechamento) só pode ser enviado após todos os S-1200 do período",
            "Rubricas devem estar previamente cadastradas na tabela S-1010",
            "Afastamentos devem ter CID informado quando por doença",
            "Prazo do evento não periódico: até 7 dias corridos após o evento"
        ],
        "integracoes": [
            "API REST via Web Services do eSocial (certificado digital A1 ou A3)",
            "Padrão XML com schemas XSD disponibilizados pelo governo",
            "Retorno em XML com recibo de entrega (nrRec) e status de processamento",
            "Consulta de situação do lote por nrRec",
            "Integração com sistema de folha de pagamento (fonte dos dados)",
            "Integração com módulo de RH para eventos trabalhistas",
            "Ambiente de produção restrita disponível para testes"
        ]
    }
    # Adicionar as outras obrigações aqui seguindo o mesmo formato
]

def populate_obrigacoes():
    db["obrigacoes"].insert_many(obrigacoes)
    print("Dados inseridos com sucesso!")

if __name__ == "__main__":
    populate_obrigacoes()