import streamlit as st
import pandas as pd
import numpy as np

# Konfiguracja wag jednostkowych
WAGI = {6: 0.222, 8: 0.395, 10: 0.617, 12: 0.888, 14: 1.21, 16: 1.58, 20: 2.47, 25: 3.85, 28: 4.83, 32: 6.31}
SREDNICE = list(WAGI.keys())
TYPY = ["Proste", "Gięte", "3D"]

st.set_page_config(page_title="Zbrojenie Wrocław - Kalkulator", layout="wide")
st.title("🏗️ System Sumowania Stallist (kg)")

# Inicjalizacja danych w pamięci (6 pustych macierzy)
if 'macierze' not in st.session_state:
    st.session_state.macierze = {
        i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)
    }

def dodaj_do_macierzy(nr, sr, typ, dl):
    if dl > 0:
        waga_kg = round(dl * WAGI[sr], 2)
        st.session_state.macierze[nr].at[typ, sr] += waga_kg

total_all_kg = 0

# Generowanie 6 sekcji
for i in range(1, 7):
    suma_listy = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} | Suma: {suma_listy:.2f} kg", expanded=(i==1)):
        
        # Formularz wprowadzania
        with st.form(key=f"form_{i}", clear_on_submit=True):
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                sr_input = st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_{i}")
            with col2:
                typ_input = st.selectbox("Typ obróbki", TYPY, key=f"typ_{i}")
            with col3:
                # WPISZ I NACIŚNIJ ENTER
                dl_input = st.number_input("Długość [mb] + ENTER", min_value=0.0, step=0.1, format="%.2f", key=f"dl_{i}")
            
            submit = st.form_submit_button("Dodaj do tabeli")
            if submit or (dl_input > 0):
                dodaj_do_macierzy(i, sr_input, typ_input, dl_input)
                st.rerun()

        # Wyświetlanie tabeli w układzie: Wiersze (Typ) x Kolumny (Średnica)
        st.write("**Zestawienie wagowe [kg]:**")
        df_display = st.session_state.macierze[i].copy()
        
        # Dodanie kolumny "RAZEM" dla wierszy
        df_display['RAZEM [kg]'] = df_display.
