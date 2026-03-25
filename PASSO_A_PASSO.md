# PASSO A PASSO — GITHUB WEB + STREAMLIT CLOUD

## 1. Criar repositório no GitHub

- Entre no GitHub
- Clique em **New repository**
- Defina o nome do repositório
- Crie vazio ou com README, como preferir

## 2. Subir os arquivos pelo GitHub web

Envie todos os arquivos desta pasta, inclusive:

- `app.py`
- `requirements.txt`
- pasta `app`
- pasta `.streamlit`

## 3. Publicar no Streamlit Cloud

- Entre no Streamlit Cloud
- Clique em **New app**
- Escolha o repositório e a branch
- Em **Main file path**, informe:

```text
app.py
```

## 4. Instalação automática

O Streamlit Cloud vai ler o arquivo `requirements.txt` e instalar tudo sozinho.

## 5. Uso do sistema

Depois do deploy:

- abra a aplicação
- envie os arquivos
- clique em **Processar arquivos**
- baixe o Excel gerado

## 6. Estrutura do projeto

### Arquivo principal do Streamlit

```text
app.py
```

### Núcleo do processamento

```text
app/main.py
```

### Interface

```text
app/ui/streamlit_app.py
```

## 7. Regra importante

Para o Streamlit Cloud, quem deve ser apontado como entrada é sempre:

```text
app.py
```

E não `app/main.py`.

## 8. Quando quiser atualizar

Como você vai usar só GitHub web:

- edite os arquivos direto no GitHub
- faça commit
- o Streamlit Cloud atualiza o app
