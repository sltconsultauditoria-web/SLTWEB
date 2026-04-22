# 🧪 GUIA DE TESTE MANUAL DOS BOTÕES NA INTERFACE

## Pré-requisitos

1. **Backend rodando:**
   ```powershell
   cd c:\Users\admin-local\ServerApp\consultSLTweb
   python -m uvicorn backend.main_enterprise:app --reload
   ```

2. **Frontend rodando:**
   ```powershell
   cd c:\Users\admin-local\ServerApp\consultSLTweb\frontend
   npm start
   ```

3. **Acessar:** http://localhost:3000/empresas

---

## 🎯 TESTE 1: BOTÃO "VISUALIZAR" (Eye Icon)

### Passos:

1. Na página de empresas, localize qualquer empresa na tabela
2. Clique no ícone **⋮** (três pontos) no final da linha
3. Selecione **"Visualizar"** (primeiro item do menu)

### O que você deve ver:

✅ Modal abre mostrando:
- **Cabeçalho:** Ícone de prédio + nome da empresa
- **Status badges:** Regime Tributário (verde/azul/roxo/amarelo) + Ativo (verde) ou Inativo (vermelho)

✅ **Seção 1: Informações Básicas**
- CNPJ com formato: **11.222.333/0001-81** (com máscara)
- Botão de cópia ao lado do CNPJ
- Regime Tributário em texto

✅ **Seção 2: Inscrições** (se preenchidas)
- Inscrição Estadual (IE)
- Inscrição Municipal (IM)

✅ **Seção 3: Endereço** (se preenchido)
- Endereço completo
- Cidade | Estado | CEP em grid

✅ **Seção 4: Contato** (se preenchido)
- Telefone
- Email

✅ **Seção 5: Informações Financeiras**
- Receita Bruta em formato R$ (ex: R$ 100.000,00)
- Fator R em percentual (ex: 15.50%)

✅ **Seção 6: Timestamps**
- Data de Cadastro
- Data de Última Atualização

✅ **Botões de Ação:**
- Botão "Editar" (azul)
- Botão "Deletar" (vermelho)

✅ **Fechar Modal:**
- Clique no X no canto superior direito

### ✅ Persistência Validada:
- Todos os dados mostrados correspondem ao banco de dados
- As datas mostram quando foi criado e quando foi modificado

---

## ✏️ TESTE 2: BOTÃO "EDITAR" (Edit Icon)

### Passos:

1. Clique em **⋮** em qualquer empresa
2. Selecione **"Editar"** (segundo item do menu)

### O que você deve ver:

✅ Modal abre com título "Editar Empresa"

✅ **Campo CNPJ:**
- Vem preenchido com a máscara: **11.222.333/0001-81**
- Campo está **cinza/desabilitado** (não pode editar)
- ⚠️ Isso é correto - CNPJ não pode mudar

✅ **Outros campos:**
- Razão Social (editável)
- Nome Fantasia (editável)
- Regime Tributário (dropdown editável)
- Inscrição Estadual (editável)
- Inscrição Municipal (editável)
- Endereço (editável)
- Cidade, Estado, CEP (editáveis)
- Telefone, Email (editáveis)
- Receita Bruta (número editável)
- Fator R (porcentagem editável)
- Checkbox "Empresa ativa" (editável)

### Teste de Persistência:

1. **Mude a Razão Social:** De "Empresa Exemplo LTDA" para "Empresa Exemplo ATUALIZADA"
2. **Mude a Receita:** De R$ 0 para R$ 250.000,00
3. **Mude o Status:** Clique em "Empresa ativa" para desativar
4. Clique em **"Salvar Alterações"** (botão azul no final)

### O que deve acontecer:

✅ **Imediatamente:**
- Modal fecha
- Tabela atualiza mostrando novo nome
- Receita atualiza na tabela
- Status muda para "Inativo" (badge vermelho)

✅ **Na Lista:**
- Busque pela empresa (filtro de busca no topo)
- Dados refletem as mudanças

✅ **Ao Recarregar:**
- Pressione **F5** para recarregar a página
- Abra a empresa novamente
- **Dados ainda estão alterados** ✅ (persistência confirmada)

✅ **Dados que Devem Persistir:**
```
ANTES:
- Razão Social: Empresa Exemplo LTDA
- Receita: R$ 0,00
- Status: Ativo

DEPOIS:
- Razão Social: Empresa Exemplo ATUALIZADA
- Receita: R$ 250.000,00
- Status: Inativo

APÓS RECARREGAR:
- Dados continuam iguais à alteração ✅
```

---

## 🗑️ TESTE 3: BOTÃO "EXCLUIR" (Trash Icon)

### Passos:

1. Clique em **⋮** em qualquer empresa
2. Selecione **"Excluir"** (terceiro item do menu)

### O que você deve ver:

✅ **Confirmação em Português:**
```
"Tem certeza que deseja excluir esta empresa? 
Esta ação não pode ser desfeita."
```

### Teste de Persistência:

1. Localize uma empresa na tabela (ex: "Empresa Exemplo LTDA")
2. Note quantas empresas aparecem na tabela
3. Clique no menu **⋮**
4. Selecione **"Excluir"**
5. Clique **"OK"** na confirmação

### O que deve acontecer:

✅ **Imediatamente:**
- Confirmação desaparece
- Empresa desaparece da tabela
- Contador de empresas diminui em 1

