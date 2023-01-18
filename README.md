# Pipeline de produção de solução de ML end-to-end

O atual projeto busca produzir uma aplicação web baseada em modelos atualizaveis mensalmente de demanda de produtos. Até o momento, foram desenvolvidas diversas atividades sendo a principal dela a construção de um pipeline end-to-end da aplicação. As etapas do pipeline até aqui construidas podem ser resumidas em: programação de todas as etapas em **airflow**, elaboração das mudanças iniciais do processo de **ELT** de banco de dados **Postgres**, preparação rudimental dos dados, treinamento de modelo linear simples com **scikit-learn**, e planejamento da serialização dos modelos em **pickle**. Todo o projeto foi desenvolvido pensando em sua reprodutibilidade. Para isso, está armazenado em containers **docker**.

## Como iniciar o ambiente:

Primeiramente, será necessário realizar a conecção dos dados do arquivo .zip com um banco de dados Postgres. A etapa de conecção pode ser realizada baseando-se no seguinte video: https://www.youtube.com/watch?v=Hhbiup59NYE.

Após o set up da conecção com o banco de dados Postgres. Você pode inicializar o projeto facilmente. Basta inicializar o **docker** com a expressão `docker-compose up`.
