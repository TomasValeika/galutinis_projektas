import pandas as pd
import numpy as np


def autobonus_def(df: pd.DataFrame) -> pd.DataFrame:
    # Istriname nereikalingus stulpelius
    df = df.drop(["url", "kliento_tipas", "telefonas", "vin"], axis=1)

    # Kaina. Panaikiname nereikalingus tarpus ir EUR simboli
    df["kaina"] = df["kaina"].str.replace(" ", "").str.replace("€", "")

    # Modelis. Jei nera tokias eilutes eliminuojame
    df = df.loc[df["modelis"].notna()]

    # Pagamimimo data. Paliekame tik metus
    df["pagaminimo_data"] = df["pagaminimo_data"].str[:4].astype(int)

    # Rida. Istriname tarpus ir eliminuojame gale esanti 'km'
    df["rida"] = df["rida"].str.replace(" ", "").str.replace("km", "")

    # Kuras. Jei nera reiksmes tokias eilutes eliminuojame
    df = df.loc[df["kuras"].notna()]

    # Vairo padetis. Palikeame tik su reiksme 'Kairėje'
    df = df.loc[df["vairo_padetis"] == "Kairėje"]

    # Bukle. Paliekame tik tas eilutes kuriose nėra reikšmės. Eilutes be reiksmes yra automobilis be defektu.
    df = df.loc[df["bukle"].isna()]

    # Variklis. Stulpeli padaliname i dvi dalis ir paliekame tik skaitines reiksmes
    # Pirma dalis - galia_kw
    # Antra dalis - galia_ag
    df[["variklis1", "galia_kw"]] = df["variklis"].str.split("(", expand=True)
    df["galia_kw"] = (
        df["galia_kw"].str.replace(" ", "").str.replace("kW)", "", regex=False)
    )

    # Istriname nereikalingus stulpelius
    df = df.drop(
        [
            "variklis",
            "vairo_padetis",
            "varantys_ratai",
            "vairo_padetis",
            "bukle",
            "variklis1",
        ],
        axis=1,
    )

    df = df.reset_index(drop=True)

    df = df.rename(
        columns={
            "marke": "gamintojas",
            "pagaminimo_data": "metai",
            "kebulo_tipas": "kebulas",
        }
    )

    return df
