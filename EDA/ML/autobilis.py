import pandas as pd
import numpy as np


def autobilis_def(df: pd.DataFrame) -> pd.DataFrame:
    # Istriname stulpelius kurių nenaudosime tolimesniuose skaiciavimuose
    df = df.drop(
        ["url", "id", "vardas", "miestas", "title", "pardavejas", "telefonas", "vin"],
        axis=1,
    )

    # Kainos stulpelis
    df["kaina"] = df["kaina"].str.replace(" ", "").str.replace("€", "").astype(int)

    # Pagaminimo data. Eliminuojame \n
    df["pagaminimo_data"] = df["pagaminimo_data"].replace(r"\n", "", regex=True)

    # Eliminuojame jei nera iraso
    df = df[df["pagaminimo_data"].notna()]

    # Imame pirmus 4 simbolius
    df["pagaminimo_data"] = df["pagaminimo_data"].str[:4].astype(int)

    # Bukle. Nei reiksme yra nan pakeiciame i 'Be defektų'.
    # Paliekame tik tas eilutes kuriose yrašas 'Be defektų'
    df["bukle"] = np.where((df["bukle"].isna()), "Be defektų", df["bukle"])

    df = df.loc[df["bukle"] == "Be defektų"]

    # Vairo padėtis. Jei nėra įrašo pakeičiame į 'Kairėje'.
    # Visus įrašus kur yra 'Desineje' eliminuojame

    df["vairo_padetis"] = np.where(
        (df["vairo_padetis"].isna()), "Kairėje", df["vairo_padetis"]
    )

    df = df.loc[df["vairo_padetis"] == "Kairėje"]

    # Modelis. Jei nera reiksmes tokias eilutes eliminuoti
    df = df.loc[df["modelis"].notna()]

    # Galia stulpeli padaliname i dvi dalis ir paliekame tik skaitines reiksmes
    # Pirma dalis - galia_kw
    # Antra dalis - galia_ag
    df[["galia_kw", "galia_ag"]] = df["galia"].str.split("(", expand=True)

    df["galia_kw"] = df["galia_kw"].str.replace(" kW", "")
    df["galia_ag"] = df["galia_ag"].str.replace(" AG)", "", regex=False)

    # Rida. Paliekame tik skaitines reiksmes.
    df["rida"] = df["rida"].str.replace(r"\n", "", regex=True)
    df["rida"] = df["rida"].str.replace(" ", "").str.replace("km", "")

    # Istriname nereikalingus stulpelius
    df = df.drop(["galia", "vairo_padetis", "bukle", "varantieji_ratai"], axis=1)

    df = df.reset_index(drop=True)

    df = df.rename(
        columns={
            "marke": "gamintojas",
            "pagaminimo_data": "metai",
            "darbinis_turis": "variklio_turis",
            "duru_skaicius": "duru_sk",
        }
    )

    return df
