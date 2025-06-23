# GeoMapIFG: Monitoramento de Pastagens com NDVI e IA

## 📄 Descrição do Projeto

O GeoMapIFG é uma ferramenta em Python desenvolvida para o monitoramento e análise da saúde de áreas de pastagem, com foco na identificação de áreas degradadas. Ele utiliza dados de satélite Sentinel-2 através da API do Google Earth Engine (GEE) para calcular o Índice de Vegetação por Diferença Normalizada (NDVI) e classificar as pastagens em diferentes níveis de degradação. Além disso, integra a inteligência artificial Gemini para gerar descrições textuais concisas sobre as condições da área mapeada, transformando os dados geoespaciais em insights compreensíveis.

Este projeto visa auxiliar agrônomos, produtores rurais e pesquisadores na avaliação rápida e visual da produtividade e do estado de conservação de pastagens.

## ✨ Funcionalidades

- **Mapeamento de NDVI:** Calcula e visualiza o Índice de Vegetação por Diferença Normalizada (NDVI).
- **Classificação de Degradação:** Classifica as áreas de pastagem em categorias como "Degradação Severa", "Pastagem Estressada", "Pastagem Boa" e "Pastagem Excelente" com base em limiares de NDVI configuráveis.
- **Análise Estatística:** Fornece estatísticas de NDVI (mínimo, médio, máximo) e a distribuição percentual das classes de degradação para a Área de Interesse (AOI).
- **Geração de Descrição por IA:** Utiliza a API Gemini para criar um resumo textual inteligente sobre a saúde da pastagem, com base nos dados analisados.
- **Visualização Interativa:** Gera um arquivo HTML com um mapa Folium interativo, exibindo as camadas de satélite, NDVI, classificação de degradação e um painel de dashboard com todas as estatísticas e a descrição da IA.
- **Entrada Flexível:** Permite que o usuário forneça a Área de Interesse (AOI) através de dados GeoJSON de Polígono ou MultiPolígono.

## 🚀 Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado e configurado:

