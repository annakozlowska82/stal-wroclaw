import streamlit as st
import pandas as pd

# Ustawienia średnic i typów
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Zbrojenia - Sumator Wag", layout="wide")
st.title("🏗️ System Ewidencji Wag Stallist")

# Inicjalizacja danych
if 'macierze' not in st.session_state:
    st.session_state.macierze = {
        i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)
    }

# 1. SEKCJA WPISYWANIA DANYCH (6 LIST)
for i in range(1, 7):
    # Wyświetlamy aktualną sumę listy w nagłówku sekcji
    suma_listy_kg = st.session_state.macierze[i].values.sum()
    
    with st.expander(f"📋 STALLISTA NR {i} (Suma: {suma_listy_kg:.2f} kg)", expanded=(i==1)):
        # Formularz wprowadzania
        with st.form(key=f"form_{i}", clear_on_submit=True):
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                sr = st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_{i}")
            with c2:
                tp = st.selectbox("Typ", TYPY, key=f"tp_{i}")
            with c3:
                # Wpisujesz wagę i naciskasz Enter
                waga = st.number_input("Wpisz wagę [kg] i naciśnij ENTER", min_value=0.0, step=0.01, format="%.2f", key=f"w_{i}")
            
            # Formularz wymaga przycisku, ale Enter zadziała jako submit
            submitted = st.form_submit_button("Dodaj do listy")
            
            if submitted and waga > 0:
                st.session_state.macierze[i].at[tp, sr] += round(waga, 2)
                st.rerun()

        # Wyświetlanie tabeli dla danej listy
        st.write(f"Wagi na liście nr {i}:")
        st.table(st.session_state.macierze[i].style.format("{:.2f}"))
        
        if st.button(f"🗑️ Wyczyść Listę {i}", key=f"clr_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()

# 2. ZBIORCZE PODSUMOWANIE (JAK W EXCELU)
st.divider()
st.header("📊 PODSUMOWANIE ZAKRESÓW (Wszystkie listy)")

# Łączymy wszystkie listy w jedną macierz zbiorczą
df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

# Grupowanie w zakresy z Excela
summary_excel = pd.DataFrame(index=TYPY)
summary_excel["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
summary_excel["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
summary_excel["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary_excel["RAZEM [kg]"] = summary_excel.sum(axis=1)

# Wyświetlanie końcowej tabeli
st.table(summary_excel.style.format("{:.2f}"))



# Ostateczny wynik
calosc_kg = summary_excel["RAZEM [kg]"].sum()

c_res1, c_res2 = st.columns(2)
with c_res1:
    st.info(f"### WAGA CAŁKOWITA: {calosc_kg:.2f} kg")
with c_res2:
    st.success(f"### WAGA CAŁKOWITA: {calosc_kg/1000:.3f} t")
