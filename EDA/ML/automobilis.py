import pandas as pd
import numpy as np


def automobilis_def(df1, df2) -> pd.DataFrame:
    # Sujungiame DF ir istriname dublikatus
    df = pd.concat([df1, df2]).drop_duplicates()

    # Istriname nereikalingus stulpelius
    df = df.drop(["url", "vardas", "telefonas"], axis=1)

    # Kaina. Paliekame tik skaities reiksmes
    df["kaina"] = df["kaina"].str.replace("Kaina: ", "")
    df["kaina"] = df["kaina"].str.replace(" EUR", "")
    df["kaina"] = df["kaina"].str.replace(" ", "").astype(int)

    # Metai. Paliekame tik metus
    df["metai"] = df["metai"].str[:4].astype(int)

    # Bukle. Paliekame tik tas eilutes kuriose nera iraso. Be iraso automobilis be trukumu
    df = df.loc[df["bukle"].isna()]

    # Galia. Padaliname stulpeli i dvi dalis. Isvalome duomenis, paliekame tik skaitines reiksmes.
    # Pirma dalis - galia_kw
    # Antra dalis - galia_ag
    df[["galia_kw", "galia_ag"]] = df["galia"].str.split("(", expand=True)

    df["galia_kw"] = df["galia_kw"].str.replace(" KW", "")
    df["galia_ag"] = df["galia_ag"].str.replace(" AG)", "", regex=False)

    # Rida. Paliekame tik skaitines reiksmes.
    df["rida"] = df["rida"].str.replace(" km", "")

    # Pavaru deze. Standartizuojame pavadinimus, kad butu tik Mechanine ir Automatine
    df["pavaru_deze"] = np.where(
        (df["pavaru_deze"] == "Pusiau automatinė"),
        "Automatinė",
        df["pavaru_deze"],
    )

    # Vairo padetis. Paliekame tik tas reiksmes kur yra Kairėje
    df = df.loc[df["vairo_padetis"] == "Kairėje"]

    # Darbinis turis. Daliname stulpeli i dvi dalis. Paliekame tik skaitines reiksmes.
    # Pirma dalis - variklio_turis_ltr
    # Antra dalis - variklio_turis_cm3
    df[["variklio_turis_ltr", "variklio_turis_cm3"]] = df["darbinis_turis"].str.split(
        "(", expand=True
    )

    df["variklio_turis_ltr"] = df["variklio_turis_ltr"].str.replace(
        " litr.", "", regex=False
    )
    df["variklio_turis_cm3"] = df["variklio_turis_cm3"].str.replace(
        " cm³)", "", regex=False
    )

    # Pavadinimas. Pavadinimas stulpeli padaliname i gamintojas ir modelis
    df[["pavadinimas1", "pavadinimas2"]] = df["pavadinimas"].str.split(
        " m.,", expand=True
    )
    df["pavadinimas1"] = df["pavadinimas1"].str[:-5]

    # I atskirus stulpelius isdaliname pavadinima
    df["gamintojas"] = df["pavadinimas1"].str.split().str.get(0)
    df["modelis"] = df["pavadinimas1"].str.split().str.get(1)
    df["modelis2"] = df["pavadinimas1"].str.split().str.get(2)

    # Apjungeme modelio pavadinima
    df["modelis_final"] = df["modelis"] + df["modelis2"]

    df["modelis_final2"] = np.where(
        (df["modelis_final"].isna()),
        df["modelis"],
        df["modelis_final"],
    )

    # Istriname nereikalingus stulpelius
    df = df.drop(
        [
            "darbinis_turis",
            "galia",
            "bukle",
            "pavadinimas2",
            "pavadinimas",
            "vairo_padetis",
            "pavadinimas1",
            "modelis",
            "modelis2",
            "modelis_final",
            "variklio_turis_cm3",
        ],
        axis=1,
    )

    df = df.reset_index(drop=True)

    df = df.rename(
        columns={
            "kebulo_tipas": "kebulas",
            "variklio_turis_ltr": "variklio_turis",
            "modelis_final2": "modelis",
        }
    )

    return df
