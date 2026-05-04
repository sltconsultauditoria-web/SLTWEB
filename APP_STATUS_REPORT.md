# APP_STATUS_REPORT

## STATUS GERAL

PARCIAL

## SCORE

67/100

## O QUE FUNCIONA

- O frontend compila com `PUBLIC_URL=/SLTWEB` e gera assets com base correta em `/SLTWEB/`.
- O contrato do `apiClient` está travado para falhar se `REACT_APP_API_URL` não existir.
- O `AuthContext` usa `api.post("/auth/login", ...)` e não monta URL manual no fluxo principal de login.
- O workflow de GitHub Pages existe, valida secret, publica `frontend/build` e gera fallback SPA com `404.html`.
- O fallback de SPA está presente em `frontend/public/404.html` e é copiado para o build.
- A suíte local passa: `76 passed, 1 skipped`.
- O build do frontend passa com `REACT_APP_API_URL=https://backend.publico.exemplo` e não contém `github.io/api` nem `"/api/auth/login"` relativo no bundle gerado.
- As rotas de frontend `"/login"` e `"/dashboard"` existem sob `basename="/SLTWEB"`.

## O QUE ESTÁ PARCIAL

- O GitHub Pages e o backend público não foram validados em runtime real neste workspace. A validação foi feita por build, leitura de código e suíte local.
- Os endpoints backend foram validados por testes automatizados, mas não com um servidor FastAPI publicado e acessado externamente.
- O teste de persistência real do MongoDB está marcado como `skipped`; então `consultslt_db` não foi comprovado com Mongo real neste ambiente.
- Worker/Redis, notificações, SharePoint, OCR e integrações fiscais não foram validados em serviços reais aqui; a evidência atual é de suíte local e contratos de código.
- O bundle do frontend ainda contém a string `localhost`, mas a ocorrência vem de dependências empacotadas, não do fluxo de login da aplicação. Mesmo assim, isso impede um scan literal “zero localhost” se esse for o critério final.
- O componente legado `frontend/src/components/EntraIDLogin.jsx` foi neutralizado e não monta mais URL manual de login.

## O QUE ESTÁ QUEBRADO

- Não há quebra confirmada no código local após build e testes.
- O problema 405 original só reaparece se a produção estiver sem `REACT_APP_API_URL` ou se o secret for configurado de forma incompatível com o contrato do cliente HTTP.
- A documentação operacional foi ajustada para deixar claro que o secret de produção deve apontar para a raiz pública do backend; o cliente HTTP faz a normalização de `/api` no fluxo relativo.

## BLOQUEADORES

- Falta validar o deploy real do GitHub Pages com o secret correto configurado.
- Falta validar a URL pública real do backend com CORS e JWT funcionando em runtime.
- Falta validar MongoDB real `consultslt_db` com persistência pós-restart.
- Falta validar Redis/worker em execução contínua com retries e logs reais.
- Falta validar SharePoint via Microsoft Graph com credenciais reais.
- Falta validar OCR, pipeline fiscal e integrações fiscais em ambiente real.

## RISCOS

- Se `REACT_APP_API_URL` não existir no GitHub Actions, o Pages falha corretamente no build, mas o deploy não acontece.
- Se o secret apontar para uma URL incompatível com o contrato do `axios.create`, o login pode voltar a falhar.
- Se o Pages publicar uma versão antiga por cache, a base URL errada pode persistir até novo deploy.
- Se o componente legado `EntraIDLogin.jsx` voltar a ser conectado no fluxo principal, ainda assim ele não deve reintroduzir URL manual porque foi neutralizado.
- A presença de strings de `localhost` no bundle pode gerar falso positivo em auditoria automatizada.

## VALIDAÇÕES REALIZADAS

- `python -m pytest tests -q`
- `python -m pytest tests/test_github_pages_frontend_contract.py -q`
- `python -m pytest tests/test_real_persistence.py -q`
- `cd frontend && npm run build`
- Scan do build para `github.io/api`
- Scan do build para `"/api/auth/login"`
- Scan do build para `localhost`

## LEITURA DOS ENDPOINTS

Observação: abaixo está a situação no workspace local; não é validação de produção publicada.

- `/health`: coberto por teste local, runtime real não validado.
- `/api/auth/login`: coberto por teste local e contrato de frontend, runtime real não validado.
- `/api/dashboard`: coberto por teste local, runtime real não validado.
- `/api/alertas`: coberto por teste local, runtime real não validado.
- `/api/events`: coberto por teste local, runtime real não validado.
- `/api/jobs`: coberto por teste local, runtime real não validado.
- `/api/notificacoes/metrics`: coberto por teste local, runtime real não validado.
- `/api/sharepoint/status`: coberto por teste local, runtime real não validado.

## PRÓXIMOS PASSOS

1. Publicar o backend em URL real e validar login, CORS e JWT no navegador.
2. Configurar `REACT_APP_API_URL` no GitHub Secrets com o backend raiz correto.
3. Executar o workflow de Pages e validar `/SLTWEB/login` e `/SLTWEB/dashboard` em runtime real.
4. Rodar `tests/test_real_persistence.py` com `RUN_REAL_MONGO_TESTS=1` contra Mongo real.
5. Validar worker/Redis, notificações, OCR, SharePoint e integrações fiscais em ambiente real.
6. Remover ou congelar o código legado `EntraIDLogin.jsx` para não reintroduzir URL manual.

## PRIORIDADE

ALTA
