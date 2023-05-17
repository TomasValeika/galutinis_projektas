import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import streamlit as st
from PIL import Image

from EDA.ML.final_df import final_df


image = Image.open("bmw.png")

st.image(image)

st.header("Pasirinkite automobilio specifikaciją")

# Importuojame duomenis
visi_auto = final_df()

# Streamlit pasirinkimas
gamintojas = st.selectbox("Gamintojas", visi_auto["gamintojas"].unique())

modelis = st.selectbox(
    "Modelis",
    visi_auto.loc[visi_auto["gamintojas"] == gamintojas]["modelis"].unique(),
)

pavaru_deze = st.selectbox(
    "Pavarų dežė",
    visi_auto.loc[visi_auto["modelis"] == modelis]["pavaru_deze"].unique(),
)

kuras = st.selectbox(
    "Kuras", visi_auto.loc[visi_auto["modelis"] == modelis]["kuras"].unique()
)

galia = st.selectbox(
    "Galia kW",
    visi_auto.loc[
        (visi_auto["modelis"] == modelis)
        & (visi_auto["kuras"] == kuras)
        & (visi_auto["pavaru_deze"] == pavaru_deze)
    ]["galia_kw"].unique(),
)

amzius = st.selectbox(
    "Amžius",
    visi_auto.loc[visi_auto["modelis"] == modelis]["amzius"].sort_values().unique(),
)

rida = st.selectbox("Rida", visi_auto["rida"].sort_values().unique())

data = {
    "gamintojas": gamintojas,
    "modelis": modelis,
    "pavaru_deze": pavaru_deze,
    "kuras": kuras,
    "galia_kw": galia,
    "rida": rida,
    "amzius": amzius,
}

# Suformuojame DF
df_vartotojo = pd.DataFrame(data, index=[0])


# Padarome dummy kategorijas
df_vartotojo = pd.get_dummies(
    data=df_vartotojo,
    columns=["gamintojas", "modelis", "pavaru_deze", "kuras"],
    dtype=float,
)

model = CatBoostRegressor()
model.load_model("catboost_model.cbm")


def duomenu_uzpildymas(data):
    # Sukuriame DF is modelio stulpeliu
    column_names = pd.DataFrame(columns=model.feature_names_)

    # Jei is paduoto DF nera tokios reiksmes graziname 0
    for col in column_names:
        if col not in data:
            data[col] = 0

    return data


kainu_spejimas = duomenu_uzpildymas(df_vartotojo)

final = model.predict(kainu_spejimas)

st.write("Planuojama kaina EUR")

st.dataframe(data=final.round())
