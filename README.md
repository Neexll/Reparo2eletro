# Reparo2Eletro - Sistema de Gerenciamento de Assistência Técnica

## Instalação

### Requisitos do Sistema
- Windows 10 ou superior
- Python 3.8 ou superior
- Acesso de administrador para instalação

### Instalação Automática (Recomendado)

1. Faça o download do instalador `Reparo2Eletro_Installer.exe` da pasta `dist`
2. Execute o instalador como administrador (clique com o botão direito e selecione "Executar como administrador")
3. Siga as instruções na tela
4. Um atalho será criado na área de trabalho

### Instalação Manual

1. Instale o Python 3.8 ou superior a partir do [site oficial](https://www.python.org/downloads/)
2. Marque a opção "Add Python to PATH" durante a instalação
3. Baixe ou clone este repositório
4. Abra um terminal na pasta do projeto e execute:
   ```
   pip install -r requirements.txt
   ```
5. Execute o arquivo `desktop.py`

## Como Usar

1. Execute o atalho na área de trabalho
2. O sistema abrirá automaticamente no navegador padrão
3. Para acessar de outros dispositivos na rede local, use o endereço IP exibido no terminal

## Configuração de Rede

O sistema está configurado para rodar na porta 5000. Para acessar de outros dispositivos na rede local:

1. Verifique o endereço IP do computador onde o servidor está rodando
2. Em outro dispositivo na mesma rede, acesse: `http://[IP_DO_SERVIDOR]:5000`

## Backup dos Dados

O banco de dados está localizado em:
- `C:\Program Files\Reparo2Eletro\database.db`

Recomenda-se fazer backup regular deste arquivo.

## Suporte

Para suporte ou relato de problemas, entre em contato com o suporte técnico.
