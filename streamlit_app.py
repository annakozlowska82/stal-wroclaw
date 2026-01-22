import streamlit as st
import pandas as pd

# Ustawienia średnic i typów
SREDNICE = [6, 8, 10, 12, 14, 16, 20, 25, 28, 32]
TYPY = ["proste", "gięte", "3D"]

st.set_page_config(page_title="Sumator Zbrojenia Wrocław", layout="wide")
st.title("🏗️ Szybki Sumator Stallist (Wagi kg)")

# Inicjalizacja baz danych w pamięci sesji
if 'macierze' not in st.session_state:
    st.session_state.macierze = {i: pd.DataFrame(0.0, index=TYPY, columns=SREDNICE) for i in range(1, 7)}

# FUNKCJA CALLBACK - wykonuje się po naciśnięciu ENTER
def przetworz_enter(nr_listy):
    klucz_wagi = f"waga_v_{nr_listy}"
    waga_do_dodania = st.session_state[klucz_wagi]
    
    if waga_do_dodania > 0:
        sr = st.session_state[f"sr_v_{nr_listy}"]
        tp = st.session_state[f"tp_v_{nr_listy}"]
        
        # Dodanie wagi do odpowiedniej komórki
        st.session_state.macierze[nr_listy].at[tp, sr] += round(waga_do_dodania, 2)
        
        # Resetowanie pola wpisywania do zera
        st.session_state[klucz_wagi] = 0.0

# WYŚWIETLANIE 6 SEKCJI
for i in range(1, 7):
    suma_listy = st.session_state.macierze[i].values.sum()
    with st.expander(f"📋 STALLISTA NR {i} (Suma: {suma_listy:.2f} kg)", expanded=(i==1)):
        
        # UI do wpisywania - brak kontenera FORM = brak przycisku
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.selectbox("Średnica [mm]", SREDNICE, key=f"sr_v_{i}")
        with c2:
            st.selectbox("Typ obróbki", TYPY, key=f"tp_v_{i}")
        with c3:
            # on_change wywołuje funkcję natychmiast po Enterze
            st.number_input("Wpisz wagę i naciśnij ENTER", 
                           min_value=0.0, step=0.01, format="%.2f", 
                           key=f"waga_v_{i}", 
                           on_change=przetworz_enter, args=(i,))

        # EDYTOWALNA TABELA - tutaj klikasz, żeby poprawić błąd
        st.write("Podgląd tabeli (kliknij komórkę, aby edytować):")
        st.session_state.macierze[i] = st.data_editor(
            st.session_state.macierze[i],
            key=f"tabela_v_{i}",
            use_container_width=True
        )
        
        if st.button(f"Wyczyść listę {i}", key=f"clear_v_{i}"):
            st.session_state.macierze[i] = pd.DataFrame(0.0, index=TYPY, columns=SREDNICE)
            st.rerun()

# --- PODSUMOWANIE ZBIORCZE NA DOLE STRONY ---
st.divider()
st.header("📊 ZBIORCZE PODSUMOWANIE (Wszystkie Listy)")

# Sumowanie wszystkich 6 macierzy
df_total = pd.concat(st.session_state.macierze.values()).groupby(level=0).sum()

# Grupowanie zakresowe zgodnie z Twoim Excelem
podsumowanie_zakresy = pd.DataFrame(index=TYPY)
podsumowanie_zakresy["#6 - #8"] = df_total[[6, 8]].sum(axis=1)
podsumowanie_zakresy["#10 - #12"] = df_total[[10, 12]].sum(axis=1)
podsumowanie_zakresy["#14 - #32"] = df_total[[14, 16, 20, 25, 28, 32]].sum(axis=1)
podsumowanie_zakresy["SUMA [kg]"] = podsumowanie_zakresy.sum(axis=1)



st.table(podsumowanie_zakresy.style.format("{:.2f}"))

lacznie = podsumowanie_zakresy["SUMA [kg]"].sum()
st.success(f"### WAGA ŁĄCZNA ZAMÓWIENIA: {lacznie:.2f} kg ({lacznie/1000:.3f} t)")
