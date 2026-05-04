# AUTH TEST REPORT

## STATUS GERAL

BLOQUEADO

## BACKEND_URL

Nao publicado ainda.

## CONTEXTO

Foi validado o contrato de autenticação no código e na suíte automatizada local, mas não foi possível executar um teste E2E real em navegador contra o GitHub Pages + backend publicado porque a URL pública do backend não está disponível neste workspace.

## VALIDAÇÕES LOCAIS EXECUTADAS

- `python -m pytest tests/test_api_endpoints.py -q`
- `python -m pytest tests/test_github_pages_frontend_contract.py -q`
- `python -m pytest tests -q`
- Revisão do contrato em `frontend/src/lib/apiClient.js`
- Revisão do login em `frontend/src/context/AuthContext.jsx`
- Revisão do fluxo legado em `frontend/src/components/EntraIDLogin.jsx`
- Revisão do endpoint em `backend/routers/auth.py`

## RESULTADO POR USUÁRIO

### admin@empresa.com / admin123

- Login: NOK
- Token: NOK
- Redirecionamento: NOK
- Permissões: NOK
- Motivo: não foi possível executar navegador real contra backend publicado.

### william.lucas@sltconsult.com.br / Slt@2024

- Login: NOK
- Token: NOK
- Redirecionamento: NOK
- Permissões: NOK
- Motivo: não foi possível executar navegador real contra backend publicado.

### admin@consultslt.com.br / Consult@2026

- Login: NOK
- Token: NOK
- Redirecionamento: NOK
- Permissões: NOK
- Motivo: não foi possível executar navegador real contra backend publicado.

## O QUE FOI CONFIRMADO EM CÓDIGO

- `AuthContext` usa `api.post("/auth/login", ...)`.
- `apiClient` exige `REACT_APP_API_URL` e não usa fallback relativo para `/api`.
- O componente legado `EntraIDLogin.jsx` foi neutralizado.
- O backend possui os três usuários default no router de auth.
- O endpoint `POST /api/auth/login` existe no backend.

## ERROS ENCONTRADOS

- 405 Method Not Allowed: risco histórico, evitado no contrato local, mas não validado em produção real aqui.
- 401 Unauthorized: esperado para credenciais inválidas; não foi exercitado em navegador real.
- CORS: não validado contra backend público.
- URL incorreta: não validado em produção real.
- Backend offline: não foi possível testar com backend publicado.

## CAUSA RAIZ

- A autenticação está consistente no código local, mas o ambiente de produção não foi acessível para validar as requisições reais de navegador e as respostas HTTP reais.
- Sem `REACT_APP_API_URL` apontando para um backend público válido, o fluxo de login em GitHub Pages não pode ser confirmado de ponta a ponta.

## SOLUÇÃO APLICADA

- O cliente HTTP foi endurecido para falhar sem `REACT_APP_API_URL`.
- O workflow de Pages valida o secret antes do build.
- O login legado foi neutralizado.
- A suíte automatizada cobre o contrato de login e o build do Pages.

## PRÓXIMOS PASSOS

1. Publicar o backend em URL pública real.
2. Configurar `REACT_APP_API_URL` no GitHub Secrets.
3. Executar login real em navegador no GitHub Pages.
4. Validar JWT, refresh, logout e RBAC com o backend publicado.

## PRIORIDADE

ALTA
