import streamlit as st
import pandas as pd

# Średnice i Typy zgodne z Twoim zakładem we Wrocławiu
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["Proste", "Gięte", "3D"]

st.set_page_config(page_title="Sumator Stali - Wrocław", layout="wide")
st.title("🏗️ System Sumowania Wag Stallist")

# Inicjalizacja macierzy w pamięci sesji
if 'macierze' not in st.session_state:
    st.session_state.macierze = {
        i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)
    }

def dodaj_wage(nr, sr, typ, waga):
    if waga > 0:
        # Dodawanie nowej wagi do tego, co już jest w tabeli
        st.session_state.macierze[nr].at[typ, sr] += round(waga, 2)

total_order_kg = 0

# Generowanie 6 sekcji
for i in range(1, 7):
    suma_listy = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} | Razem: {suma_listy:.2f} kg", expanded=(i==1)):
        
        # Formularz wprowadzania danych
        with st.form(key=f"form_{i}", clear_on_submit=True):
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                sr_in = st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_{i}")
            with c2:
                typ_in = st.selectbox("Typ", TYPY, key=f"t_{i}")
            with c3:
                # WPISUJESZ WAGĘ I NACISKASZ ENTER
                waga_in = st.number_input("Wpisz wagę [kg] i naciśnij ENTER", min_value=0.0, step=0.01, format="%.2f", key=f"w_{i}")
            
            if st.form_submit_button("Dodaj"):
                pass # Formularz i tak się wyśle

            if waga_in > 0:
                dodaj_wage(i, sr_in, typ_in, waga_in)
                st.rerun()

        # Wyświetlanie tabeli (Widok jak w Twoim Excelu)
        st.write("**Podsumowanie wagowe listy [kg]:**")
        df_display = st.session_state.macierze[i].copy()
        
        # Dodanie sumy wiersza
        df_display['SUMA TYPU'] = df_display.sum(axis=1)
        
        # Wyświetlenie tabeli z formatowaniem do 2 miejsc po przecinku
        st.table(df_display.style.format("{:.2f}"))
        
        if st.button(f"🗑️ Wyczyść Listę {i}", key=f"clr_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()
            
    total_order_kg += suma_listy

# --- PODSUMOWANIE ZBIORCZE ---
st.divider()
st.header("📊 Łącznie do produkcji (Wszystkie listy)")
col_kg, col_t = st.columns(2)
col_kg.metric("Suma Całkowita [kg]", f"{total_order_kg:.2f} kg")
col_t.metric("Suma Całkowita [tony]", f"{total_order_kg/1000:.3f} t")
