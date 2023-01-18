# Pipeline de produção de solução de ML end-to-end

O atual projeto busca produzir uma aplicação web baseada em modelos atualizaveis mensalmente de demanda de produtos. Até o momento, foram desenvolvidas diversas atividades sendo a principal dela a construção de um pipeline end-to-end da aplicação. As etapas do pipeline até aqui construidas podem ser resumidas em: programação de todas as etapas em **airflow**, elaboração das mudanças iniciais do processo de **ELT** de banco de dados **Postgres**, preparação rudimental dos dados, treinamento de modelo linear simples com **scikit-learn**, e planejamento da serialização dos modelos em **pickle**. Todo o projeto foi desenvolvido pensando em sua reprodutibilidade. Para isso, está armazenado em containers **docker**.

## Como iniciar o ambiente:

Você pode inicializar o projeto facilmente. Basta clonar o repositório, e usar o **Docker** com `docker-compose up`.
