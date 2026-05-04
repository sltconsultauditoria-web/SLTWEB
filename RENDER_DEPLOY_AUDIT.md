# Render Deploy Audit

## Estado local

- Branch atual do workspace: `release-auditoria`
- `refs/heads/main`: `c3eeec32f52889e3c76aad0a3e9cb13898eb7c30`
- `refs/remotes/origin/main`: `5ffbff789cb05ec58a1cfeb3dbf9c75f8874d638`
- `refs/heads/release-auditoria`: `926f8014a9e97c08f8ca9058a0a8088e27c70bd5`

## Último commit local em `main`

- Hash: `c3eeec32f52889e3c76aad0a3e9cb13898eb7c30`
- Mensagem: `backend/.git/COMMIT_EDITMSG`
- Data: `2026-04-18T19:37:38-03:00`

## Commit mais novo no workspace

- Hash: `926f8014a9e97c08f8ca9058a0a8088e27c70bd5`
- Branch: `release-auditoria`

## Commit do `origin/main`

- Hash: `5ffbff789cb05ec58a1cfeb3dbf9c75f8874d638`
- Mensagem: `fix: force production api url for pages login`

## Comparação

O workspace não está sincronizado com a `main` do GitHub.

- `main` local está diferente de `origin/main`.
- O branch atual `release-auditoria` está à frente do `origin/main`.
- O Render, se configurado para acompanhar `main`, provavelmente ainda usa um commit anterior ao mais novo do workspace.

## Configuração atual do Render blueprint

- `branch: main`
- `autoDeploy: true`
- `startCommand: uvicorn backend.main_enterprise:app --host 0.0.0.0 --port $PORT`
- `healthCheckPath: /health`
- `runtime: python`
- `PYTHON_VERSION: 3.11.11`

## Causas prováveis de divergência

1. O commit mais novo não foi promovido para `main` no GitHub.
2. O Render estava com `autoDeploy` desativado antes da correção.
3. O Render pode estar usando cache de build.
4. O deploy manual pode ter ficado preso em commit antigo.

## Correções práticas

1. Tornar `main` o branch efetivo de publicação no GitHub.
2. Fazer push do commit mais novo para `main`.
3. No Render, acionar **Clear build cache and deploy**.
4. Confirmar no painel do Render que o deploy aponta para o hash mais novo.

## Limitação desta auditoria

Não há acesso ao painel do Render nem à rede externa do GitHub a partir deste workspace, então o hash real em produção não pode ser validado aqui.

## Comandos para validação local

```bash
git status
git branch --show-current
git log -5 --oneline
git log -1 --oneline main
git log -1 --oneline release-auditoria
git push origin main
```
