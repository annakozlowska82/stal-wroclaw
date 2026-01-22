import streamlit as st
import pandas as pd

# Konfiguracja
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Zbrojenia Wrocław", layout="wide")
st.title("🏗️ System Sumowania Wag Stallist")

# Inicjalizacja danych w pamięci
if 'macierze' not in st.session_state:
    st.session_state.macierze = {i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)}

# FUNKCJA CALLBACK - Wykonuje się natychmiast po naciśnięciu ENTER
def dodaj_wage_po_enterze(nr):
    waga_key = f"input_waga_{nr}"
    waga_wartosc = st.session_state[waga_key]
    
    if waga_wartosc > 0:
        wybrana_sr = st.session_state[f"sr_{nr}"]
        wybrany_tp = st.session_state[f"tp_{nr}"]
        
        # Dodanie wagi do odpowiedniej komórki w tabeli
        st.session_state.macierze[nr].at[wybrany_tp, wybrana_sr] += round(waga_wartosc, 2)
        
        # Resetowanie pola wpisywania, aby było puste po Enterze
        st.session_state[waga_key] = 0.0

# 1. GENEROWANIE 6 LIST
for i in range(1, 7):
    aktualna_suma = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} | Suma: {aktualna_suma:.2f} kg", expanded=(i==1)):
        
        # Interfejs wprowadzania
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_{i}")
        with c2:
            st.selectbox("Typ obróbki", TYPY, key=f"tp_{i}")
        with c3:
            # Brak formularza = brak przycisku. on_change reaguje na ENTER.
            st.number_input("Wpisz wagę i naciśnij ENTER", 
                           min_value=0.0, step=0.01, format="%.2f", 
                           key=f"input_waga_{i}", 
                           on_change=dodaj_wage_po_enterze, args=(i,))

        # EDYTOWALNA TABELA - tutaj klikasz w liczbę, żeby ją poprawić
        st.write("Podgląd tabeli (edytuj klikając w komórkę):")
        st.session_state.macierze[i] = st.data_editor(
            st.session_state.macierze[i],
            key=f"editor_{i}",
            use_container_width=True
        )
        
        if st.button(f"🗑️ Wyczyść listę {i}", key=f"clr_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()

# 2. PODSUMOWANIE ZAKRESOWE (DOKŁADNIE JAK W TWOIM EXCELU)
st.divider()
st.header("📊 ZBIORCZE PODSUMOWANIE ZAKRESÓW")

# Sumowanie wszystkich 6 list
df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

# Zakresy średnic
summary = pd.DataFrame(index=TYPY)
summary["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
summary["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
summary["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary["SUMA [kg]"] = summary.sum(axis=1)



st.table(summary.style.format("{:.2f}"))

total_final = summary["SUMA [kg]"].sum()
st.success(f"### ŁĄCZNA WAGA CAŁOŚCI: {total_final:.2f} kg ({total_final/1000:.3f} t)")
