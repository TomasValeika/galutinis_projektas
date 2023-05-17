import pandas as pd
import numpy as np


def auto_final_df(df1, df2, df3, df4):
    # Apjungiame visus DF
    all_auto = pd.concat([df1, df2, df3, df4], ignore_index=True)

    # Automobiliu pavadinimu tvarkymas
    gamintojas = all_auto.copy()

    # Alfa - Romeo
    gamintojas["gamintojas"] = np.where(
        (gamintojas["gamintojas"] == "Alfa Romeo"),
        "Alfa-Romeo",
        np.where(
            (gamintojas["gamintojas"] == "AlfaRomeo"),
            "Alfa-Romeo",
            gamintojas["gamintojas"],
        ),
    )

    # Land-Rover
    gamintojas["gamintojas"] = np.where(
        (gamintojas["gamintojas"] == "Land Rover"),
        "Land-Rover",
        np.where(
            (gamintojas["gamintojas"] == "LandRover"),
            "Land-Rover",
            gamintojas["gamintojas"],
        ),
    )

    # Mercedes-Benz
    gamintojas["gamintojas"] = np.where(
        (gamintojas["gamintojas"] == "Mercedes Benz"),
        "Mercedes-Benz",
        gamintojas["gamintojas"],
    )

    # Mini
    gamintojas["gamintojas"] = np.where(
        (gamintojas["gamintojas"] == "MINI"), "Mini", gamintojas["gamintojas"]
    )

    # Seat
    gamintojas["gamintojas"] = np.where(
        (gamintojas["gamintojas"] == "SEAT"), "Seat", gamintojas["gamintojas"]
    )

    # SsangYong
    gamintojas["gamintojas"] = np.where(
        (gamintojas["gamintojas"] == "Ssangyong"), "SsangYong", gamintojas["gamintojas"]
    )

    # Istriname dublikatus
    gamintojas = gamintojas.drop_duplicates()

    # Sugrupuojame patikrinti kiek yra kiekvieno galintojo vienetu
    # Jei kiekis mazesnis nei 10 tokius gamintojus istrinti
    gamintoju_kiekis = gamintojas.copy()

    gamintoju_kiekis = (
        gamintoju_kiekis.groupby(["gamintojas"])[["gamintojas"]]
        .count()
        .rename(columns={"gamintojas": "count"})
        .reset_index()
    )
    gamintoju_kiekis = gamintoju_kiekis.sort_values(by="count")

    gamintoju_kiekis = gamintoju_kiekis.loc[gamintoju_kiekis["count"] < 10]

    # Prie gamintojas pridedame gamintoju kiekis ir visus kas sutapo istrinti
    gamintojas = pd.merge(gamintojas, gamintoju_kiekis, how="left", on="gamintojas")

    # Istriname tuos gamintojus kuriu kiekis yra mazesnis uz 10
    gamintojas = gamintojas.loc[gamintojas["count"].isna()].reset_index(drop=True)

    # Modeliu koregavimas
    modelis = gamintojas.copy()

    # Panaikiname tarpus stulpelyje modelis. Didziosios raides
    modelis["modelis"] = modelis["modelis"].str.replace(" ", "")
    modelis["modelis"] = modelis["modelis"].str.replace(r"\t", "", regex=True)
    modelis["modelis"] = modelis["modelis"].str.upper()

    # Istriname jei modelis yra -KITA- arba KITAS
    modelis = modelis.loc[modelis["modelis"] != "-KITA-"]
    modelis = modelis.loc[modelis["modelis"] != "KITAS"]

    # Metai stulpeli konvertuojame i int reiksme
    modelis["metai"] = modelis["metai"].astype(int)

    # Greiciu deze standartizuojame
    modelis["pavaru_deze"] = np.where(
        (modelis["pavaru_deze"] == "Pusiau automatinė"),
        "Automatinė",
        modelis["pavaru_deze"],
    )

    # Jei nera nurodytas pavaru dezes tipas tokias eilutes eliminuojame
    modelis = modelis.loc[modelis["pavaru_deze"].notna()]

    # Jei neturi iraso variklio_turis, pavaru_deze, duru_sk, galia_kw, galia_ag. Jei trinti 0, palikti 1
    modelis["remove"] = np.where(
        (
            (modelis["variklio_turis"].isna())
            & (modelis["pavaru_deze"].isna())
            & (modelis["duru_sk"].isna())
            & (modelis["galia_kw"].isna())
            & (modelis["galia_ag"].isna())
        ),
        0,
        1,
    )

    modelis = modelis.loc[modelis["remove"] == 1]

    # Kuras. Standartizuojame. Jei neturi iraso, tokias eilutes eliminuojame
    modelis["kuras"] = np.where(
        (modelis["kuras"] == "Benzinas / dujos"),
        "Benzinas/Dujos",
        np.where(
            (modelis["kuras"] == "Benzinas / elektra"),
            "Benzinas/Elektra",
            np.where(
                (modelis["kuras"] == "Benzinas/dujos"),
                "Benzinas/Dujos",
                np.where(
                    (modelis["kuras"] == "Dujos"), "Benzinas/Dujos", modelis["kuras"]
                ),
            ),
        ),
    )

    # Jei kuras tulpelyje nera reiksmes arba reiksme lygi Kita tokias eilutes salinti
    modelis = modelis.loc[(modelis["kuras"].notna()) & (modelis["kuras"] != "Kita")]

    # Istriname galia_kw jei nera iraso
    modelis = modelis.loc[modelis["galia_kw"].notna()]

    # Rida. Jei nan reiksme pakeiciame i 0. Tada konvertuojame i int tipa
    modelis["rida"] = modelis["rida"].str.replace(".", "", regex=False)

    modelis["rida"] = np.where((modelis["rida"].isna()), "0", modelis["rida"])

    modelis["rida"] = pd.to_numeric(modelis["rida"])

    # Paskaiciuojame ridu vidurki
    ridos_vidurkis = modelis.copy()

    # Istriname tas eilutes kur nera irasu
    ridos_vidurkis = ridos_vidurkis.loc[ridos_vidurkis["rida"] != 0]

    # Sugrupuojame duomenis ir isvedame vidurki
    ridos_vidurkis = (
        ridos_vidurkis.groupby(["gamintojas", "modelis", "metai", "kuras"])[["rida"]]
        .mean()
        .reset_index()
        .rename(columns={"rida": "rida_mean"})
    )

    # Pridedame prie df modelis
    car_final = pd.merge(
        modelis,
        ridos_vidurkis,
        how="left",
        on=["gamintojas", "modelis", "metai", "kuras"],
    )

    # Jei rida lygu 0 tokiu atveju graziname reiksme is rida_mean
    car_final["rida_final"] = np.where(
        (car_final["rida"] == 0), car_final["rida_mean"], car_final["rida"]
    )

    # Jei rida_fiinal yra nan reiksme tokias eilutes eliminuoti
    car_final = car_final.loc[car_final["rida_final"].notna()]

    # Sugrupuojame paziureti kiek vienetu yra kiekvieno gamintojo
    car_final_gr = (
        car_final.groupby(["gamintojas"])[["gamintojas"]]
        .count()
        .rename(columns={"gamintojas": "count_final"})
        .reset_index()
    )

    # Jei kiekis yra mazesnis uz 10 tokius eliminuojame
    car_final_gr = car_final_gr.loc[car_final_gr["count_final"] > 10]

    # Pridedame prie car_final df ir kur nera duomenu istrinti
    car_final = pd.merge(car_final, car_final_gr, how="left", on="gamintojas")

    car_final = car_final.loc[car_final["count_final"].notna()]

    # Standartizuojame ridas. Ridu rezis kas 1000 km
    car_final["rida_std"] = (car_final["rida_final"] / 1000).apply(np.ceil) * 1000

    # Paskaiciuojame amziu. Is einamuju metu atimame 'metai'.
    car_final["amzius"] = 2023 - car_final["metai"]

    # Istriname nereikalingus stulpelius
    car_final = car_final.drop(
        [
            "variklio_turis",
            "duru_sk",
            "count",
            "remove",
            "rida",
            "rida_mean",
            "count_final",
            "galia_ag",
            "metai",
            "rida_final",
            "kebulas",
        ],
        axis=1,
    )

    # Pervadiname stulpelius
    car_final = car_final.rename(columns={"rida_std": "rida"})

    return car_final
