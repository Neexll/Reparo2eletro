# 🖥️ Guia de Instalação - Servidor da Empresa

## 📋 Pré-requisitos

1. **Python 3.8 ou superior** instalado no servidor
2. Acesso administrativo ao servidor
3. Rede local funcional conectando servidor e estações de trabalho

---

## 🚀 Instalação no Servidor

### Passo 1: Preparar o Ambiente

```cmd
# Navegue até a pasta do projeto
cd C:\Users\Micro\Desktop\Reparo2eletro

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Passo 2: Inicializar o Banco de Dados

Se for a primeira execução, certifique-se de que o banco de dados está criado:

```cmd
python
>>> from app import init_db
>>> init_db()
>>> exit()
```

### Passo 3: Configurar Firewall do Windows

**Importante:** Libere a porta 5000 no firewall:

1. Abra o **Windows Defender Firewall**
2. Clique em **Configurações Avançadas**
3. Clique em **Regras de Entrada** > **Nova Regra**
4. Selecione **Porta** > Próximo
5. Escolha **TCP** e digite **5000** > Próximo
6. Marque **Permitir a conexão** > Próximo
7. Aplique para **Domínio, Privado e Público** > Próximo
8. Nomeie como "Reparo2Eletro" > Concluir

**OU execute este comando como Administrador no PowerShell:**

```powershell
New-NetFirewallRule -DisplayName "Reparo2Eletro" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

### Passo 4: Iniciar o Servidor

```cmd
# Com o ambiente virtual ativado
python server.py
```

Você verá algo como:

```
============================================================
🖥️  SERVIDOR REPARO2ELETRO - MODO REDE
============================================================

✅ Servidor iniciado com sucesso!

📍 IP do Servidor: 192.168.1.100
📍 Porta: 5000

🌐 URL de Acesso para Funcionários:
   http://192.168.1.100:5000/dashboard
```

---

## 👥 Acesso dos Funcionários

### Para funcionários acessarem:

1. **Abra qualquer navegador** (Chrome, Firefox, Edge, etc.)
2. **Digite a URL** fornecida pelo servidor: `http://192.168.1.100:5000/dashboard`
3. **Salve nos favoritos** para acesso rápido

### Criando atalhos nas estações de trabalho:

**Opção 1: Atalho no Desktop**

Crie um arquivo `.bat` no desktop dos funcionários:

```bat
@echo off
start http://192.168.1.100:5000/dashboard
```

**Opção 2: Atalho HTML**

Crie um arquivo `Reparo2Eletro.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=http://192.168.1.100:5000/dashboard">
</head>
<body>Abrindo Reparo2Eletro...</body>
</html>
```

---

## 🔧 Configuração Avançada

### Executar como Serviço do Windows (Opcional)

Para que o servidor inicie automaticamente com o Windows:

1. Instale o **NSSM** (Non-Sucking Service Manager):
   - Baixe em: https://nssm.cc/download
   
2. Execute como Administrador:

```cmd
nssm install Reparo2Eletro
```

3. Configure:
   - **Path**: `C:\Users\Micro\Desktop\Reparo2eletro\venv\Scripts\python.exe`
   - **Startup directory**: `C:\Users\Micro\Desktop\Reparo2eletro`
   - **Arguments**: `server.py`

4. Inicie o serviço:

```cmd
nssm start Reparo2Eletro
```

### Usar uma Porta Diferente

Se a porta 5000 já estiver em uso, edite `server.py`:

```python
port = 8080  # Altere para a porta desejada
```

---

## 🛠️ Manutenção

### Backup do Banco de Dados

Faça backup regular do arquivo `database.db`:

```cmd
copy database.db backup\database_2025-09-30.db
```

### Atualizar o Sistema

```cmd
# Pare o servidor (Ctrl+C)
# Ative o ambiente virtual
venv\Scripts\activate
# Atualize as dependências
pip install -r requirements.txt --upgrade
# Reinicie o servidor
python server.py
```

### Ver Logs de Acesso

Os logs de acesso aparecerão no terminal onde o servidor está rodando.

---

## ❓ Solução de Problemas

### Problema: "Endereço já em uso"

**Solução:** A porta 5000 já está sendo utilizada.

```cmd
# Encontre o processo usando a porta
netstat -ano | findstr :5000
# Finalize o processo (substitua PID pelo número encontrado)
taskkill /PID <PID> /F
```

### Problema: Funcionários não conseguem acessar

**Verificações:**

1. ✅ Firewall liberado?
2. ✅ Servidor e estações na mesma rede?
3. ✅ IP correto? Execute `ipconfig` no servidor
4. ✅ Servidor rodando? Verifique o terminal

```cmd
# Teste de conexão de uma estação
ping 192.168.1.100
telnet 192.168.1.100 5000
```

### Problema: Servidor lento com muitos usuários

**Soluções:**

1. Use um servidor de produção como **Waitress**:

```cmd
pip install waitress
```

Crie `server_production.py`:

```python
from waitress import serve
from app import app
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print(f"Servidor iniciado em http://{local_ip}:{port}/dashboard")
    serve(app, host='0.0.0.0', port=port, threads=10)
```

Execute com:

```cmd
python server_production.py
```

---

## 📞 Suporte

Para problemas técnicos:
1. Verifique os logs no terminal do servidor
2. Consulte a seção de Solução de Problemas
3. Verifique a conectividade de rede

---

## 📝 Notas Importantes

- ⚠️ **Não exponha o servidor à internet** sem medidas de segurança adequadas
- 🔒 O sistema foi projetado para uso em **rede local** apenas
- 💾 Faça **backups regulares** do banco de dados
- 🔄 Mantenha o **Python e dependências atualizadas**
- 👥 Para **mais de 20 usuários simultâneos**, considere usar Waitress ou Gunicorn

---

**Versão do Guia:** 1.0  
**Data:** 30/09/2025
