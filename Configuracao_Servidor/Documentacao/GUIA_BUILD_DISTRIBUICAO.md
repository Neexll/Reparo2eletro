# 📦 Guia de Build e Distribuição - Reparo2Eletro

## 🎯 Objetivo

Criar uma **distribuição executável** do sistema que pode ser copiada e executada em qualquer servidor Windows **sem precisar instalar Python ou dependências**.

---

## 🚀 Como Criar a Distribuição

### Opção A: Automática (Recomendada)

```cmd
# Clique 2x ou execute no terminal:
build_server.bat
```

### Opção B: Manual

```cmd
# 1. Ative o ambiente virtual
venv\Scripts\activate

# 2. Instale PyInstaller
pip install pyinstaller

# 3. Execute o script de build
python build_server.py
```

---

## ⏱️ Tempo de Build

- **Primeira vez**: 5-10 minutos
- **Builds subsequentes**: 3-5 minutos

Durante o build, o PyInstaller irá:
1. Analisar todas as dependências
2. Compilar o código Python
3. Empacotar tudo em um executável
4. Criar a estrutura de distribuição

---

## 📁 O que é Criado

Após o build, você terá a pasta **`dist_servidor/`** contendo:

```
dist_servidor/
├── Reparo2Eletro_Server.exe    ← Executável principal
├── templates/                   ← Páginas HTML
├── static/                      ← CSS, JS, imagens
├── schema.sql                   ← Estrutura do banco
├── database.db                  ← Banco de dados (se existir)
├── LEIA-ME.txt                 ← Instruções
├── INICIAR_SERVIDOR.bat        ← Atalho para iniciar
├── CONFIGURAR_FIREWALL.bat     ← Configurar firewall
└── FAZER_BACKUP.bat            ← Fazer backup
```

---

## 📤 Como Distribuir

### Passo 1: Preparar a Distribuição

1. Execute `build_server.bat`
2. Aguarde o build completar
3. Verifique que a pasta `dist_servidor` foi criada

### Passo 2: Copiar para o Servidor

Escolha uma das opções:

**Opção A - Pendrive**
- Copie a pasta `dist_servidor` para um pendrive
- Conecte no servidor e cole a pasta

**Opção B - Rede Compartilhada**
- Mapeie uma unidade de rede do servidor
- Copie a pasta `dist_servidor`

**Opção C - Compactar e Enviar**
```cmd
# Compacte a pasta dist_servidor
# Envie por email, cloud storage, etc.
```

### Passo 3: Executar no Servidor

No servidor da empresa:

1. Abra a pasta `dist_servidor`
2. Execute `INICIAR_SERVIDOR.bat`
3. Anote a URL exibida
4. Configure o firewall (se necessário): `CONFIGURAR_FIREWALL.bat`
5. Compartilhe a URL com funcionários

---

## ✅ Vantagens da Distribuição

### Para o Servidor:
- ✓ **Não precisa Python** instalado
- ✓ **Não precisa dependências** (Flask, etc.)
- ✓ **Plug and Play** - copie e execute
- ✓ **Portátil** - funciona em qualquer Windows
- ✓ **Auto-contido** - tudo incluído

### Para Você:
- ✓ **Fácil de atualizar** - só criar novo build
- ✓ **Fácil de distribuir** - uma pasta apenas
- ✓ **Menos suporte** - usuários não mexem em código
- ✓ **Profissional** - parece software "de verdade"

---

## 🔄 Atualizando o Sistema

Quando você fizer mudanças no código:

```cmd
# 1. Teste suas mudanças localmente
python app.py

# 2. Crie novo build
build_server.bat

# 3. Substitua a pasta no servidor
# - Faça backup do database.db do servidor
# - Copie a nova dist_servidor
# - Restaure o database.db antigo
```

---

## ⚠️ Considerações Importantes

### Antivírus

Executáveis criados com PyInstaller podem ser detectados como "suspeitos" por antivírus (falso positivo). 

**Soluções:**
- Adicione exceção no antivírus para `Reparo2Eletro_Server.exe`
- Explique à equipe de TI que é um executável Python legítimo
- Use certificado de assinatura de código (opcional, para empresas grandes)

