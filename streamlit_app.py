import streamlit as st
import pandas as pd

# Konfiguracja średnic i typów
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Zbrojenia Wrocław - Edytowalny Sumator", layout="wide")
st.title("🏗️ System Sumowania Wag Stali")

# Inicjalizacja 6 macierzy w pamięci sesji
if 'macierze' not in st.session_state:
    st.session_state.macierze = {
        i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)
    }

# 1. SEKCJA WPISYWANIA (6 LIST)
for i in range(1, 7):
    with st.expander(f"📋 STALLISTA NR {i}", expanded=(i==1)):
        
        # Formularz bez widocznego przycisku (zatwierdzany ENTEREM)
        with st.form(key=f"form_{i}", clear_on_submit=True):
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                sr = st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_sel_{i}")
            with c2:
                tp = st.selectbox("Typ", TYPY, key=f"tp_sel_{i}")
            with c3:
                # Wpisujesz wagę i naciskasz ENTER
                waga = st.number_input("Wpisz wagę [kg] i naciśnij ENTER", 
                                     min_value=0.0, step=0.01, format="%.2f", key=f"w_in_{i}")
            
            # Ukryty przycisk, który pozwala na działanie ENTER
            st.form_submit_button("Dodaj", use_container_width=True)
            
            if waga > 0:
                st.session_state.macierze[i].at[tp, sr] += round(waga, 2)
                st.rerun()

        # EDYTOWALNA TABELA - możesz kliknąć w komórkę i poprawić błąd
        st.write("Podgląd listy (kliknij w komórkę, aby edytować wagę):")
        edited_df = st.data_editor(
            st.session_state.macierze[i],
            key=f"editor_{i}",
            use_container_width=True
        )
        # Zapisywanie zmian wprowadzonych ręcznie w tabeli
        st.session_state.macierze[i] = edited_df

# 2. PODSUMOWANIE ZAKRESOWE (JAK W EXCELU)
st.divider()
st.header("📊 ZBIORCZE PODSUMOWANIE ZAKRESÓW")

# Sumujemy wszystkie 6 tabel
df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

summary_excel = pd.DataFrame(index=TYPY)
summary_excel["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
summary_excel["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
summary_excel["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary_excel["RAZEM [kg]"] = summary_excel.sum(axis=1)

# Wyświetlanie tabeli końcowej
st.table(summary_excel.style.format("{:.2f}"))

# Wynik końcowy
total_kg = summary_excel["RAZEM [kg]"].sum()
st.info(f"### ŁĄCZNA WAGA CAŁOŚCI: {total_kg:.2f} kg ({total_kg/1000:.3f} t)")
