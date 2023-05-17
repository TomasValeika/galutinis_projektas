# Projektas

**Projektas: Automobilių kainos prognozavimas**
Problematika:\
Kaip teisingai nustatyti savo automobilio kainą jį parduodant? Kaip nuspręstiar perkamo automobilio kaina adekvati?

## Projekto eiga

### Duomenų surinkimas

1. Duomenys buvo paimti iš automobilių skelbimų svetainių:

- autogidas.lt
- autobilis.lt
- autobonus.lt
- automobilis.lt

2. Naudota biblioteka - **_scrapy_**
3. Kiekvienos svetainės svetainės duomenys buvo išsaugoti atskiruose csv dokumentuose
4. Kiekvienas dokumentas buvo išvalytas ir užpildytas trūkstamais duomenimis
5. Apjungtas į vieną bendrą 'dataframe'

### ML dalis

1. Naudoti mokymo algoritmai :

- linear_model
- CatBoostRegressor
- RandomForestRegressor

2. Geriausią rezultatą parodė CatBoostRegressor - **0.9607**, RandomForestRegressor - **0.9135**
3. Šis modelis buvo išsaugotas 'deployment'

### Deployment

Modelis yra atvaizduojamas dodojant **streamlit** biblioteką. \
Vartotojas pasirinkdamas laukus sukuria df kuris perduodamas modeliui. \
Pasirinkimų apačioje vartotojas mato prognozuojamą kainą.

### Streamlit paleidimas

1. Parsisiųsti visus failus.
2. Terminale įveskite **streamlit run main.py**
3. Interneto naršyklėje bus užkrauta svetainė su modeliu.
