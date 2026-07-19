# Procura-Estágio Bot

Este projeto é um bot de Telegram que automatiza a busca por vagas de estágio/oportunidades de desenvolvimento, filtra-as com base em critérios específicos e as notifica em um canal do Telegram. Ele utiliza uma API externa para buscar as vagas, um banco de dados SQLite para evitar duplicatas e envia notificações formatadas.

## Funcionalidades

*   Busca automática de vagas em múltiplas páginas de uma API externa.
*   Filtra vagas por palavras-chave relevantes para estágios em desenvolvimento (backend, frontend, etc.).
*   Filtra vagas que são remotas ou localizadas em Salvador - BA.
*   Salva novas vagas encontradas em um banco de dados SQLite para evitar duplicidade.
*   Envia notificações formatadas via bot do Telegram para um canal específico.
*   Execução periódica configurável (atualmente a cada 4 horas).

## Começando

Este projeto requer Python 3.10+ e algumas bibliotecas.

### 1. Pré-requisitos e Criação do Bot no Telegram

Para rodar esta aplicação, você precisará:

*   **Python 3.10+**: Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
*   **Docker (Opcional, mas recomendado para consistência)**: Para rodar a aplicação em um ambiente isolado e consistente, o Docker é recomendado. Você pode baixá-lo em [docker.com](https://www.docker.com/get-started/).

#### 1.1. Criando um Bot no Telegram e Obtendo Credenciais

Se você nunca interagiu com a API do Telegram para criar bots, siga estes passos:

1.  **Abra o Telegram e procure por `@BotFather`**: Este é o bot oficial do Telegram para gerenciar outros bots.
2.  **Inicie uma conversa com `@BotFather`**: Digite `/start` para ver os comandos disponíveis.
3.  **Crie um novo bot**: Digite `/newbot`. O BotFather pedirá um **nome** para o seu bot (por exemplo, "Procura Estágio Bot") e um **username** para ele. O username **deve terminar com `bot`** (por exemplo, `procura_estagio_bot` ou `meu_bot_de_vagas_bot`).
4.  **Salve seu `TOKEN_BOT`**: Após criar o bot com sucesso, o BotFather fornecerá um **token de acesso HTTP API**. Este token é a chave para controlar o seu bot. **Guarde-o em segurança**, pois ele concede acesso total ao seu bot. O token se parece com `1234567890:ABC-DEF1234ghIkl-xyz567890efgh`.
5.  **Crie um Canal no Telegram**:
    *   Abra o Telegram, vá em "Novo Grupo" ou "Novo Canal" (dependendo da sua preferência, mas um canal é ideal para notificações em massa).
    *   Selecione a opção "Canal".
    *   Dê um nome ao seu canal (ex: "Vagas de Estágio TI").
    *   Escolha se o canal será público ou privado. Para fins de notificação, um canal privado é geralmente mais adequado para controlar quem recebe as mensagens. Se for privado, anote o link que o BotFather pode gerar para você.
6.  **Adicione seu Bot ao Canal**:
    *   Depois de criar o canal, vá nas configurações do canal e adicione seu bot recém-criado como **administrador**. Conceda a ele permissão para "Enviar mensagens".
7.  **Obtenha o `CHAT_ID` do Canal**:
    *   **Método 1 (Recomendado: Usando `@RawDataBot`)**: Adicione o bot `@RawDataBot` ao seu canal como membro (não precisa ser admin). Envie qualquer mensagem para o seu canal (pode ser algo como "teste"). O `@RawDataBot` responderá na conversa privada com ele, mostrando os dados brutos da mensagem. Procure pelo campo `"chat"` e, dentro dele, o valor de `"id"`. Esse é o seu `CHAT_ID`. Ele será um número negativo (ex: `-1001234567890`).
    *   **Método 2 (Encaminhando mensagem)**: Encaminhe qualquer mensagem do seu canal para um bot como `@JsonDumpBot` ou `@ShowJsonBot`. Ele retornará os detalhes da mensagem, incluindo o `CHAT_ID` do canal de origem.
    *   **Anote o `CHAT_ID`**.

### Configuração do Projeto

1.  **Clonar o repositório**:
    ```bash
    git clone https://github.com/seu-usuario/procura-estagio.git
    cd procura-estagio
    ```
    *(Substitua `https://github.com/seu-usuario/procura-estagio.git` pela URL do seu repositório)*

2.  **Criar um Ambiente Virtual (Recomendado)**:
    ```bash
    python -m venv venv
    # Ative o ambiente virtual:
    # No Windows:
    # venv\Scripts\activate
    # No macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Instalar Dependências**:
    ```bash
    pip install python-telegram-bot python-dotenv requests httpx
    ```

4.  **Configurar Variáveis de Ambiente**:
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis, usando as informações que você obteve do Telegram:

    ```dotenv
    # URL base da API de vagas (a paginação será adicionada dinamicamente)
    URL_API="https://querovagastech.com.br/api/jobs?pageSize=20&sort=postedAt%3Adesc"

    # Token de acesso do seu bot Telegram obtido com @BotFather
    TOKEN_BOT="SEU_TOKEN_DO_BOT_AQUI"

    # ID do chat (canal ou grupo) onde as notificações serão enviadas
    CHAT_ID="-1001234567890" # Exemplo de CHAT_ID de canal privado
    ```
    *   Certifique-se de que os valores de `TOKEN_BOT` e `CHAT_ID` sejam os corretos que você obteve.

### Executando a Aplicação

1.  **Rodar o script principal**:
    ```bash
    python main.py
    ```
    A aplicação iniciará um loop contínuo, buscando novas vagas a cada 4 horas e notificando o canal do Telegram configurado. O bot também responderá ao comando `/start` se você enviar para ele diretamente.

## Estrutura do Projeto

*   **`bot/`**: Contém a lógica do bot do Telegram, incluindo a criação do bot, o handler `/start` e a função `send_job_notifications` para enviar mensagens formatadas.
*   **`crawler/`**: Contém a lógica para buscar e filtrar vagas da API externa (`search.py`). Inclui a busca paginada e a filtragem por palavras-chave, senioridade, localização e modo de trabalho.
*   **`database/`**: Gerencia a conexão com o banco de dados SQLite e as operações de salvar/verificar vagas.
    *   `db.py`: Configuração inicial do banco de dados e criação da tabela `jobs`.
    *   `jobs.db`: O banco de dados em si (será criado se não existir).
    *   `jobs.py`: Funções para interagir com a tabela de vagas (salvar, verificar existência).
*   **`model/`**: Define os modelos de dados.
    *   `job.py`: Classe `Job` para representar uma vaga, incluindo `work_mode`.
    *   `mapper.py`: Mapeia dicionários de vagas da API para objetos `Job` e gerencia a lógica de salvar apenas vagas novas no banco de dados. Retorna as vagas que foram efetivamente salvas para notificação.
*   **`main.py`**: O ponto de entrada principal da aplicação. Ele orquestra todas as outras partes: carrega o `.env`, busca e filtra vagas, salva novas vagas e envia notificações via Telegram em um loop periódico.
*   **`.env`**: Arquivo para armazenar variáveis de ambiente (tokens, URLs, IDs). **Importante:** Adicione este arquivo ao seu `.gitignore` para evitar expor suas credenciais.
*   **`.gitignore`**: Define quais arquivos e pastas devem ser ignorados pelo Git (ex: `.env`, `venv`, `__pycache__`, `jobs.db`, `repomix-output.xml`).

## Colaborando no Projeto

Se você tem interesse em contribuir para o projeto, seja bem-vindo! Abaixo estão as diretrizes para colaboração.

### Como Contribuir

1.  **Fork o Repositório**: Crie seu próprio fork do repositório.
2.  **Clone o seu Fork**: Clone o seu fork para sua máquina local.
    ```bash
    git clone https://github.com/seu-usuario/procura-estagio.git
    cd procura-estagio
    ```
    *(Substitua `https://github.com/seu-usuario/procura-estagio.git` pela URL do seu repositório)*
3.  **Crie uma Branch para suas Mudanças**: Mantenha suas alterações isoladas em uma nova branch.
    ```bash
    git checkout -b feature/sua-nova-funcionalidade
    ```
4.  **Faça suas Mudanças**: Implemente suas novas funcionalidades ou correções de bugs.
5.  **Teste Suas Mudanças**: Rode a aplicação localmente com `python main.py` e verifique se as mudanças funcionam como esperado. Se adicionar novas funcionalidades, considere adicionar testes unitários.
6.  **Faça Commit das Suas Mudanças**: Escreva mensagens de commit claras e descritivas.
    ```bash
    git add .
    git commit -m "feat: Adiciona filtragem por senioridade para vagas de estágio"
    ```
7.  **Envie para o Seu Fork**:
    ```bash
    git push origin feature/sua-nova-funcionalidade
    ```
8.  **Abra um Pull Request (PR)**: No GitHub (ou na plataforma onde o repositório estiver hospedado), abra um Pull Request do seu fork (a branch `feature/sua-nova-funcionalidade`) para a branch `main` do repositório principal. Descreva suas alterações detalhadamente no PR.

### Diretrizes de Código

*   **Python 3.10+**: O projeto é desenvolvido em Python 3.10+. Mantenha a compatibilidade e utilize recursos modernos do Python.
*   **Ambiente Virtual e Dependências**: Sempre trabalhe dentro de um ambiente virtual (`venv`). Instale dependências com `pip install -r requirements.txt` após clonar ou criar uma nova branch.
*   **Estilo de Código (PEP 8)**: Mantenha a consistência no estilo de código. Utilize ferramentas como `flake8` para verificar o código e `black` para formatá-lo automaticamente.
*   **Comentários**: Adicione comentários claros para partes complexas do código, para explicar a intenção por trás de decisões específicas ou para documentar o uso de funções/classes complexas.
*   **Mensagens de Commit**: Use um estilo de commit consistente (ex: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)). Isso ajuda a organizar o histórico do projeto e a gerar changelogs automaticamente.

