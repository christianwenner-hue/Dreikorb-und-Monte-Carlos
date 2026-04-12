import pandas as pd
import yfinance as yf
import time
import streamlit as st

@st.cache_data(ttl=3600) # Speichert die Daten für 1 Stunde im Cache
def lade_marktdaten(portfolio_mix, max_retries=3):
    # 1. Filtere alle Ticker raus, die 0% Gewichtung haben
    aktive_ticker = {ticker: weight/100.0 for ticker, weight in portfolio_mix.items() if weight > 0}
    
    if not aktive_ticker:
        return pd.DataFrame()

    tickers_list = list(aktive_ticker.keys())
    
    # 2. Der Retry-Loop: Bis zu 3 Versuche, falls Yahoo zickt
    for versuch in range(max_retries):
        try:
            # Lade historische Monats-Daten (so weit zurück wie möglich)
            df_raw = yf.download(tickers_list, start="1927-01-01", interval="1mo", progress=False)
            
            # Prüfe, ob Daten überhaupt geladen wurden
            if df_raw.empty:
                raise ValueError("Yahoo hat einen leeren Datensatz zurückgegeben.")
                
            # Extrahiere die angepassten Schlusskurse (inkl. Dividenden, falls vorhanden)
            if 'Adj Close' in df_raw.columns:
                df_close = df_raw['Adj Close']
            elif 'Close' in df_raw.columns:
                df_close = df_raw['Close']
            else:
                df_close = df_raw

            # Falls nur ein Ticker (100%) gewählt wurde, wandle Series in DataFrame um
            if isinstance(df_close, pd.Series):
                df_close = df_close.to_frame(tickers_list[0])

            # Monatsrenditen pro Index berechnen (prozentuale Änderung)
            df_returns = df_close.pct_change().dropna()

            # Gewichtete Portfolio-Rendite berechnen
            portfolio_return = pd.Series(0.0, index=df_returns.index)
            for ticker, weight in aktive_ticker.items():
                if ticker in df_returns.columns:
                    portfolio_return += df_returns[ticker] * weight

            # Finale Tabelle exakt so formatieren, wie simulationen.py sie erwartet
            h_df = pd.DataFrame({
                'Jahr': portfolio_return.index.year,
                'Monat': portfolio_return.index.month,
                'Rendite_Monat': portfolio_return.values
            })
            
            return h_df

        except Exception as e:
            if versuch < max_retries - 1:
                time.sleep(2) # 2 Sekunden warten und nochmal versuchen
            else:
                # Nach 3 Versuchen aufgeben -> Gibt leeren DataFrame zurück (Fallback springt ein)
                return pd.DataFrame()