- **Python 3.8+:** [Download Python](https://www.python.org/downloads/)
- **Conta Google Cloud Platform (GCP):**
  - Necessária para criar um projeto e habilitar a API do Earth Engine.
  - [Console GCP](https://console.cloud.google.com/)
- **Acesso ao Google Earth Engine (GEE):**
  - Certifique-se de que sua conta Google tem acesso ao GEE.
  - [Google Earth Engine Sign Up](https://earthengine.google.com/signup/)
- **Conta Google AI Studio (Makersuite):**
  - Necessária para obter a chave de API Gemini.
  - [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências.

1.  **Clonar o Repositório:**
    Abra seu terminal/prompt de comando e clone o projeto:

    ```bash
    git clone https://github.com/luixsouza/GeoMapIFG.git
    cd GeoMapIFG
    ```

    _(Substitua `seu-usuario` e `GeoMapIFG` pelo caminho real do seu repositório)_

2.  **Criar e Ativar Ambiente Virtual (Altamente Recomendado):**
    É uma boa prática usar ambientes virtuais para isolar as dependências do projeto.

    ```bash
    python -m venv venv
    ```

    _Ativar o ambiente virtual:_

    - **Windows (PowerShell):**
      ```powershell
      .\venv\Scripts\Activate.ps1
      ```
    - **Windows (CMD):**
      ```cmd
      venv\Scripts\activate.bat
      ```
    - **Linux/macOS:**
      ```bash
      source venv/bin/activate
      ```

3.  **Instalar Dependências:**
    Com o ambiente virtual ativado, instale as bibliotecas necessárias:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar e Autenticar o CLI do Google Earth Engine:**
    O utilitário de linha de comando `earthengine` é essencial para a autenticação inicial.

    - **Instalação (geralmente já vem com `earthengine-api`):**

      ```bash
      pip install earthengine-api --upgrade
      ```

    - **Autenticação:**
      Em seu terminal, execute:

      ```bash
      earthengine authenticate
      ```

      Siga as instruções que aparecerão no seu navegador para fazer login com sua conta Google e conceder as permissões necessárias.

    - **Resolução de `earthengine` não reconhecido (Windows):** Se o comando `earthengine` não for reconhecido, o diretório `Scripts` da sua instalação Python (ou do seu ambiente virtual) pode não estar no `PATH` do sistema.

      - Descubra o caminho: `python -c "import site; print(site.USER_BASE + '\\Scripts')"` (para instalação de usuário) ou `.\venv\Scripts` (para ambiente virtual).
      - Adicione este caminho à variável de ambiente `Path` do Windows (Propriedades do Sistema \> Avançado \> Variáveis de Ambiente \> Variáveis do Sistema \> Path).
      - **Reinicie seu terminal ou computador** após alterar o `PATH`.

## ⚙️ Configuração

Você precisará configurar seu ID de Projeto GCP e sua Chave de API Gemini.

1.  **Criar o arquivo `.env`:**
    Na raiz do projeto (`GeoMapIFG/`), crie um arquivo chamado `.env` e adicione as seguintes linhas:

    ```
    # .env
    # Não comite este arquivo para repositórios públicos!
    GOOGLE_CLOUD_PROJECT_ID="SEU_ID_DO_PROJETO_GCP"
    GEMINI_API_KEY="SUA_CHAVE_API_GEMINI_AQUI"
    ```

    _(Substitua os placeholders pelos seus valores reais)_

2.  **Como Obter suas Chaves e IDs:**

    - **`GOOGLE_CLOUD_PROJECT_ID`:**

      1.  Vá para o [Console do Google Cloud](https://console.cloud.google.com/).
      2.  No canto superior esquerdo, clique no seletor de projeto (ao lado do logo do Google Cloud).
      3.  Crie um novo projeto ou selecione um existente.
      4.  Uma vez selecionado, o **ID do Projeto** estará visível no topo da página ou nas informações do projeto (é uma string alfanumérica, como `my-project-123456`).
      5.  Certifique-se de que a **"API do Earth Engine"** esteja habilitada para este projeto. Vá em "API e Serviços" \> "Biblioteca", pesquise por "Earth Engine API" e habilite-a.
      6.  Copie este ID para o seu arquivo `.env`.

    - **`GEMINI_API_KEY`:**

      1.  Vá para o [Google AI Studio (Makersuite)](https://makersuite.google.com/app/apikey).
      2.  Faça login com sua conta Google.
      3.  Clique em **"Create API key in new project"** ou **"Get API key"**.
      4.  Copie a chave de API gerada.
      5.  Cole esta chave no seu arquivo `.env`.

## 🚀 Uso

Com todas as dependências instaladas e as configurações no `.env` feitas, você pode executar a aplicação.

1.  **Navegue para a pasta PARENTE do seu projeto `GeoMapIFG` no terminal.**
    Por exemplo, se seu projeto está em `C:\Users\User\Desktop\GeoMapIFG`, navegue para `C:\Users\User\Desktop\`:
    ```bash
    cd C:\Users\User\Desktop\
    ```
2.  **Execute o script como um módulo Python:**
    ```bash
    python -m GeoMapIFG.main
    ```
3.  O script pedirá para você **colar os dados GeoJSON** da sua Área de Interesse (AOI). Cole o GeoJSON completo e pressione Enter.
    - **Importante:** Certifique-se de colar o GeoJSON como um bloco único, e que ele seja do tipo `Polygon` ou `MultiPolygon` com o anel fechado (o último ponto igual ao primeiro). Use ferramentas como [geojson.io](https://geojson.io/) para criar e validar seu GeoJSON.
4.  O script processará os dados, fará requisições ao Earth Engine e à API Gemini.
5.  Ao final, um arquivo HTML chamado `mapa_degradacao_pastagem.html` será salvo no diretório de onde você executou o comando.
6.  **Abra o arquivo `mapa_degradacao_pastagem.html`** em seu navegador web para visualizar o mapa interativo e o dashboard de análise.

## 📂 Estrutura do Projeto

```
GeoMapIFG/
├── main.py             # Ponto de entrada principal da aplicação.
├── config.py           # Configurações globais (IDs, chaves, limiares, cores).
├── data_utils.py       # Funções para entrada e processamento de dados GeoJSON.
├── ee_utils.py         # Funções para interação com a API do Google Earth Engine (GEE).
├── ai_analysis.py      # Funções para integração com a API Gemini e geração de texto.
├── map_utils.py        # Funções para criação e renderização de mapas Folium.
├── requirements.txt    # Lista de dependências Python.
└── .env                # Variáveis de ambiente.
```

## 📊 Limiares de Classificação NDVI

As classes de degradação da pastagem são baseadas em limiares de NDVI pré-definidos no `config.py`. É fundamental entender que esses limiares são **exemplos** e podem precisar ser ajustados/calibrados para a sua região específica ou tipo de pastagem, com base em conhecimento de campo ou literatura científica.

- **NDVI \< 0.15:** Degradação Severa
- **0.15 \<= NDVI \< 0.3:** Degradação Moderada
- **0.3 \<= NDVI \< 0.5:** Pastagem Estressada / Baixa Produtividade
- **0.5 \<= NDVI \< 0.7:** Pastagem Boa
- **NDVI \>= 0.7:** Pastagem Excelente / Alta Produtividade