### Tamanho do Arquivo

O executável será **grande** (~50-100 MB) porque inclui:
- Interpretador Python
- Todas as bibliotecas (Flask, matplotlib, etc.)
- Templates e recursos

Isso é **normal** para aplicações PyInstaller.

### Banco de Dados

- O `database.db` pode ou não ser incluído no build
- Se incluído: será o estado inicial (vazio ou com dados de exemplo)
- O banco será criado automaticamente na primeira execução se não existir
- **Sempre faça backup** do database.db do servidor antes de atualizar

---

## 🆘 Solução de Problemas

### Erro: "PyInstaller não encontrado"

```cmd
pip install pyinstaller
```

### Erro: "Módulo não encontrado"

Edite `build_server.py` e adicione em `--hidden-import`:

```python
'--hidden-import=nome_do_modulo',
```

### Erro ao executar no servidor

1. Verifique se todas as pastas foram copiadas
2. Execute como Administrador (primeira vez)
3. Verifique logs no terminal
4. Adicione exceção no antivírus

### Build muito lento

Normal na primeira vez. PyInstaller precisa:
- Analisar todas as dependências
- Compilar bytecode
- Empacotar recursos

Builds subsequentes são mais rápidos.

### Executável não inicia

```cmd
# Execute no terminal para ver erros:
cd dist_servidor
Reparo2Eletro_Server.exe
```

---

## 🎯 Comparação: Build vs Instalação Manual

| Aspecto | Com Build | Sem Build (Manual) |
|---------|-----------|-------------------|
| **Instalação no Servidor** | Copiar pasta | Instalar Python + deps |
| **Tempo de Setup** | 2 minutos | 15-30 minutos |
| **Conhecimento Técnico** | Básico | Intermediário |
| **Atualizações** | Substituir pasta | Git pull + pip install |
| **Portabilidade** | Alta | Baixa |
| **Tamanho** | ~100 MB | ~500 MB (com Python) |
| **Manutenção** | Fácil | Requer conhecimento |

---

## 📝 Checklist de Distribuição

Antes de enviar para o servidor:

- [ ] Build criado com sucesso
- [ ] Pasta `dist_servidor` completa
- [ ] Testado localmente (executável funciona)
- [ ] README incluído
- [ ] Scripts batch incluídos
- [ ] Templates e static copiados
- [ ] Schema.sql incluído

No servidor:

- [ ] Pasta copiada completamente
- [ ] Firewall configurado (porta 5000)
- [ ] Executável com exceção no antivírus
- [ ] Servidor iniciado e URL anotada
- [ ] Testado acesso pela rede
- [ ] Funcionários conseguem acessar

---

## 🔐 Segurança

### Dados Sensíveis

Antes de criar o build:

1. **Remova** dados de teste do database.db
2. **Altere** a `secret_key` em `app.py`
3. **Não inclua** senhas ou tokens no código

### Recomendações:

```python
# app.py - Use variável de ambiente para secret_key
import os
app.secret_key = os.environ.get('SECRET_KEY', 'chave_padrao_para_dev')
```

---

## 💡 Dicas Profissionais

### 1. Versionamento

Adicione versão no executável:

```python
# build_server.py
'--name=Reparo2Eletro_Server_v1.0',
```

### 2. Ícone Personalizado

```python
# build_server.py
'--icon=icone.ico',  # Substitua NONE por caminho do ícone
```

### 3. Build Silencioso

Para builds automatizados:

```cmd
python build_server.py --quiet
```

### 4. Múltiplas Versões

Mantenha builds anteriores:

```cmd
dist_servidor_v1.0/
dist_servidor_v1.1/
dist_servidor_v1.2/
```

---

## 📞 Suporte

Se tiver problemas:

1. Verifique os logs durante o build
2. Teste o executável localmente antes de distribuir
3. Consulte documentação do PyInstaller: https://pyinstaller.org
4. Verifique issues comuns no GitHub do projeto

---

**Versão:** 1.0  
**Data:** 30/09/2025  
**Compatibilidade:** Windows 10/11, Python 3.8+
