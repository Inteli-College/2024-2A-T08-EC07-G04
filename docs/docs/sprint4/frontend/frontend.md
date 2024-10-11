# Como Executar

O front-end é uma parte crucial de um sistema de análise de dados desenvolvido especialmente para a Volkswagen, com o objetivo de otimizar e acelerar o processo de análise de grandes volumes de informações referentes a falhas veiculares. Esse dashboard foi concebido para oferecer uma interface amigável, intuitiva e eficiente, que permita aos usuários compreender de maneira rápida e precisa a relação entre o número de veículos com falhas e aqueles sem falhas.

O ponto central da aplicação é a visualização clara desses dados, com gráficos e indicadores de performance que facilitam a identificação de padrões, problemas e tendências. Por meio do dashboard, os usuários podem acessar de forma direta informações detalhadas, possibilitando tomadas de decisão mais rápidas e assertivas, sem a necessidade de navegar por relatórios extensos ou complexos.

Além da funcionalidade de visualização, o sistema conta com uma página específica para o upload de arquivos no formato XLSX. Essa funcionalidade permite que os usuários carreguem novos conjuntos de dados, que são imediatamente processados pelo modelo de análise integrado. Após o upload, o modelo verifica e interpreta as informações, determinando se os dados indicam veículos com falhas ou sem falhas, oferecendo um feedback ágil e eficiente sobre a situação dos veículos analisados.

A interface do front-end está integrada ao backend, ao banco de dados e ao modelo de análise preditiva. Isso significa que as informações exibidas no dashboard estão sempre atualizadas e em sincronia com os dados, proporcionando uma visão fiel do desempenho dos veículos. Além disso, essa integração permite uma comunicação eficiente entre todas as camadas da aplicação, garantindo que os usuários possam acessar dados de forma fluida e consistente. 

## Como Executar o Frontend

Para isso, siga os passos abaixo:

### Pré-requisitos
Certifique-se de que você tenha as seguintes ferramentas instaladas no seu ambiente de desenvolvimento local:

1. **Node.js** (v12 ou superior) – O Node.js é necessário para executar o servidor de desenvolvimento e gerenciar pacotes.
2. **NPM** ou **Yarn** – Gerenciadores de pacotes que permitem instalar as dependências do projeto.
3. **Git** (opcional) – Para clonar o repositório do projeto, caso ele esteja hospedado em um repositório Git.

### Passo a Passo para Executar o Frontend

1. **Clone o repositório (opcional):**
   Se o código estiver disponível em um repositório Git, clone o projeto usando o seguinte comando:
   ```bash
   git clone https://github.com/Inteli-College/2024-2A-T08-EC07-G04
   ```
   Caso contrário, baixe o código-fonte e extraia em uma pasta local.

2. **Instale as dependências do projeto:**
   Navegue até o diretório raiz do projeto no terminal e execute o comando abaixo para instalar todas as dependências necessárias. O comando pode variar dependendo do gerenciador de pacotes que você usa:

   Usando **NPM**:
   ```bash
   npm install
   ```

   Usando **Yarn**:
   ```bash
   yarn install
   ```

3. **Configuração de ambiente (opcional):**
   Se o projeto requer configurações específicas (como uma API URL, chaves de API, ou variáveis de ambiente), verifique se existe um arquivo `.env.example` no projeto. Crie uma cópia desse arquivo e renomeie para `.env`, e ajuste os valores conforme necessário:
   ```bash
   cp .env.example .env
   ```

4. **Execute o servidor de desenvolvimento:**
   Para iniciar o servidor local e visualizar o dashboard, use o seguinte comando:

   Usando **NPM**:
   ```bash
   npm run start
   ```

   Usando **Yarn**:
   ```bash
   yarn start
   ```

   Isso iniciará o servidor de desenvolvimento e abrirá automaticamente o aplicativo no navegador padrão, geralmente acessível em `http://localhost:3000`.

5. **Acesse o Dashboard:**
   Uma vez que o servidor de desenvolvimento estiver rodando, você poderá interagir com o dashboard, visualizar os dados das falhas veiculares e utilizar a funcionalidade de upload de arquivos XLSX para carregar novos dados e atualizar as análises.

### Build para Produção (opcional)

Se você deseja gerar uma versão otimizada do front-end para implantar em produção, use o comando de build:

Usando **NPM**:
```bash
npm run build
```

Usando **Yarn**:
```bash
yarn build
```

Isso irá gerar uma pasta `build` com todos os arquivos necessários para implantação em um servidor de produção.

Seguindo esses passos, o front-end será executado localmente, permitindo que você explore e interaja com o sistema de análise de falhas da Volkswagen.