import streamlit as st
import pandas as pd

# Standardowe wagi jednostkowe (kg/mb) wg Twojego Excela
WAGI = {
    6: 0.222, 8: 0.395, 10: 0.617, 12: 0.888, 14: 1.210,
    16: 1.580, 20: 2.470, 25: 3.850, 28: 4.830, 32: 6.310
}

st.set_page_config(page_title="Kalkulator Zbrojenia Wrocław", layout="wide")

st.title("🏗️ System Ewidencji Stallist")
st.write("Wprowadź dane dla poszczególnych list stali. Możesz dodać wiele średnic do każdej listy.")

if 'listy' not in st.session_state:
    st.session_state.listy = {i: [] for i in range(1, 7)}

total_order_weight = 0

# Generowanie 6 sekcji Stallist
for i in range(1, 7):
    with st.expander(f"📋 STALLISTA NR {i}", expanded=(i==1)):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        
        with col1:
            srednica = st.selectbox(f"Średnica #{i}", list(WAGI.keys()), key=f"s_{i}")
        with col2:
            typ = st.selectbox(f"Typ #{i}", ["Proste", "Gięte", "3D"], key=f"t_{i}")
        with col3:
            dlugosc = st.number_input(f"Długość łączna [mb] #{i}", min_value=0.0, step=0.1, key=f"d_{i}")
        with col4:
            if st.button(f"➕ Dodaj do listy {i}", key=f"b_{i}"):
                waga = round(dlugosc * WAGI[srednica], 2)
                st.session_state.listy[i].append({
                    "Średnica [mm]": srednica,
                    "Typ": typ,
                    "Długość [mb]": dlugosc,
                    "Waga [kg]": waga
                })
        with col5:
            if st.button(f"🗑️ Wyczyść listę {i}", key=f"c_{i}"):
                st.session_state.listy[i] = []

        # Wyświetlanie tabeli dla danej listy
        if st.session_state.listy[i]:
            df = pd.DataFrame(st.session_state.listy[i])
            st.table(df)
            suma_listy = df["Waga [kg]"].sum()
            st.info(f"Suma dla Stallisty {i}: **{suma_listy:.2f} kg**")
            total_order_weight += suma_listy
        else:
            st.write("Lista jest pusta.")

# --- PODSUMOWANIE CAŁOŚCI ---
st.divider()
st.header("📊 Podsumowanie Całkowite")
col_res1, col_res2 = st.columns(2)

with col_res1:
    st.metric("ŁĄCZNA WAGA [kg]", f"{total_order_weight:.2f} kg")
with col_res2:
    st.metric("ŁĄCZNA WAGA [tony]", f"{total_order_weight/1000:.3f} t")

if st.button("📥 Eksportuj wyniki (Podgląd tekstowy)"):
    st.code(str(st.session_state.listy))