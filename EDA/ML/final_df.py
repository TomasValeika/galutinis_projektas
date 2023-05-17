import pandas as pd
import numpy as np
from scipy import stats
import os


# Importuojame funkcijas
from .autobilis import autobilis_def
from .autobonus import autobonus_def
from .automobilis import automobilis_def
from .autogidas import autogidas_def
from .automobilis_final_df import auto_final_df


def final_df():
    # Autobilis
    autobilis_df = pd.read_csv(os.path.join(os.getcwd() + r"\EDA\csv\autobilis.csv"))
    autobilis = autobilis_def(autobilis_df)

    # Autobonus
    autobonus_df = pd.read_csv(os.path.join(os.getcwd() + r"\EDA\csv\autobonus.csv"))
    autobonus = autobonus_def(autobonus_df)

    # Automobilis
    automobilis_df1 = pd.read_csv(
        os.path.join(os.getcwd() + r"\EDA\csv\automobilis.csv")
    )
    automobilis_df2 = pd.read_csv(
        os.path.join(os.getcwd() + r"\EDA\csv\automobilis2.csv")
    )
    automobilis = automobilis_def(automobilis_df1, automobilis_df2)

    # Autogidas
    autogidas_df = pd.read_csv(os.path.join(os.getcwd() + r"\EDA\csv\autogidas.csv"))
    autogidas = autogidas_def(autogidas_df)

    # Suformuojame final DF

    visi_auto = auto_final_df(autobilis, autobonus, automobilis, autogidas)

    # ### Papildoma duomenu korekcija

    # Jei yra str reiksme ja pakeisti i 0
    visi_auto["kaina"] = np.where(
        (visi_auto["kaina"] == "Sutartinė"), 0, visi_auto["kaina"]
    )

    # Kaina stulpeli konvertuojame i int
    visi_auto["kaina"] = visi_auto["kaina"].astype(int)
    visi_auto["galia_kw"] = visi_auto["galia_kw"].astype(int)
    visi_auto["rida"] = visi_auto["rida"].astype(int)

    # Jei rida yra minusine, panaikiname tokias eilutes
    visi_auto = visi_auto.loc[visi_auto["rida"] > 1]

    # Jei nuokrypis yra daugiau nei 3, tokias eilutes panaikiname

    visi_auto = visi_auto[stats.zscore(visi_auto["kaina"]) < 3]
    visi_auto = visi_auto[stats.zscore(visi_auto["galia_kw"]) < 3]
    visi_auto = visi_auto[stats.zscore(visi_auto["rida"]) < 3]

    return visi_auto
