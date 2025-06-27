import streamlit as st
import pandas as pd
from calculs_hydro import (
    mois_noms_std,
    calcul_etp_par_df, calcul_pe
)

# ────────────── INTERFACE ──────────────
def main():
    st.set_page_config(page_title="ETP & Pluie efficace", layout="wide")
    st.title("🌍 Calcul de l'Évapotranspiration Potentielle (ETP) & Pluie Efficace par la méthode de Thornthwaite (1948)")

    # Tutoriel d’utilisation
    st.markdown("""
# Tutoriel d’utilisation

Cette application permet de calculer l’**évapotranspiration potentielle (ETP)** mensuelle par station et année selon la méthode de **Thornthwaite**, ainsi que la **pluie efficace** en tenant compte du bilan hydrique sol/pluie/évaporation.

### Étapes principales :

1. **Entrée des données** :  
   - Saisir manuellement les températures (°C) et précipitations (mm) moyennes mensuelles pour chaque station, ou  
   - Importer un fichier CSV/Excel avec les colonnes "Station", "Année", "mois", "Température (°C)", "Pluie (mm)".

2. **Calcul de l’ETP** :  
   - Calcul des indices mensuels *i*, puis de l’indice annuel *I* et du coefficient *a*.  
   - Application de la formule Thornthwaite pour chaque mois ou interpolation selon la table si température ≥ 26.5°C.  
   - Application des coefficients K selon latitude et hémisphère pour obtenir l’ETP corrigée (ETPc).

3. **Calcul de la pluie efficace** :  
   - Simulation d’un réservoir de stockage d’eau dans le sol (RFU) avec capacité maximale réglable.  
   - Calcul mensuel de la pluie efficace disponible, de l’évapotranspiration réelle (ETR) et de la réserve RFU.

4. **Visualisation & export** :  
   - Résultats affichés dans des tableaux.  
   - Possibilité d’exporter au format CSV.

---
*Pour commencer, choisissez un mode d’entrée et cliquez sur les boutons pour lancer les calculs.*
""")

    # ────────────── FORMULAIRE UNIFIÉ ──────────────
    st.header("🔧 Configuration des stations")

    with st.expander("Paramètres des stations", expanded=True):
        nb_stations = st.number_input("Nombre de stations:", 1, 10, 1, key="nb_stations")
        rfu_max = st.number_input("Capacité maximale du réservoir (RFU max en mm)", 0.0, 500.0, 100.0)

        stations_info = []
        for i in range(nb_stations):
            cols = st.columns(3)
            nom = cols[0].text_input(f"Nom station {i+1}:", f"Station_{i+1}", key=f"nom_{i}")
            hemisphere = cols[1].selectbox(f"Hémisphère:", ["Nord", "Sud"], key=f"hemi_{i}")
            latitude = cols[2].number_input(f"Latitude (°):", 0.0, 60.0, 10.0, key=f"lat_{i}")

            stations_info.append({
                "Station": nom.strip(),
                "Hémisphère": hemisphere,
                "Latitude": latitude
            })

    stations_info_df = pd.DataFrame(stations_info).drop_duplicates(subset="Station")

    # ────────────── SAISIE DES DONNÉES ──────────────
    st.header("📊 Entrée des données")
    mode = st.radio("Mode d'entrée:", ["📝 Saisie manuelle", "📁 Importer fichier"])

    if mode == "📝 Saisie manuelle":
        all_data = []
        for station in stations_info:
            st.subheader(f"🌍 {station['Station']}")
            nb_annees = st.number_input(f"Nombre d'années", 1, 30, 1, key=f"an_{station['Station']}")

            for a in range(nb_annees):
                annee = st.text_input("Année", "2023", key=f"an_{station['Station']}_{a}")
                for i, mois in enumerate(mois_noms_std):
                    cols = st.columns(2)
                    T = cols[0].number_input(f"{mois} - Température (°C)", -50.0, 50.0, 25.0, key=f"T_{station['Station']}_{annee}_{i}")
                    P = cols[1].number_input(f"{mois} - Pluie (mm)", 0.0, 1000.0, 100.0, key=f"P_{station['Station']}_{annee}_{i}")
                    all_data.append({
                        "Station": station["Station"], "Année": annee,
                        "mois": mois, "Température (°C)": T, "Pluie (mm)": P,
                        "Hémisphère": station["Hémisphère"],
                        "Latitude": station["Latitude"]
                    })
        df = pd.DataFrame(all_data)

    else:
        fichier = st.file_uploader("📁 Charger un fichier (CSV/Excel)", type=["csv", "xlsx"])
        if fichier:
            df = pd.read_csv(fichier, sep=";") if fichier.name.endswith(".csv") else pd.read_excel(fichier)
            df.columns = [col.strip().capitalize() for col in df.columns]

            if "Station" in df.columns:
                # Nettoyage des colonnes Station avant fusion
                df["Station"] = df["Station"].astype(str).str.strip()
                stations_info_df["Station"] = stations_info_df["Station"].astype(str).str.strip()

                # Fusion avec les infos des stations
                df = pd.merge(
                    df,
                    stations_info_df[["Station", "Hémisphère", "Latitude"]],
                    on="Station",
                    how="left"
                )

                # 🔍 Vérification des colonnes après fusion
                if "Hémisphère" not in df.columns or "Latitude" not in df.columns:
                    st.error("❌ Échec de la fusion : les colonnes 'Hémisphère' ou 'Latitude' sont manquantes. Vérifiez les noms des stations.")
                else:
                    if df["Hémisphère"].isnull().any() or df["Latitude"].isnull().any():
                        stations_inconnues = df[df["Hémisphère"].isnull()]["Station"].unique()
                        st.error(f"⚠️ Les stations suivantes n'ont pas pu être reconnues : {', '.join(stations_inconnues)}")

    # ────────────── CALCULS ──────────────
    if 'df' in locals() and not df.empty:
        if st.button("📊 Calculer ETP"):
            with st.spinner("Calcul de l'ETP..."):
                etp_df, resume_df = calcul_etp_par_df(df, stations_info_df, st=st)
                if etp_df is not None:
                    st.dataframe(etp_df)
                    st.subheader("🔍 Résumé")
                    st.dataframe(resume_df)
                    st.download_button("💾 Télécharger ETP", etp_df.to_csv(index=False, sep=";").encode("utf-8"), "resultats_etp.csv")

        if st.button("🌧️ Calculer Pluie efficace"):
            with st.spinner("Calcul pluie efficace..."):
                if "ETP corrigé (mm)" not in df.columns:
                    df, _ = calcul_etp_par_df(df, stations_info_df, st=st)
                if df is not None:
                    pe_df = calcul_pe(df, rfu_max)
                    st.dataframe(pe_df)
                    st.download_button("💾 Télécharger résultats", pe_df.to_csv(index=False, sep=";").encode("utf-8"), "resultats_complets.csv")

if __name__ == "__main__":
    main()
