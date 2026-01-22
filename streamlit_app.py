import streamlit as st
import pandas as pd

# Wagi jednostkowe wg Twojego arkusza
WAGI = {
    6: 0.222, 8: 0.395, 10: 0.617, 12: 0.888, 14: 1.21,
    16: 1.58, 20: 2.47, 25: 3.85, 28: 4.83, 32: 6.31
}

st.set_page_config(page_title="Kalkulator Zbrojenia - Wrocław", layout="wide")

st.title("🏗️ Szybkie Sumowanie Stallist")

# Inicjalizacja pamięci aplikacji
if 'listy' not in st.session_state:
    st.session_state.listy = {i: [] for i in range(1, 7)}

def dodaj_pozycje(nr_listy, sr, t, dl):
    if dl > 0:
        waga = round(dl * WAGI[sr], 2)
        nowa_pozycja = {
            "Średnica [mm]": sr,
            "Typ": t,
            "Długość [mb]": round(dl, 2),
            "Waga [kg]": waga
        }
        st.session_state.listy[nr_listy].append(nowa_pozycja)

total_order_weight = 0

# Tworzenie 6 sekcji
for i in range(1, 7):
    with st.expander(f"📋 STALLISTA NR {i} (Suma: {sum(d['Waga [kg]'] for d in st.session_state.listy[i]):.2f} kg)", expanded=(i==1)):
        
        # Formularz wprowadzania - Enter automatycznie wysyła formularz
        with st.form(key=f"form_{i}", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns([1, 1, 2, 1])
            with c1:
                sr = st.selectbox("Średnica", list(WAGI.keys()), key=f"s_sel_{i}")
            with c2:
                typ = st.selectbox("Typ", ["Proste", "Gięte", "3D"], key=f"t_sel_{i}")
            with c3:
                # Naciśnięcie ENTER w tym polu doda pozycję do listy
                dl = st.number_input("Długość [mb] + ENTER", min_value=0.0, step=0.1, format="%.2f", key=f"d_in_{i}")
            with c4:
                st.write("") # Odstęp
                submit = st.form_submit_button("Dodaj ręcznie")
            
            if submit or (dl > 0):
                dodaj_pozycje(i, sr, typ, dl)
                st.rerun()

        # Tabela wyników dla danej listy
        if st.session_state.listy[i]:
            df = pd.DataFrame(st.session_state.listy[i])
            st.table(df)
            if st.button(f"🗑️ Wyczyść listę {i}", key=f"clear_{i}"):
                st.session_state.listy[i] = []
                st.rerun()
            
            total_order_weight += df["Waga [kg]"].sum()

# --- STOPKA Z PODSUMOWANIEM ---
st.divider()
c_total1, c_total2 = st.columns(2)
with c_total1:
    st.subheader(f"Waga całkowita: {total_order_weight:.2f} kg")
with c_total2:
    st.subheader(f"Waga w tonach: {total_order_weight/1000:.3f} t")
