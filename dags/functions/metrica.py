from sklearn import metrics

def get_scores(y_true, y_pred):
    """
    - Função: 
        Calcular múltiplas métricas para modelos de regressão
    - Argumentos:
        y_true(pd.Series): target do conjunto de teste
        y_pred(output sklearn model): target inferidas pelo modelo
    """
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)
    
    score_dict = {
        'MAE': mae,
        'MSE': mse,
        'R2': r2,
    }

    return score_dict