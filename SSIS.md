---
aliases:
  - SQL Server Integration Services (SSIS)
tags:
  - automation
  - database
---
## Para que serve

- **ETL (Extração, Transformação e Carga):** Extrai dados de diversas origines (SQL Server, Oracle, MySQL, arquivos Excel, CSV, etc.), limpa, reorganiza ou aplica regras de negócio neles, e os carrega em um banco de dados ou _Data Warehouse_.
- **Automação de Tarefas:** Executa comandos SQL, gerencia arquivos via FTP/sistema de arquivos, envia e-mails e realiza manutenção de banco de dados.

## Principais Componentes

- **Control Flow (Fluxo de Controle):** O "cérebro" do pacote SSIS. Define a ordem lógica das tarefas, executando _tasks_ e _containers_.
- **Data Flow (Fluxo de Dados):** O pipeline responsável por mover e transformar os dados propriamente ditos, dividido em _Sources_ (Origens), _Transformations_ (Transformações) e _Destinations_ (Destinos).
- **Connection Managers (Gerenciadores de Conexões):** Configuram as pontes de acesso aos bancos de dados e arquivos externos.
- **SSISDB:** O catálogo centralizado no SQL Server para gerenciar, armazenar e monitorar a execução de pacotes. 

## Como é desenvolvido

Os projetos de SSIS são criados no **Visual Studio** utilizando a extensão de projetos do Integration Services (SSDT) e, após prontos, podem ser publicados no SQL Server para agendamento via _SQL Server Agent_.
