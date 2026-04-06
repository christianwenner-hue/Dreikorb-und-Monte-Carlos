import pandas as pd
import yfinance as yf
import math
import streamlit as st

def berechne_brutto_und_steuer(netto_ziel, gewinn_anteil, ist_etf=True):
    if netto_ziel <= 0: return 0, 0
    st_satz = 0.26375 
    eff_st_pro_euro = st_satz * (0.70 if ist_etf else 1.0) * gewinn_anteil
    eff_st_pro_euro = min(eff_st_pro_euro, 0.8)
    brutto = netto_ziel / (1 - eff_st_pro_euro)
    brutto_int = math.ceil(brutto)
    steuer_int = brutto_int - math.ceil(netto_ziel)
    return brutto_int, steuer_int

@st.cache_data(show_spinner=False, ttl=3600)
def lade_marktdaten(ticker_dict):
    all_data = []
    for ticker, weight in ticker_dict.items():
        if weight <= 0: continue
        try:
            raw = yf.download(ticker, period="max", interval="1mo", progress=False)
            if raw.empty: continue
            
            if 'Close' in raw.columns:
                if isinstance(raw.columns, pd.MultiIndex):
                    price_col = raw['Close'][ticker]
                else:
                    price_col = raw['Close']
            else: continue
            
            ret = price_col.pct_change().dropna()
            if isinstance(ret, pd.DataFrame): ret = ret.iloc[:, 0]
                
            df_ticker = ret.to_frame(name=f"w_ret_{ticker}")
            df_ticker[f"w_ret_{ticker}"] = df_ticker[f"w_ret_{ticker}"] * (weight / 100)
            all_data.append(df_ticker)
        except Exception as e:
            st.error(f"Fehler beim Laden von {ticker}: {e}")

    if not all_data: return pd.DataFrame()
    combined = pd.concat(all_data, axis=1).dropna()
    combined['Rendite_Monat'] = combined.sum(axis=1)
    
    df_final = pd.DataFrame({
        "Datum": combined.index,
        "Jahr": combined.index.year.astype(int),
        "Monat": combined.index.month.astype(int),
        "Rendite_Monat": combined['Rendite_Monat'].values.astype(float)
    })
    return df_final.sort_values(["Jahr", "Monat"])

# --- DIESE FUNKTION HAT GEFEHLT ---
def get_monatliche_rente(m_idx, alter_start, r_std, r_a, alt_a, r_b, alt_b, infl_m):
    aktuelles_alter = alter_start + (m_idx / 12)
    if r_a > 0 and aktuelles_alter < alt_a: 
        basis = r_a
    elif r_b > 0 and aktuelles_alter < alt_b: 
        basis = r_b
    else: 
        basis = r_std
    return math.ceil(basis * (1 + infl_m)**m_idx)
