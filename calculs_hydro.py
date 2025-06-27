import pandas as pd
import numpy as np
import unicodedata
from io import StringIO

# ────────────── NORMALISATION DES MOIS ──────────────
def normaliser_mois(mois):
    mois = mois.lower().strip()
    mapping = {
        'janvier': 'Janvier',
        'fevrier': 'Février', 'février': 'Février',
        'mars': 'Mars',
        'avril': 'Avril',
        'mai': 'Mai',
        'juin': 'Juin',
        'juillet': 'Juillet',
        'aout': 'Août', 'août': 'Août',
        'septembre': 'Septembre',
        'octobre': 'Octobre',
        'novembre': 'Novembre',
        'decembre': 'Décembre', 'décembre': 'Décembre'  # Gère les deux formes
    }
    return mapping.get(mois, mois.capitalize())  # Retourne le mois normalisé

mois_noms_std = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

etp_table = {26.5:135.0, 27.0:139.5, 27.5:143.7, 28.0:147.8, 28.5:151.7,
             29.0:155.4, 29.5:158.9, 30.0:162.1, 30.5:165.2, 31.0:168.0}

#Chargement des coefficients de correction K
# ────────────── TABLES K ──────────────
K_NORD_CSV = """Latitude,Janvier,Février,Mars,Avril,Mai,Juin,Juillet,Août,Septembre,Octobre,Novembre,Décembre
0,1.04,0.94,1.04,1.01,1.04,1.01,1.04,1.01,1.04,1.01,1.01,1.01
5,1.02,0.93,1.03,1.02,1.06,1.03,1.06,1.05,1.01,1.03,0.99,1.02
10,1,0.91,1.03,1.03,1.08,1.06,1.08,1.07,1.02,1.02,0.98,0.99
15,0.97,0.91,1.03,1.04,1.11,1.08,1.12,1.08,1.02,1.01,0.95,0.97
20,0.95,0.9,1.03,1.05,1.13,1.11,1.14,1.11,1.02,1,0.93,0.94
25,0.93,0.89,1.03,1.06,1.15,1.14,1.17,1.12,1.02,0.99,0.91,0.91
26,0.92,0.88,1.03,1.06,1.15,1.15,1.17,1.12,1.02,0.99,0.91,0.91
27,0.92,0.88,1.03,1.07,1.16,1.15,1.18,1.13,1.02,0.99,0.9,0.9
28,0.91,0.88,1.03,1.07,1.16,1.16,1.18,1.13,1.02,0.98,0.9,0.9
29,0.91,0.87,1.03,1.07,1.17,1.16,1.19,1.13,1.03,0.98,0.9,0.89
30,0.9,0.87,1.03,1.08,1.18,1.17,1.2,1.14,1.03,0.98,0.89,0.88
31,0.9,0.87,1.03,1.08,1.18,1.18,1.2,1.14,1.03,0.98,0.89,0.88
32,0.89,0.86,1.03,1.08,1.19,1.19,1.21,1.15,1.03,0.98,0.88,0.87
33,0.88,0.86,1.03,1.09,1.19,1.2,1.22,1.15,1.03,0.97,0.88,0.86
34,0.88,0.85,1.03,1.09,1.2,1.2,1.22,1.16,1.03,0.97,0.87,0.86
35,0.87,0.85,1.03,1.09,1.21,1.21,1.23,1.16,1.03,0.97,0.86,0.85
36,0.87,0.85,1.03,1.1,1.21,1.22,1.24,1.16,1.03,0.97,0.86,0.84
37,0.86,0.84,1.03,1.1,1.22,1.23,1.25,1.17,1.03,0.97,0.85,0.83
38,0.85,0.84,1.03,1.1,1.23,1.24,1.25,1.17,1.04,0.96,0.84,0.83
39,0.85,0.84,1.03,1.11,1.23,1.24,1.26,1.18,1.04,0.96,0.84,0.82
40,0.84,0.83,1.03,1.11,1.24,1.25,1.27,1.18,1.04,0.96,0.83,0.81
41,0.83,0.83,1.03,1.11,1.25,1.26,1.27,1.19,1.04,0.96,0.82,0.8
42,0.82,0.83,1.03,1.12,1.26,1.27,1.28,1.19,1.04,0.95,0.82,0.79
43,0.81,0.82,1.02,1.12,1.26,1.28,1.29,1.2,1.04,0.95,0.81,0.77
44,0.81,0.82,1.02,1.13,1.27,1.29,1.3,1.2,1.04,0.95,0.8,0.76
45,0.8,0.81,1.02,1.13,1.28,1.29,1.31,1.21,1.04,0.94,0.79,0.75
46,0.79,0.81,1.02,1.13,1.29,1.31,1.32,1.22,1.04,0.94,0.79,0.74
47,0.77,0.8,1.02,1.14,1.3,1.32,1.33,1.22,1.04,0.93,0.78,0.73
48,0.76,0.8,1.02,1.14,1.31,1.33,1.34,1.23,1.05,0.93,0.77,0.72
49,0.75,0.79,1.02,1.14,1.32,1.34,1.35,1.24,1.05,0.93,0.76,0.71
50,0.74,0.78,1.02,1.15,1.33,1.36,1.37,1.25,1.06,0.92,0.76,0.7"""

