# OS Generator - Sistema de Gestão de Ordens de Serviço

---

## Sobre o Projeto

O **OS Generator** é uma aplicação web desenvolvida em Django para facilitar o gerenciamento de ordens de serviço em assistências técnicas, com foco em lojas de conserto de celulares. O sistema oferece as seguintes funcionalidades principais:

- Cadastro e gerenciamento de clientes e ordens de serviço.
- Fluxo personalizado para ordens com checklists e geração de documentos PDF.
- Dashboard responsivo com métricas financeiras (total ganho, a receber, ordens em andamento, ticket médio).
- Filtros avançados para pesquisa dinâmica das ordens.
- Gráficos interativos mostrando evolução mensal das ordens e faturamento.
- Interface moderna com menu lateral, totalmente responsivo e com código CSS3 puro.
- Sistema de autenticação e gerenciamento de usuários com senhas seguras.
- Configuração via variáveis de ambiente para facilitar deploy em ambientes locais e nuvem.
- Dockerização completa com Postgres como banco de dados para facilitar implantação em nuvem.

---

## Tecnologias Usadas

- Python 3.11, Django 4.x
- PostgreSQL 16
- Gunicorn para servidor WSGI em produção
- Docker e Docker Compose para containerização
- Bootstrap 5 (CDN) e CSS3 puro para estilos responsivos
- Chart.js para renderização dos gráficos no dashboard
- Python-dotenv para gestão de variáveis de ambiente

---

## Estrutura do Projeto

- `core/` – Contém o módulo principal Django, com `settings.py`, `wsgi.py`, e a configuração principal.
- `orders/` – App Django responsável pelo gerenciamento das ordens de serviço.
- `person/` – App contendo modelos relacionados a clientes e endereços.
- `static/css/style.css` – Estilos CSS3 personalizados do sistema.
- `static/js/dashboard.js` – JavaScript para controle da UI e gráficos.
- `Dockerfile` – Script para criação da imagem Docker do projeto.
- `docker-compose.yml` – Define os serviços da aplicação e banco de dados.
- `.env` – Arquivo de variáveis de ambiente (deve estar na raiz do projeto; **não deve ser versionado.**)

---

## Como Executar o Projeto pela Primeira Vez

### Pré-Requisitos

- Docker e Docker Compose instalados na sua máquina.
- Git para clonar o repositório (opcional).

### Passo a Passo

1. **Clone o repositório**

# OS Generator - Sistema de Gestão de Ordens de Serviço

---

## Sobre o Projeto

O **OS Generator** é uma aplicação web desenvolvida em Django para facilitar o gerenciamento de ordens de serviço em assistências técnicas, com foco em lojas de conserto de celulares. O sistema oferece as seguintes funcionalidades principais:

- Cadastro e gerenciamento de clientes e ordens de serviço.
- Fluxo personalizado para ordens com checklists e geração de documentos PDF.
- Dashboard responsivo com métricas financeiras (total ganho, a receber, ordens em andamento, ticket médio).
- Filtros avançados para pesquisa dinâmica das ordens.
- Gráficos interativos mostrando evolução mensal das ordens e faturamento.
- Interface moderna com menu lateral, totalmente responsivo e com código CSS3 puro.
- Sistema de autenticação e gerenciamento de usuários com senhas seguras.
- Configuração via variáveis de ambiente para facilitar deploy em ambientes locais e nuvem.
- Dockerização completa com Postgres como banco de dados para facilitar implantação em nuvem.

---

## Tecnologias Usadas

- Python 3.11, Django 4.x
- PostgreSQL 16
- Gunicorn para servidor WSGI em produção
- Docker e Docker Compose para containerização
- Bootstrap 5 (CDN) e CSS3 puro para estilos responsivos
- Chart.js para renderização dos gráficos no dashboard
- Python-dotenv para gestão de variáveis de ambiente

---

## Estrutura do Projeto

- `core/` – Contém o módulo principal Django, com `settings.py`, `wsgi.py`, e a configuração principal.
- `orders/` – App Django responsável pelo gerenciamento das ordens de serviço.
- `person/` – App contendo modelos relacionados a clientes e endereços.
- `static/css/style.css` – Estilos CSS3 personalizados do sistema.
- `static/js/dashboard.js` – JavaScript para controle da UI e gráficos.
- `Dockerfile` – Script para criação da imagem Docker do projeto.
- `docker-compose.yml` – Define os serviços da aplicação e banco de dados.
- `.env` – Arquivo de variáveis de ambiente (deve estar na raiz do projeto; **não deve ser versionado.**)

---

## Como Executar o Projeto pela Primeira Vez

### Pré-Requisitos

- Docker e Docker Compose instalados na sua máquina.
- Git para clonar o repositório (opcional).

### Passo a Passo

1. **Clone o repositório**

git clone <url_do_seu_repositorio>
cd os_generator


2. **Crie ou confirme o arquivo `.env` na raiz do projeto**

Seu `.env` deve conter as variáveis essenciais estão no env-example:


> **Importante:** Nunca versionar seu `.env` com segredos reais. Mantenha-o localmente e seguro.

3. **Construa as imagens Docker**

docker-compose build


4. **Suba os containers**

docker-compose up -d


5. **Execute migrações para criar as tabelas no banco**

docker-compose exec os_generator_web python manage.py migrate


6. **Crie um superusuário Django para acessar o admin**

docker-compose exec os_generator_web python manage.py createsuperuser


> Siga as instruções para definir usuário e senha.

7. **Acesse a aplicação**

- Dashboard: [http://localhost:8000/](http://localhost:8000/)
- Admin Django: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Observações Importantes

- Para conseguir rodar seu container web com sucesso, as variáveis do `.env` devem estar configuradas corretamente, sobretudo as configurações do banco Postgres.
- O volume do banco pode ser removido manualmente se precisar reinicializar o banco, com:

docker-compose down