### Reportando Bugs ou Sugerindo Melhorias

Se você encontrar um bug ou tiver uma ideia para uma nova funcionalidade, por favor, abra uma **Issue** no repositório. Descreva o problema ou sugestão o mais detalhadamente possível:
*   Qual o comportamento esperado?
*   Qual o comportamento observado?
*   Passos para reproduzir o erro (se aplicável).
*   Qualquer mensagem de erro relevante.
*   Qualquer sugestão para melhoria.

---

### Próximas Features Sugeridas

Este projeto é um ponto de partida para automatizar a busca de vagas. Existem várias direções que podemos seguir para torná-lo ainda mais poderoso e versátil:

1.  **Web Scraping de Múltiplas Fontes**:
    *   **Ideia**: Expandir a capacidade de busca para além da API atual, utilizando web scraping para coletar vagas de sites populares como:
        *   **LinkedIn**: Principalmente para vagas de estágio e entry-level, utilizando bibliotecas como `linkedin-api` ou técnicas de scraping mais avançadas.
        *   **Indeed**: Similar ao LinkedIn, com uma vasta quantidade de vagas.
        *   **Vagas.com.br, Catho, etc.**: Adaptar o scraper para extrair dados desses portais.
    *   **Desafio**: Web scraping pode ser complexo devido a mudanças frequentes nos layouts dos sites, medidas anti-scraping e a necessidade de respeitar os termos de serviço. Cada site exigirá uma abordagem customizada.

