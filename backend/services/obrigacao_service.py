from typing import Optional
async def listar_obrigacoes(
    self,
    empresa_id: Optional[str] = None,
    tipo: Optional[TipoObrigacao] = None,
    status: Optional[StatusObrigacao] = None,
    cnpj: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    pagina: int = 1,
    por_pagina: int = 20
) -> Dict[str, Any]:
    """
    Lista obrigações com filtros e paginação
    """

    filtro = {}

    if empresa_id:
        filtro["empresa_id"] = empresa_id
    if tipo:
        filtro["tipo"] = tipo.value
    if status:
        filtro["status"] = status.value
    if cnpj:
        filtro["cnpj"] = cnpj

    # Filtro por data de vencimento
    if data_inicio or data_fim:
        filtro["data_vencimento"] = {}
        if data_inicio:
            filtro["data_vencimento"]["$gte"] = data_inicio.isoformat()
        if data_fim:
            filtro["data_vencimento"]["$lte"] = data_fim.isoformat()

    total = await self.db.obrigacoes.count_documents(filtro)

    skip = (pagina - 1) * por_pagina

    cursor = (
        self.db.obrigacoes.find(filtro, {"_id": 0})
        .sort("data_vencimento", 1)
        .skip(skip)
        .limit(por_pagina)
    )

    obrigacoes = await cursor.to_list(length=por_pagina)

    # 🔥 Converter datas ISO string para date (para bater com schema)
    for obrigacao in obrigacoes:
        if obrigacao.get("data_vencimento") and isinstance(obrigacao["data_vencimento"], str):
            obrigacao["data_vencimento"] = date.fromisoformat(obrigacao["data_vencimento"])

        if obrigacao.get("data_pagamento") and isinstance(obrigacao["data_pagamento"], str):
            obrigacao["data_pagamento"] = date.fromisoformat(obrigacao["data_pagamento"])

    return {
        "data": obrigacoes,   # 🔥 AQUI ESTÁ A CORREÇÃO
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina
    }