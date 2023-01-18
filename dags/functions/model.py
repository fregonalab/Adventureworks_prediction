import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import ElasticNet
from functions.metrica import get_scores
import joblib
import os

def data_preparation():
    #Upload dos dados
    df = pd.read_csv('dags/data/orders.csv', index_col=0)
    #Transformando datas em dados datetime
    df['modifieddate'] = pd.to_datetime(df['modifieddate'], format='%Y-%m-%d %H:%M:%S')
    df['date_month'] = df['modifieddate'].dt.strftime('%Y-%m')
    #Selecionando apenas um produto para prever a sua demanda
    df = df.groupby(by=['date_month', 'productid']).agg({"orderqty": "sum", "unitprice": "mean"}).reset_index()
    #Calculando o total de vendas mensal do produto
    df['total_sales'] = df.orderqty*df.unitprice
    #Separando a variável 'date_month' em duas variáveis
    df[['year', 'month']] = df['date_month'].str.split('-', 1, expand=True)
    #Dropando colunas desnecessários para as próximas etapas do projeto
    df = df.drop(["orderqty", "unitprice", "date_month"], axis = 1)
    #Produzir arquivo .csv final para utilização do modelo
    df.to_csv('dags/data/products_demand.csv')

def model_707():

    #Upload dos dados
    df = pd.read_csv('dags/data/products_demand.csv', index_col=0)

    #Prevendo a demanda do produto 771
    df_707 = df[df['productid']==707]

    #Separando target
    X = df_707.drop(['total_sales'], axis = 1)
    y = df_707['total_sales']

    #Separando em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Pipeline para transformação de variáveis numéricas
    categorical_features = ['year', 'month']
    categorical_transformer = Pipeline(
        steps=[('onehotencoding', OneHotEncoder(handle_unknown = "ignore", sparse=False)), ('scaler', StandardScaler())]
    )

    # Pipeline de pré-processamento geral das variáveis (numéricas e categóricas)
    preprocessor = ColumnTransformer(
        transformers=[('cat', categorical_transformer, categorical_features)],
        remainder = 'passthrough'
    )

    #Pipeline do pré-procesammento e treinamento do modelo
    model_pipeline = Pipeline(
    steps=[('preprocessor', preprocessor), 
            ('regressor', ElasticNet())]
    )

    #Grade de parâmetros para consulta
    params_grid = {
        "regressor__alpha":[0.001, 0.01, 0.1, 1, 10, 100],
        "regressor__l1_ratio": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    }

    # Instanciar grid search e treinar modelo com 10 k-folds
    grid_search = GridSearchCV(model_pipeline, param_grid=params_grid, cv=10, scoring='neg_median_absolute_error')
    grid_search.fit(X_train, y_train)

    #Seleção do melhor modelo
    model_pipeline = grid_search.best_estimator_

    # Log dos parâmetros do modelo final
    model_params = model_pipeline.named_steps['regressor'].get_params()

    # Calcular métricas para dados de treino e de teste com modelo final
    y_pred_train = model_pipeline.predict(X_train)
    y_pred_test = model_pipeline.predict(X_test)

    # Criar pasta para salvar as metricas
    os.makedirs('dags/metrics', exist_ok=True)

    # Salvar métricas em um dataframe
    df_metrics = pd.DataFrame([
        get_scores(y_train, y_pred_train),
        get_scores(y_test, y_pred_test)
    ], index=['train','test']).rename_axis('input_data')

    # Log das métricas como csv e html
    df_metrics.to_csv('dags/metrics/product_707.csv')

    # Criar pasta para salvar os plots
    os.makedirs('dags/models', exist_ok=True)

    # Serialização do modelo
    joblib.dump(model_pipeline, filename = 'dags/models/product_707.pkl')
    