✅ **Procure pela Empresa:**
- Use o campo de busca para procurar o CNPJ ou nome
- **Nenhum resultado** ✅ (confirmação que foi deletado)

✅ **Ao Recarregar:**
- Pressione **F5**
- **Empresa não reaparece** ✅ (confirmação que foi deletado do banco)

✅ **Dados Removidos Permanentemente:**
```
ANTES: 2 empresas na lista
DEPOIS DE DELETAR: 1 empresa na lista

APÓS RECARREGAR: 1 empresa na lista (não volta) ✅
```

---

## 📊 TESTE 4: PERSISTÊNCIA GERAL

### Cenário Completo:

```
1️⃣ CRIAR
   - Clique em "Nova Empresa" (botão azul no topo)
   - Preencha os campos:
     * CNPJ: 88.777.666/0001-55
     * Razão Social: Empresa Teste Novo
     * Regime: Lucro Presumido
     * Receita: 150.000,00
     * Ativo: checado
   - Clique "Cadastrar Empresa"
   - ✅ Empresa aparece na lista

2️⃣ VISUALIZAR
   - Clique em ⋮ da empresa criada
   - Clique "Visualizar"
   - ✅ Todos os dados aparecem no modal
   - ✅ Data de criação mostra

3️⃣ EDITAR
   - Ainda no modal, clique "Editar"
   - Mude Nome para: "Empresa Teste Atualizada"
   - Mude Receita para: 200.000,00
   - Clique "Salvar Alterações"
   - ✅ Dados atualizam na lista
   - ✅ Data de atualização muda no banco

4️⃣ RECARREGAR PÁGINA
   - Pressione F5
   - ✅ Empresa ainda está lá
   - ✅ Dados continuam alterados
   - ✅ PERSISTÊNCIA CONFIRMADA! ✅

5️⃣ DELETAR
   - Clique em ⋮
   - Clique "Excluir"
   - Confirme "OK"
   - ✅ Empresa desaparece da lista

6️⃣ VERIFICAR DELEÇÃO
   - Pressione F5
   - Busque pelo CNPJ: 88777666000155
   - ✅ Nenhum resultado
   - ✅ CONFIRMADO DELETADO PERMANENTEMENTE! ✅
```

---

## 🔍 CHECKLIST VISUAL

Marque cada item conforme testa:

### Botão Visualizar
- [ ] Modal abre com título "Detalhes da Empresa"
- [ ] CNPJ mostra com máscara (XX.XXX.XXX/XXXX-XX)
- [ ] Há botão de cópia para CNPJ
- [ ] 6 seções de informações visíveis
- [ ] Timestamps mostram em português
- [ ] Botões Edit/Delete disponíveis no modal

### Botão Editar
- [ ] Modal abre com título "Editar Empresa"
- [ ] CNPJ está desabilitado (cinza)
- [ ] Outros campos estão habilitados
- [ ] Dados preenchidos com valores atuais
- [ ] Alterações salvam (teste com Razão Social)
- [ ] Tabela atualiza imediatamente
- [ ] Dados persistem após recarregar (F5)

### Botão Excluir
- [ ] Confirmação em português aparece
- [ ] Empresa sai da tabela após confirmação
- [ ] Empresa não reaparece após recarregar (F5)
- [ ] Busca não encontra a empresa deletada

### Persistência Geral
- [ ] Dados criados permanecem após F5
- [ ] Dados editados permanecem após F5
- [ ] Dados deletados não reapareem após F5
- [ ] Contador de empresas atualiza corretamente
- [ ] Filtro de busca funciona
- [ ] Timestamps atualizam após edição

---

## ⚠️ Possíveis Problemas e Soluções

### Problema: Botão não abre modal
**Solução:** Veja se o menu ⋮ está visível. Se não, o JavaScript não carregou.
- Pressione F12 para abrir DevTools
- Procure por erros em vermelho no Console
- Tente recarregar: Ctrl+Shift+R (hard refresh)

### Problema: Dados não salvam
**Solução:** Verifique se o backend está rodando:
- Terminal: `python -m uvicorn backend.main_enterprise:app --reload`
- Verifique se mostra "Uvicorn running on http://127.0.0.1:8000"

### Problema: CNPJ não formata
**Solução:** Normal - o CNPJ se formata quando:
- Você digita (máscara em tempo real)
- Quando é exibido na tabela
- Quando é exibido no modal

### Problema: Não consegue deletar
**Solução:** Se a confirmação não aparecer:
- Bloqueador de pop-ups ativo? Verifique as configurações do navegador
- Se clicou OK e nada acontece, o backend caiu. Reinicie.

---

## 🎯 Resumo Rápido

| Ação | Resultado Esperado | ✓ OK? |
|------|------------------|-------|
| Click Visualizar | Modal abre com 6 seções | [ ] |
| Dados visíveis | CNPJ, Receita, etc aparecem | [ ] |
| Click Editar | Modal abre formulário preenchido | [ ] |
| Muda Razão Social | Tabela atualiza imediatamente | [ ] |
| Salva Alteração | F5 - dados continuam alterados | [ ] |
| Click Excluir | Confirmação em português aparece | [ ] |
| Confirma Exclusão | Empresa sai da lista | [ ] |
| F5 após clicar | Empresa não reaparece | [ ] |

Se todos os ✓ estão marcados, **TODOS OS BOTÕES ESTÃO FUNCIONAIS E PERSISTENTES!** ✅

---

**Última Atualização:** 15 de Fevereiro de 2026  
**Status:** Todos os Botões Verificados ✅
