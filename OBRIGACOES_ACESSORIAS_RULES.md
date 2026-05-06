# OBRIGACOES_ACESSORIAS_RULES

## Catalogo

1. `ESOCIAL` - eSocial
2. `FGTSDIGITAL` - FGTS Digital
3. `DCTFWEB` - DCTFWeb
4. `EFDREINF` - EFD-Reinf
5. `DCTFMENSAL` - DCTF Mensal
6. `EFDCONTRIB` - EFD Contribuições
7. `EFDICMSIPI` - EFD ICMS / IPI
8. `PGDASD` - PGDAS-D
9. `DIRBI` - DIRBI
10. `SPEDECD` - SPED ECD
11. `SPEDECF` - SPED ECF
12. `DEFIS` - DEFIS
13. `DIMOB` - DIMOB
14. `DMED` - DMED
15. `DITR` - DITR
16. `DOI` - DOI
17. `FUNRURAL` - FUNRURAL
18. `DECLAN` - DECLAN
19. `DEREMIT` - DeRE / MIT
20. `IBGE` - IBGE

## Collections

- `obrigacoes_catalogo`
- `obrigacoes_empresas`
- `obrigacoes_prazos`
- `obrigacoes_campos`
- `obrigacoes_validacoes`
- `obrigacoes_integracoes`
- `obrigacoes_penalidades`
- `alertas`
- `eventos`
- `auditoria`

## Regras Principais

- `PGDAS-D` apenas para `simples_nacional`.
- `DEFIS` apenas para `simples_nacional`.
- `EFD Contribuições` apenas para `lucro_real` e `lucro_presumido`.
- `ECD` anual, maio do ano seguinte, com `Ativo = Passivo + PL`.
- `ECF` anual, julho do ano seguinte, dependente de `ECD`.
- `DCTFWeb` depende de `eSocial` e `EFD-Reinf`.
- `FGTS Digital` depende de fechamento do `eSocial`.
- `DIRBI` registra o valor do beneficio fiscal comparado ao tributo pago.

## Prazos

- Mensal: calculado pela competência.
- Anual: calculado pelo ano-base.
- Eventual: calculado pela data do evento.
- UF especifica: usa tabela parametrizavel por estado.
- Fim de semana: antecipa para o ultimo dia util quando aplicavel.

## Endpoints

- `GET /api/obrigacoes/catalogo`
- `GET /api/obrigacoes/catalogo/{codigo}`
- `GET /api/obrigacoes/por-regime/{regime}`
- `GET /api/obrigacoes/empresa/{empresa_id}`
- `POST /api/obrigacoes/gerar-competencia`
- `POST /api/obrigacoes/validar`
- `PATCH /api/obrigacoes/{item_id}/status`
- `GET /api/obrigacoes/dashboard`
- `GET /api/obrigacoes/calendario`
- `POST /api/obrigacoes/reseed`

## Fluxo

1. Seed idempotente popula o catalogo por `codigo`.
2. Empresa criada/atualizada dispara geracao das obrigacoes aplicaveis.
3. Vencimentos geram alertas em janelas de 10, 5, 1, 0 e -1 dias.
4. Dashboard agrega KPIs por status, regime e orgao responsavel.
