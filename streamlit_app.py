import streamlit as st
import pandas as pd

# Ustawienia
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Zbrojenia Wrocław - Automat", layout="wide")
st.title("🏗️ System Sumowania Wag (Automatyczny)")

# Inicjalizacja danych
if 'macierze' not in st.session_state:
    st.session_state.macierze = {i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)}

# Funkcja obsługująca ENTER
def dodaj_wage_enter(nr):
    waga_key = f"waga_val_{nr}"
    if st.session_state[waga_key] > 0:
        sr = st.session_state[f"sr_{nr}"]
        tp = st.session_state[f"tp_{nr}"]
        waga = st.session_state[waga_key]
        
        # Dodaj do macierzy
        st.session_state.macierze[nr].at[tp, sr] += round(waga, 2)
        # UWAGA: Streamlit wyczyści pole po rerun, jeśli nie użyjemy form, 
        # ale musimy zresetować wartość w session_state, żeby nie dodawało w kółko tego samego
        st.session_state[waga_key] = 0.0

# 1. PANELE LIST (1-6)
for i in range(1, 7):
    with st.expander(f"📋 STALLISTA NR {i}", expanded=(i==1)):
        c1, c2, c3 = st.columns([1, 1, 2])
        
        with c1:
            st.selectbox("Średnica", SREDNICE, key=f"sr_{i}")
        with c2:
            st.selectbox("Typ", TYPY, key=f"tp_{i}")
        with c3:
            # KLUCZOWE: on_change powoduje, że ENTER od razu dodaje wagę
            st.number_input("Wpisz wagę [kg] i naciśnij ENTER", 
                           min_value=0.0, step=0.01, format="%.2f", 
                           key=f"waga_val_{i}", 
                           on_change=dodaj_wage_enter, args=(i,))

        # TABELA EDYTOWALNA - poprawiasz błędy klikając w komórkę
        st.session_state.macierze[i] = st.data_editor(
            st.session_state.macierze[i],
            key=f"edit_{i}",
            use_container_width=True
        )
        
        if st.button(f"🗑️ Wyczyść Listę {i}", key=f"clr_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()

# 2. PODSUMOWANIE ZAKRESOWE (DOKŁADNIE JAK W TWOIM EXCELU)
st.divider()
st.header("📊 ZBIORCZE PODSUMOWANIE (Wszystkie Listy)")

df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

summary_excel = pd.DataFrame(index=TYPY)
summary_excel["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
summary_excel["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
summary_excel["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary_excel["SUMA TYPU [kg]"] = summary_excel.sum(axis=1)

st.table(summary_excel.style.format("{:.2f}"))

total_kg = summary_excel["SUMA TYPU [kg]"].sum()
st.success(f"### WAGA CAŁKOWITA ZAMÓWIENIA: {total_kg:.2f} kg ({total_kg/1000:.3f} t)")
