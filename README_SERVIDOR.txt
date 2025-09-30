================================================================================
         REPARO2ELETRO - CONFIGURAÇÃO PARA SERVIDOR DA EMPRESA
================================================================================

📌 RESUMO RÁPIDO
================================================================================

Agora você tem 4 formas de executar o sistema:

1. MODO DESKTOP (Local)
   - Arquivo: desktop.py ou start_server.bat
   - Uso: Apenas no computador local
   - Acesso: http://127.0.0.1:5000

2. MODO DISTRIBUIÇÃO (Build Executável) ⭐ MELHOR PARA SERVIDOR
   - Arquivo: build_server.bat (criar) → dist_servidor/ (usar)
   - Uso: Servidor sem Python instalado
   - Vantagens: Portátil, sem dependências, plug and play
   - Execute: build_server.bat para criar

3. MODO REDE (Servidor Simples)
   - Arquivo: server.py ou start_server_network.bat
   - Uso: Compartilhar com funcionários na rede (1-10 usuários)
   - Acesso: http://IP_DO_SERVIDOR:5000

4. MODO PRODUÇÃO (Servidor Robusto)
   - Arquivo: server_production.py
   - Uso: Muitos usuários simultâneos (10+ usuários)
   - Acesso: http://IP_DO_SERVIDOR:5000
   - Requer: pip install waitress


🚀 PASSO A PASSO RÁPIDO
================================================================================

1. Abra o terminal na pasta do projeto

2. Crie e ative o ambiente virtual:
   python -m venv venv
   venv\Scripts\activate

3. Instale as dependências:
   
   PARA MODO REDE:
   pip install -r requirements.txt
   
   PARA MODO PRODUÇÃO (recomendado):
   pip install -r requirements_production.txt

4. Libere a porta no Firewall:
   - Painel de Controle > Firewall do Windows > Configurações Avançadas
   - Nova Regra de Entrada > Porta TCP 5000 > Permitir
   
   OU execute como Administrador no PowerShell:
   New-NetFirewallRule -DisplayName "Reparo2Eletro" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow

5. Inicie o servidor:
   
   MODO REDE:
   python server.py
   
   MODO PRODUÇÃO:
   python server_production.py
   
   OU clique duas vezes em:
   start_server_network.bat

6. Copie a URL que aparece e compartilhe com os funcionários
   Exemplo: http://192.168.1.100:5000/dashboard


📖 DOCUMENTAÇÃO COMPLETA
================================================================================

Para instruções detalhadas, leia:
GUIA_INSTALACAO_SERVIDOR.md


🆘 PRECISA DE AJUDA?
================================================================================

PROBLEMA: "Porta já em uso"
SOLUÇÃO: 
  netstat -ano | findstr :5000
  taskkill /PID <NUMERO_DO_PID> /F

PROBLEMA: "Funcionários não conseguem acessar"
SOLUÇÃO:
  1. Verifique o firewall
  2. Confirme que estão na mesma rede
  3. Use o IP correto (execute ipconfig no servidor)
  4. Teste: ping IP_DO_SERVIDOR

PROBLEMA: "Sistema lento"
SOLUÇÃO:
  Use o modo produção (server_production.py)


💡 DICAS
================================================================================

✓ Faça backup regular do arquivo database.db
✓ Mantenha o terminal do servidor aberto
✓ Anote a URL e crie atalhos para os funcionários
✓ Para fechar o servidor: pressione Ctrl+C no terminal


================================================================================
Versão: 1.0 | Data: 30/09/2025
================================================================================
