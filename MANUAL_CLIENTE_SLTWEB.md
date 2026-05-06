# SLTWEB - Manual Completo do Cliente

## 1. Objetivo

Este manual descreve o uso operacional do SLTWEB para perfis `admin` e `viewer`, cobrindo login, navegação, principais telas, integrações, relatórios e troubleshooting.

## 2. Acesso

- Frontend: `https://sltconsultauditoria-web.github.io/SLTWEB/`
- Login: `https://sltconsultauditoria-web.github.io/SLTWEB/login`
- Backend: `https://sltweb.onrender.com`
- Swagger: `https://sltweb.onrender.com/docs`

## 3. Perfis

### Admin

- Acesso completo ao sistema.
- Pode cadastrar, editar e excluir dados.
- Pode sincronizar integrações e executar rotinas administrativas.

### Viewer

- Acesso de consulta e operação assistida.
- Não acessa telas administrativas restritas.
- Não executa ações destrutivas.

## 4. Manual de Acesso e Login

**Perfil necessário:** `admin` ou `viewer`  
**Objetivo:** entrar no sistema e validar a sessão.

### Passo a passo

1. Acesse a tela de login.
2. Informe e-mail e senha.
3. Clique em `Entrar`.
4. Aguarde o redirecionamento para o `Dashboard`.

### Resultado esperado

- O sistema abre o dashboard do usuário autenticado.
- O menu lateral é carregado conforme o perfil.

### Erros comuns

- Credenciais inválidas.
- Sessão expirada.
- Token ausente ou inválido.

## 5. Dashboard

**Objetivo:** apresentar visão executiva com KPIs fiscais, obrigações, alertas e integrações.

### Como usar

1. Abra o menu `Dashboard`.
2. Analise os cards de resumo.
3. Consulte os gráficos e listas de pendências.
4. Verifique alertas e vencimentos próximos.

### O que observar

- Total de empresas.
- Obrigações em dia, vencendo e atrasadas.
- Alertas críticos.
- Status de integrações.

### Resultado esperado

- Painel com dados carregados da API.
- Empty state quando não houver dados.

## 6. Empresas

**Objetivo:** cadastrar e manter empresas com seus dados fiscais.

### Campos principais

- CNPJ
- Razão social
- Nome fantasia
- Regime tributário
- UF
- Status

### Passo a passo

1. Abra `Empresas`.
2. Use a busca para localizar uma empresa.
3. Clique em `Nova empresa` para criar.
4. Preencha os campos obrigatórios.
5. Salve.

### Resultado esperado

- Empresa aparece na listagem.
- CNPJ deve ser digitado com máscara `00.000.000/0000-00`.

### Erros comuns

- CNPJ inválido.
- Campos obrigatórios ausentes.

## 7. Documentos

**Objetivo:** centralizar documentos recebidos e vinculá-los às empresas.

### Passo a passo

1. Abra `Documentos`.
2. Filtre por empresa, tipo ou status.
3. Faça upload ou selecione um documento existente.
4. Vincule ao cadastro correto, quando aplicável.
5. Baixe ou exclua conforme permissão.

### Relacionamento com OCR

- Documentos podem ser processados automaticamente.
- O OCR pode extrair CNPJ, valores, datas e texto.

## 8. OCR

**Objetivo:** extrair dados automaticamente de arquivos.

### Passo a passo

1. Abra `OCR`.
2. Selecione um arquivo PDF, PNG, JPG ou JPEG.
3. Envie o arquivo.
4. Acompanhe o status de processamento.
5. Revise o texto extraído.

### Estados esperados

- `pendente`
- `processando`
- `concluido`
- `erro`

### Erros comuns

- Tipo de arquivo não suportado.
- Arquivo corrompido.
- Falha no reconhecimento.

## 9. Obrigações

**Objetivo:** acompanhar obrigações por empresa, competência e status.

### Passo a passo

1. Abra `Obrigações`.
2. Filtre por empresa, regime, competência ou status.
3. Consulte o calendário fiscal.
4. Marque como entregue quando aplicável.

### Status principais

- `em_dia`
- `vencendo`
- `vence_hoje`
- `atrasada`
- `entregue`
- `dispensada`
- `nao_aplicavel`

## 10. Catálogo de Obrigações

**Objetivo:** consultar as regras fiscais do catálogo interno.

### Como usar

1. Abra `Catálogo Fiscal`.
2. Pesquise por código ou nome.
3. Filtre por regime tributário.
4. Abra o detalhe para ver prazos, campos, validações e penalidades.

