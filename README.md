# Conciliador Universal — GitHub Web + Streamlit Cloud

Projeto preparado para rodar **somente com GitHub web + Streamlit Cloud**.

## Estrutura principal

- `app.py` → arquivo principal que o Streamlit Cloud executa
- `app/main.py` → motor de processamento
- `app/ui/streamlit_app.py` → interface
- `requirements.txt` → dependências do projeto

## Como publicar no Streamlit Cloud

1. Suba esta pasta inteira para um repositório no GitHub.
2. Acesse o Streamlit Cloud.
3. Clique em **New app**.
4. Conecte sua conta GitHub, escolha o repositório e a branch.
5. Em **Main file path**, informe:

```text
app.py
```

6. Clique em **Deploy**.

## Como funciona

O usuário envia um ou mais arquivos:

- PDF
- TXT
- CSV
- XLS
- XLSX

O sistema:

1. lê os arquivos
2. reconstrói linhas quebradas no histórico
3. normaliza nomes de colunas
4. identifica bases com débito/crédito
5. roda a conciliação
6. gera um Excel para download

## Regra principal do projeto

Quando a base tiver colunas de **Débito** e **Crédito**, o sistema trata como **razão contábil**:

- todo **crédito** precisa ser localizado
- **débitos** podem sobrar como pendência ou em aberto

## Deploy esperado

No Streamlit Cloud, o sistema deve abrir pela interface web e permitir:

- upload de arquivos
- processamento
- download do Excel final

## Observação

O `app/main.py` continua sendo o núcleo do programa. O `app.py` apenas chama a interface Streamlit de forma compatível com deploy web.
