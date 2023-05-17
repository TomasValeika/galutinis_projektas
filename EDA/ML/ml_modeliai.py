import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import r2_score
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor

# Importuojame galutini DF
from final_df import final_df

visi_auto = final_df()

# Paruosiame duomenis ML
# Dummy kategorijoms
visi_auto = pd.get_dummies(
    data=visi_auto,
    columns=["gamintojas", "modelis", "pavaru_deze", "kuras"],
    dtype=float,
)

# Normalizuojame duomenis
# visi_auto.iloc[:, 1:4] = MinMaxScaler().fit_transform(visi_auto.iloc[:, 1:4])

# Suskaidome i train ir test dalis
X = visi_auto.drop(["kaina"], axis=1)
Y = visi_auto["kaina"]
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, train_size=0.7, test_size=0.3, random_state=42
)

# ML modeliavimas

# Linear model
lm = linear_model.LinearRegression()
lm.fit(X_train, y_train)
y_pred = lm.predict(X_test)

lm_rezultatas = r2_score(y_true=y_test, y_pred=y_pred)

print(f"Linear model rezultatas {lm_rezultatas}")

# CatBoost
cb_model = CatBoostRegressor(iterations=5000, learning_rate=0.03)
cb_model = cb_model.fit(
    X_train,
    y_train,
    eval_set=(X_test, y_test),
)
cb_rezultatas = cb_model.score(X, Y)

print(f"CatBoost rezultatas {cb_rezultatas}")

cb_model.save_model("catboost_model.cbm")

# RandomForest
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

rf_rezultatas = r2_score(y_true=y_test, y_pred=y_pred)

print(f"RandomForest rezultatas {rf_rezultatas}")