2.  **Melhoria na Filtragem e Interação via Comandos do Bot**:
    *   **Ideia**: Permitir que o usuário configure suas preferências de busca diretamente através de comandos no Telegram, como:
        *   `/set_keywords <palavras>`: Para definir termos de busca para o título.
        *   `/set_location <local>`: Para definir a localização desejada (ex: "Salvador - BA", "Remoto").
        *   `/set_seniority <nível>`: Para definir o nível de senioridade (ex: "estágio", "júnior").
        *   `/set_filters`: Para gerenciar todas as preferências de uma vez.
        *   `/clear_filters`: Para resetar as preferências.
    *   **Armazenamento**: As preferências poderiam ser salvas em um banco de dados ou arquivo de configuração para persistência.
    *   **Benefício**: Torna o bot mais interativo e personalizável sem a necessidade de editar o código.

3.  **Interface de Configuração Mais Amigável**:
    *   **Interface Web/API**: Desenvolver uma interface web simples ou uma API para gerenciar as configurações do bot, monitorar a atividade e visualizar as vagas.

4.  **Otimização de Desempenho e Escalabilidade**:
    *   **Agendamento mais robusto**: Utilizar ferramentas como `APScheduler` ou recursos de agendamento de plataformas de nuvem para gerenciar a execução periódica, garantindo que não haja perda de dados ou falhas.
    *   **Banco de Dados mais robusto**: Para um volume muito grande de vagas ou de usuários, considerar migrar de SQLite para um banco de dados mais escalável como PostgreSQL ou MySQL.
    *   **Gerenciamento de Múltiplos Bots/Canais**: Adaptar o código para que um único bot possa gerenciar notificações para diferentes usuários ou canais com preferências distintas.

5.  **Testes Automatizados**:
    *   Implementar uma suíte de testes unitários e de integração para garantir a qualidade do código e facilitar futuras modificações.

---

Lembre-se de substituir `seu-usuario` e `procura-estagio` pelos seus dados reais do GitHub ao clonar o repositório.