K_SUD_CSV = """Latitude,Janvier,Fevrier,Mars,Avril,Mai,Juin,Juillet,Aout,Septembre,Octobre,Novembre,Decembre
5,1.06,0.95,1.04,1,1.02,0.99,1.02,1.03,1,1.05,1.03,1.06
10,1.08,0.97,1.05,0.99,1.01,0.96,1,1.01,1,1.06,1.05,1.1
15,1.12,0.98,1.05,0.98,0.98,0.94,0.97,1,1,1.07,1.07,1.12
20,1.14,1,1.05,0.97,0.96,0.91,0.95,0.99,1,1.08,1.09,1.15
25,1.17,1.01,1.05,0.96,0.94,0.88,0.93,0.98,1,1.1,1.11,1.18
30,1.2,1.03,1.06,0.95,0.92,0.85,0.9,0.96,1,1.12,1.14,1.21
35,1.23,1.04,1.06,0.94,0.89,0.82,0.87,0.94,1,1.13,1.17,1.25
40,1.27,1.06,1.07,0.93,0.86,0.78,0.84,0.92,1,1.15,1.2,1.29
42,1.8,1.07,1.07,0.92,0.85,0.76,0.82,0.92,1,1.16,1.22,1.31
44,1.3,1.08,1.07,0.92,0.83,0.74,0.81,0.91,0.99,1.17,1.23,1.33
46,1.32,1.1,1.07,0.91,0.82,0.72,0.79,0.9,0.99,1.17,1.25,1.35
48,1.34,1.11,1.08,0.9,0.8,0.7,0.76,0.89,0.99,1.18,1.27,1.37
50,1.37,1.12,1.08,0.89,0.77,0.67,0.74,0.88,0.99,1.19,1.29,1.41"""

df_k_nord = pd.read_csv(StringIO(K_NORD_CSV))
df_k_sud = pd.read_csv(StringIO(K_SUD_CSV))

# ────────────── FONCTIONS DE CALCUL ──────────────
#Fonction pour obtenir le coefficient K
def get_k_coefficient(hemisphere, mois, latitude):
    mois = normaliser_mois(mois)
    df = df_k_nord if hemisphere == "Nord" else df_k_sud
    lat_values = df['Latitude'].values
    closest_lat = lat_values[np.abs(lat_values - latitude).argmin()]
    return df[df['Latitude'] == closest_lat][mois].values[0]

def etp_thornthwaite(T, I, a):
    return 16 * ((10 * T / I) ** a) if I > 0 else 0.0

def etp_interp(temp):
    if temp in etp_table:
        return etp_table[temp]
    keys = sorted(etp_table.keys())
    if temp < keys[0]:
        return etp_table[keys[0]]
    if temp > keys[-1]:
        return etp_table[keys[-1]]
    for i in range(len(keys)-1):
        if keys[i] <= temp <= keys[i+1]:
            return etp_table[keys[i]] + (temp - keys[i]) * (etp_table[keys[i+1]] - etp_table[keys[i]]) / (keys[i+1] - keys[i])

def calcul_I_et_a(temperatures):
    indices = [(T/5)**1.514 for T in temperatures]
    I = sum(indices)
    a = (6.75e-7 * I**3) - (7.71e-5 * I**2) + (1.792e-2 * I) + 0.49239
    return I, a

