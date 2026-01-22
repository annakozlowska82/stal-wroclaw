import streamlit as st
import pandas as pd

# Konfiguracja średnic i typów
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Zbrojenia Wrocław - Szybki Sumator", layout="wide")

# CSS do ukrycia przycisku formularza (żeby nie drażnił wzroku)
st.markdown("""
    <style>
    div[data-testid="stFormSubmitButton"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ System Sumowania Wag Stali")

# Inicjalizacja danych w pamięci
if 'macierze' not in st.session_state:
    st.session_state.macierze = {
        i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)
    }

# Funkcja dodająca wagę wywoływana przy zmianie w polu
def dodaj_wage_callback(nr):
    key_waga = f"w_in_{nr}"
    key_sr = f"sr_sel_{nr}"
    key_tp = f"tp_sel_{nr}"
    
    waga_val = st.session_state[key_waga]
    sr_val = st.session_state[key_sr]
    tp_val = st.session_state[key_tp]
    
    if waga_val > 0:
        st.session_state.macierze[nr].at[tp_val, sr_val] += round(waga_val, 2)
        # Nie czyścimy ręcznie, number_input z on_change sam obsłuży stan

# 1. SEKCJA WPISYWANIA (6 LIST)
for i in range(1, 7):
    suma_listy = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} (Suma: {suma_listy:.2f} kg)", expanded=(i==1)):
        
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_sel_{i}")
        with c2:
            st.selectbox("Typ", TYPY, key=f"tp_sel_{i}")
        with c3:
            # Używamy on_change - to reaguje na Enter natychmiast
            st.number_input("Wpisz wagę [kg] i naciśnij ENTER", 
                           min_value=0.0, step=0.01, format="%.2f", 
                           key=f"w_in_{i}", 
                           on_change=dodaj_wage_callback, args=(i,))

        # EDYTOWALNA TABELA - tutaj poprawiasz błędy
        st.write("Podgląd i edycja (kliknij w komórkę, aby zmienić):")
        st.session_state.macierze[i] = st.data_editor(
            st.session_state.macierze[i],
            key=f"editor_{i}",
            use_container_width=True
        )
        
        if st.button(f"🗑️ Wyczyść Listę {i}", key=f"clr_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()

# 2. PODSUMOWANIE ZAKRESOWE (DLA CAŁOŚCI)
st.divider()
st.header("📊 Zestawienie Zakresowe (Wszystkie Listy)")

df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

summary_excel = pd.DataFrame(index=TYPY)
summary_excel["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
summary_excel["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
summary_excel["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary_excel["RAZEM [kg]"] = summary_excel.sum(axis=1)

st.table(summary_excel.style.format("{:.2f}"))

total_kg = summary_excel["RAZEM [kg]"].sum()
st.success(f"### WAGA CAŁKOWITA ZAMÓWIENIA: {total_kg:.2f} kg ({total_kg/1000:.3f} t)")
