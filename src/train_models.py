import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def train_linear_model(df):
    print("Entrenando modelo de Regresión Lineal...")

    # Separar los datos train y test
    train_df = df[df['temporada'] < 2025]
    test_df = df[df['temporada'] == 2025]

    # Variables de entrada y salida
    features = ["carreras_corridas", "promedio_pos_final", "podios", "abandonos", "es_rookie"]
    target = "puntos_totales"

    # Datos de entrenamiento y prueba
    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]

    # Entrenar el modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    print(f"MAE promedio: (CrossVal): {-scores.mean():.2f}")

    # Predicción en pilotos 2025
    y_pred = model.predict(X_test)

    # Evaluación (si hay valores reales para comparar)
    print("\n Evaluación del modelo en temporada 2025:")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
    print(f"R²:   {r2_score(y_test, y_pred):.2f}")

    # Mostrar predicciones ordenadas
    test_df = test_df.copy()
    test_df["puntos_predichos"] = y_pred
    print("\n Predicción de puntos para pilotos 2025:")
    print(test_df[["piloto", "constructor", "puntos_totales", "puntos_predichos"]].sort_values("puntos_predichos", ascending=False))

    return model