def calcul_etp_par_df(df, stations_info, st=None):
    df.columns = [col.strip().capitalize() for col in df.columns]
    df.rename(columns={
        "Température (°c)": "Température (°C)", "Temperature": "Température (°C)",
        "Pluie": "Pluie (mm)", "Precipitation": "Pluie (mm)",
        "Station": "Station", "Annee": "Année", "Année": "Année", "Mois": "mois"
    }, inplace=True)

    required = ["Station", "Année", "mois", "Température (°C)", "Pluie (mm)"]
    if not all(col in df.columns for col in required):
        if st: st.error("Colonnes manquantes")
        return None, None

    df["mois"] = df["mois"].apply(normaliser_mois)
    try:
        df["mois_num"] = df["mois"].apply(lambda x: mois_noms_std.index(x))
    except:
        if st: st.error("Erreur de correspondance des mois")
        return None, None

    if "Hémisphère" not in df.columns or "Latitude" not in df.columns:
        if stations_info is not None:
            df["Station"] = df["Station"].str.strip()
            stations_info["Station"] = stations_info["Station"].str.strip()
            stations_info = stations_info.drop_duplicates(subset=["Station"])
            df = df.drop_duplicates()
            df = pd.merge(df, stations_info, on="Station", how="left", validate="many_to_one")

            if df["Hémisphère"].isnull().any() or df["Latitude"].isnull().any():
                if st: st.error("Fusion échouée (infos manquantes)")
                return None, None
        else:
            if st: st.error("Informations des stations manquantes")
            return None, None

    df = df.reset_index(drop=True)
    result, resume = [], []
    for (station, annee), group in df.groupby(["Station", "Année"], sort=False):
        if len(group) != 12:
            if st: st.error(f"{station} {annee}: {len(group)} mois au lieu de 12")
            continue

        group = group.sort_values("mois_num")
        T_list = group["Température (°C)"].tolist()
        i_list = [(T/5)**1.514 if T > 0 else 0 for T in T_list]
        I = sum(i_list)
        a = (6.75e-7 * I**3) - (7.71e-5 * I**2) + (1.792e-2 * I) + 0.49239
        etp_vals = [round(etp_thornthwaite(T,I,a),2) if T<26.5 else round(etp_interp(T),2) for T in T_list]

        k_vals, etp_corr_vals = [], []
        for T, (_, row) in zip(etp_vals, group.iterrows()):
            try:
                k = get_k_coefficient(row["Hémisphère"], row["mois"], row["Latitude"])
                k_vals.append(round(k, 3))
                etp_corr_vals.append(round(k * T, 2))
            except:
                k_vals.append(np.nan)
                etp_corr_vals.append(np.nan)

        group = group.copy()
        group["i"] = i_list
        group["ETP (mm)"] = etp_vals
        group["K"] = k_vals
        group["ETP corrigé (mm)"] = etp_corr_vals

        result.append(group)
        resume.append({"Station": station, "Année": annee, "I": round(I,3), "a": round(a,5)})

    if not result:
        return None, None

    df_etp = pd.concat(result).drop(columns=["mois_num"])
    df_resume = pd.DataFrame(resume)
    return df_etp, df_resume

def calcul_pe(df, rfu_max):
    result = []
    for (station, annee), group in df.groupby(["Station", "Année"]):
        rfu = rfu_max
        pe_list, rfu_list, etr_list = [], [], []
        for _, row in group.iterrows():
            P = row["Pluie (mm)"]
            ETP = row["ETP corrigé (mm)"]
            if P > ETP:
                ETR = ETP
                exc = P - ETP
                add = min(rfu_max - rfu, exc) if rfu < rfu_max else 0
                rfu += add
                pe = exc - add
            else:
                ETR = P
                rfu = max(0, rfu - (ETP - P))
                pe = 0
            pe_list.append(round(pe,2))
            rfu_list.append(round(rfu,2))
            etr_list.append(round(ETR,2))

        group = group.copy()
        group["ETP utilisé (mm)"] = group["ETP corrigé (mm)"]
        group["RFU (mm)"] = rfu_list
        group["ETR (mm)"] = etr_list
        group["Pluie efficace (mm)"] = pe_list

        colonnes_ordre = ["Station", "Année", "mois", "Pluie (mm)", "ETP utilisé (mm)", "RFU (mm)", "ETR (mm)", "Pluie efficace (mm)"]
        if "K" in group.columns:
            colonnes_ordre.insert(4, "K")
        colonnes_existantes = [col for col in colonnes_ordre if col in group.columns]
        group = group[colonnes_existantes]

        result.append(group)

    return pd.concat(result)
