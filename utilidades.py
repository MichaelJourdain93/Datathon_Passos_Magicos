import pandas as pd
def forecast_performance(data, model):
    return model.predict(data)[0]