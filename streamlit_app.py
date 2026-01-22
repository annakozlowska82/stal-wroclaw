import streamlit as st
import pandas as pd

# Konfiguracja zgodnie z Twoim Excelem
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Sumator Stali - Wrocław", layout="wide")
st.title("🏗️ Automatyczny Kalkulator Stallist")

# Inicjalizacja baz danych dla 6 list
if 'macierze' not in st.session_state:
    st.session_state.macierze = {i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)}

# Funkcja obsługująca ENTER (Callback)
def dodaj_wage_automatycznie(nr_listy):
    input_key = f"input_waga_{nr_listy}"
    nowa_waga = st.session_state[input_key]
    
    if nowa_waga > 0:
        wybrana_sr = st.session_state[f"sr_{nr_listy}"]
        wybrany_typ = st.session_state[f"tp_{nr_listy}"]
        
        # Dodanie do tabeli
        st.session_state.macierze[nr_listy].at[wybrany_typ, wybrana_sr] += round(nowa_waga, 2)
        
        # Wyzerowanie pola po dodaniu (żeby było gotowe na następny wpis)
        st.session_state[input_key] = 0.0

# 1. SEKCJA 6 STALLIST
for i in range(1, 7):
    aktualna_suma = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} | Suma: {aktualna_suma:.2f} kg", expanded=(i==1)):
        
        # Pola wprowadzania danych
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.selectbox("Wybierz średnicę", SREDNICE, key=f"sr_{i}")
        with c2:
            st.selectbox("Wybierz typ", TYPY, key=f"tp_{i}")
        with c3:
            # ON_CHANGE sprawia, że Enter wyzwala funkcję dodawania
            st.number_input("Wpisz wagę [kg] i naciśnij ENTER", 
                           min_value=0.0, step=0.01, format="%.2f", 
                           key=f"input_waga_{i}", 
                           on_change=dodaj_wage_automatycznie, args=(i,))

        # EDYTOWALNA TABELA - tutaj poprawiasz błędy ręcznie
        st.write("Tabela Listy (kliknij komórkę, aby edytować):")
        st.session_state.macierze[i] = st.data_editor(
            st.session_state.macierze[i], 
            key=f"editor_{i}", 
            use_container_width=True
        )
        
        if st.button(f"Wyczyść Listę {i}", key=f"clear_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()

# 2. PODSUMOWANIE ZAKRESOWE (DOKŁADNIE JAK W EXCELU)
st.divider()
st.header("📊 Zestawienie Zakresowe (Suma wszystkich list)")

# Łączenie wszystkich danych
df_all = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

summary = pd.DataFrame(index=TYPY)
summary["#6 - #8 [kg]"] = df_all[[6, 8]].sum(axis=1)
summary["#10 - #12 [kg]"] = df_all[[10, 12]].sum(axis=1)
summary["#14 - #32 [kg]"] = df_all[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary["SUMA [kg]"] = summary.sum(axis=1)



st.table(summary.style.format("{:.2f}"))

# Wynik końcowy zamówienia
total_all = summary["SUMA [kg]"].sum()
st.success(f"### ŁĄCZNA WAGA CAŁEGO ZAMÓWIENIA: {total_all:.2f} kg ({total_all/1000:.3f} t)")