### Exemplos

- eSocial
- PGDAS-D
- DCTFWeb
- EFD-Reinf

## 11. Relatórios

**Objetivo:** gerar e exportar relatórios operacionais.

### Passo a passo

1. Abra `Relatórios`.
2. Use os filtros disponíveis.
3. Exporte em PDF ou Excel.
4. Baixe o arquivo gerado.

### Resultado esperado

- PDF é baixado corretamente.
- Excel é baixado em `.xlsx`.

## 12. Alertas

**Objetivo:** acompanhar eventos fiscais e operacionais.

### Como usar

1. Abra `Alertas`.
2. Verifique prioridade e status.
3. Marque como lido.
4. Resolva quando necessário.

### Prioridades

- crítica
- alta
- média
- baixa

## 13. Configurações

**Objetivo:** visualizar parâmetros do sistema e atalhos administrativos.

### Observação

- Algumas opções aparecem apenas para `admin`.
- Perfis comuns devem ver apenas opções permitidas.

## 14. Gestão de Usuários Viewer

**Perfil necessário:** `admin`

### Passo a passo

1. Acesse `Configurações`.
2. Abra `Gestão de Usuários Viewer`.
3. Clique em `Criar Viewer`.
4. Preencha nome, e-mail e senha.
5. Salve.
6. Edite ou exclua conforme necessidade.

### Regras

- Apenas admin acessa.
- Viewer não cria usuário.
- Viewer não exclui usuário.
- A role é fixa como `viewer`.

## 15. Perfil Viewer

**Perfil necessário:** `viewer`

### O que o viewer pode fazer

- Acessar dashboard.
- Consultar páginas operacionais permitidas.
- Visualizar status e relatórios conforme RBAC.

### O que o viewer não pode fazer

- Criar usuários.
- Excluir usuários.
- Executar rotinas administrativas.

## 16. Robôs / Ingestão

**Objetivo:** acompanhar automações e ingestão de arquivos.

### Passo a passo

1. Abra `Robôs`.
2. Consulte status, histórico e arquivos.
3. Admin pode iniciar/parar/executar quando habilitado.

### Status esperados

- `idle`
- `running`
- `error`

## 17. SharePoint / Integrações

**Objetivo:** verificar a conectividade com Microsoft Graph/SharePoint.

### Status possíveis

- `real`
- `simulado`
- `log_only`
- `not_configured`

### Como interpretar

- `real`: conexão pronta.
- `simulado`: retorno estruturado sem integração oficial completa.
- `log_only`: apenas registro local.
- `not_configured`: variáveis ausentes.

## 18. Fiscal

**Objetivo:** cálculos fiscais e consultas operacionais.

### Funcionalidades

- Cálculo de DAS.
- Fator R.
- Consulta de certidões e débitos.

### Resultado esperado

- Ações retornam status claro e mensagem legível.

## 19. Auditoria

**Objetivo:** consultar eventos, trilhas e estatísticas.

### Como usar

1. Abra `Auditoria`.
2. Filtre por período ou severidade.
3. Verifique eventos e estatísticas.

## 20. Certidões, Débitos e Guias

**Objetivo:** consultar dados fiscais relacionados à empresa.

### Como usar

1. Abra a tela correspondente.
2. Filtre por CNPJ/empresa.
3. Analise a situação.

## 21. Notificações

**Objetivo:** acompanhar canais, preferências e logs de envio.

### Status

- canais configurados
- logs
- métricas
- fallback polling/WebSocket

## 22. Troubleshooting

### Login inválido

- Verifique e-mail e senha.
- Confirme se a conta está ativa.

### 401

- Token ausente ou expirado.

### 403

- Perfil sem permissão para a ação.

### 404

- Rota ou recurso inexistente.

### 405

- Método HTTP incorreto ou deploy desatualizado.

### SharePoint not_configured

- Configure variáveis `AZURE_*` e `SHAREPOINT_*`.

### Integração simulada

- Não é erro; significa que a funcionalidade ainda está em modo simulado.

### Download não inicia

- Verifique bloqueio do navegador.
- Confirme se o backend respondeu com `Content-Disposition`.

### OCR falha

- Verifique formato e integridade do arquivo.

## 23. Organização do manual

Este manual consolidado deve ser dividido no Scribe em:

1. Acesso e Login
2. Visão Geral
3. Perfil Admin
4. Perfil Viewer
5. Módulos Operacionais
6. Módulos Fiscais
7. Relatórios
8. Configurações
9. Integrações
10. Troubleshooting

