import pandas as pd
import numpy as np


def autogidas_def(df) -> pd.DataFrame:
    # Sutvarkome kainu stulpeli, nuimame Eur simboli
    df["kaina"] = df["kaina"].str[:-1]
    df["kaina"] = df["kaina"].str.replace(" ", "").astype(int)

    # Marke stulpelyje istriname gale esanty tarpa
    df["marke"] = df["marke"].str.replace(" ", "")

    # Modelis nutriname gale tuscia tarpa
    df["modelis"] = df["modelis"].str[:-1]

    # Paliekame tik metus, menesi pasaliname
    df["metai"] = df["metai"].str[:4]

    # Kuras pasaliname gale esanti tarpa
    df["kuras"] = df["kuras"].str[:-1]

    # Standartizuojame kuro tipus
    df["kuras_kor"] = np.where(
        (df["kuras"] == "Benzinas/Gamtinės dujos"),
        "Benzinas/Dujos",
        np.where(
            (df["kuras"] == "Benzinas / Elektra"),
            "Benzinas/Elektra",
            np.where(
                (df["kuras"] == "Benzinas + Elektra"),
                "Benzinas/Elektra",
                np.where(
                    (df["kuras"] == "Benzinas + Dujos (LPG)"),
                    "Benzinas/Dujos",
                    np.where(
                        (df["kuras"] == "Dyzelinas + Elektra"),
                        "Dyzelinas/Elektra",
                        np.where(
                            (df["kuras"] == "Etanolis"),
                            "Dujos",
                            np.where(
                                (df["kuras"] == "Benzinas / Bioetanolis E85"),
                                "Benzinas/Dujos",
                                df["kuras"],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    # Pavaru deze istrinti nereikalingus tapus
    df["pavaru_deze"] = df["pavaru_deze"].str.replace(" ", "")

    # Duru skaicius, panaikiname nereikalingus tarpus
    df["duru_sk"] = df["duru_sk"].str.replace(" ", "")

    # Vairo padetis, panaikiname nereikalingus tarpus.
    df["vairo_padetis"] = df["vairo_padetis"].str.replace(" ", "")

    # Defektai, istriname nereikalingus tarpus.
    df["defektai"] = df["defektai"].str[:-1]

    # Varantys ratai, panaikiname gale esanti tarpa ir standartizuojame kategorija
    df["varantys_ratai"] = df["varantys_ratai"].str[:-1]

    df["varantys_ratai"] = np.where(
        (df["varantys_ratai"] == "Priekiniai varantys ratai"),
        "Priekiniai",
        np.where(
            (df["varantys_ratai"] == "Galiniai varantys ratai"),
            "Galiniai",
            np.where(
                (df["varantys_ratai"] == "Visi varantys ratai"),
                "Visi",
                np.where(
                    (df["varantys_ratai"] == "Visi varantys (4х4)"),
                    "Visi",
                    df["varantys_ratai"],
                ),
            ),
        ),
    )

    # Rida
    df["rida"] = df["rida"].str.replace(" ", "").str.replace("km", "")

    # Variklio stulpeli padaliname i tris stulpelius variklio)_turis, galia_kw, galia_ag
    df[["variklis1", "galia_ag"]] = df["variklis"].str.split("(", expand=True)
    df["galia_ag"] = df["galia_ag"].str.replace(" Ag)", "", regex=False)

    df[["turis", "galia_kw"]] = df["variklis1"].str.split("l.", expand=True)
    df["galia_kw"] = df["galia_kw"].str.replace(" ", "").str.replace("kW", "")

    # Sukuriame nauja stulpeli paimti kW is turis stulpelio
    df["galia_kw2"] = np.where(
        (df["galia_kw"].isna()),
        df["turis"],
        df["galia_kw"],
    )

    # Turis stulpelis. Jie turis reiksme lygi galia_kW2 pakeisti i nan
    df["turis2"] = np.where(
        (df["turis"] == df["galia_kw2"]),
        np.nan,
        df["turis"],
    )

    df["turis2"] = df["turis2"].str.replace(" ", "")

    df["galia_kw2"] = df["galia_kw2"].str.replace(" ", "").str.replace("kW", "")

    df["galia_kw2"] = np.where((df["galia_kw2"] == ""), np.nan, df["galia_kw2"])

    # Defektai. Triname eilutes kuriose nėra įraso 'Be defektų'
    df = df.loc[df["defektai"] == "Be defektų"]

    # Vairo padetis. Istriname eilutes kuriose nėra įrašo 'Kairėje'
    df = df.loc[df["vairo_padetis"] == "Kairėje"]

    # Modelis. Triname eilutes kur nėra nurodytas modelis
    df = df.loc[df["modelis"].notna()]

    # Duru skaicius. Irasome trukstama reiksme
    df["duru_sk2"] = np.where((df["duru_sk"].isna()), "4/5", df["duru_sk"])

    # Istriname stulpeli duru_sk ir duru_sk2 pervadiname i duru_sk2
    df = df.drop(["duru_sk"], axis=1).rename(columns={"duru_sk2": "duru_sk"})

    # Istriname stulpelius
    df = df.drop(
        [
            "url",
            "skelbimo_id",
            "variklis",
            "variklis1",
            "kuras",
            "telefono_nr",
            "vairo_padetis",
            "defektai",
            "varantys_ratai",
            "turis",
            "galia_kw",
        ],
        axis=1,
    )

    df = df.reset_index(drop=True)

    df = df.rename(
        columns={
            "marke": "gamintojas",
            "kuras_kor": "kuras",
            "galia_kw2": "galia_kw",
            "turis2": "variklio_turis",
        }
    )

    return df
