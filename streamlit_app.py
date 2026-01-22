import streamlit as st
import pandas as pd

# Ustawienia
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Sumator Stali Wrocław", layout="wide")
st.title("🏗️ System Sumowania Wag Stallist")

# Inicjalizacja danych w pamięci
if 'macierze' not in st.session_state:
    st.session_state.macierze = {i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)}

# FUNKCJA OBSŁUGI ENTERA
def dodaj_wage_po_enterze(nr):
    klucz_wagi = f"waga_input_{nr}"
    waga = st.session_state[klucz_wagi]
    
    if waga > 0:
        sr = st.session_state[f"sr_wybor_{nr}"]
        tp = st.session_state[f"tp_wybor_{nr}"]
        
        # Dodanie wagi do tabeli
        st.session_state.macierze[nr].at[tp, sr] += round(waga, 2)
        
        # Automatyczne czyszczenie pola po Enterze
        st.session_state[klucz_wagi] = 0.0

# WYŚWIETLANIE 6 LIST
for i in range(1, 7):
    aktualna_suma = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} | Suma: {aktualna_suma:.2f} kg", expanded=(i==1)):
        
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_wybor_{i}")
        with c2:
            st.selectbox("Typ", TYPY, key=f"tp_wybor_{i}")
        with c3:
            # KLUCZOWE: on_change wywołuje funkcję natychmiast po naciśnięciu ENTER
            st.number_input("Wpisz wagę i daj ENTER", min_value=0.0, step=0.01, 
                           key=f"waga_input_{i}", 
                           on_change=dodaj_wage_po_enterze, args=(i,))

        # TABELA DO EDYCJI (Poprawianie pomyłek)
        st.write("Kliknij w komórkę, aby poprawić wagę:")
        st.session_state.macierze[i] = st.data_editor(
            st.session_state.macierze[i], 
            key=f"tabela_{i}", 
            use_container_width=True
        )

# PODSUMOWANIE ZAKRESOWE (DOKŁADNIE JAK W EXCELU)
st.divider()
st.header("📊 PODSUMOWANIE ZAKRESÓW (Wszystkie listy)")

# Łączymy dane ze wszystkich list
df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

summary = pd.DataFrame(index=TYPY)
summary["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
summary["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
summary["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
summary["RAZEM [kg]"] = summary.sum(axis=1)



st.table(summary.style.format("{:.2f}"))

laczna_waga = summary["RAZEM [kg]"].sum()
st.success(f"### WAGA CAŁKOWITA: {laczna_waga:.2f} kg ({laczna_waga/1000:.3f} t)")
