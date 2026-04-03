import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import math, io
from mathe_utils import lade_marktdaten
import simulationen

# --- UI SETUP ---
st.set_page_config(page_title="Dreikorb Profi v10.5", layout="wide")
st.title("📊 Dreikorb-Strategie Cockpit")

with st.sidebar:
    st.header("🏢 Setup")
    k1_s = st.number_input("K1 Cash", 0.0, value=30000.0)
    k2_s = st.number_input("K2 Anleihen", 0.0, value=30000.0)
    k3_s = st.number_input("K3 Aktien", 0.0, value=520000.0)
    g_s = st.slider("Gewinn %", 0, 100, 30) / 100
    
    st.header("📂 Portfolio-Mix")
    w_msci = st.slider("MSCI World %", 0, 100, 50)
    w_ndx = st.slider("Nasdaq 100 %", 0, 100, 30)
    w_sp = st.slider("S&P 500 %", 0, 100, 20)
    w_dax = st.slider("DAX %", 0, 100, 0)
    
    total_w = w_msci + w_ndx + w_sp + w_dax
    if total_w == 100:
        st.success("✅ Allokation: 100%")
        portfolio_mix = {"URTH": w_msci, "^NDX": w_ndx, "^GSPC": w_sp, "^GDAXI": w_dax}
    elif total_w > 0:
        st.warning(f"⚠️ Normiert auf 100% (Summe war {total_w}%)")
        f = 100.0 / total_w
        portfolio_mix = {"URTH": w_msci*f, "^NDX": w_ndx*f, "^GSPC": w_sp*f, "^GDAXI": w_dax*f}
    else:
        st.error("❗ Bitte Mix wählen.")
        portfolio_mix = {"URTH": 100, "^NDX": 0, "^GSPC": 0, "^GDAXI": 0}

    st.header("💰 Rente")
    alt_j = st.number_input("Alter", 18, 100, 53)
    r_a = st.number_input("Rente A", 0, 10000, value=2500)
    a_a = st.number_input("Bis A", alt_j, 110, 65)
    r_b = st.number_input("Rente B", 0, 10000, value=1100)
    a_b = st.number_input("Bis B", a_a, 110, 95)
    r_std = st.number_input("Standard Rente", 0, 10000, value=2500)
    alt_z = st.number_input("Ziel Alter", a_b, 110, 95)
    
    st.header("🛡️ Puffer & MC")
    k1_j = st.slider("K1 Jahre", 0.5, 3.0, 1.0)
    k2_j = st.slider("K2 Jahre", 1.0, 5.0, 1.0)
    exp_ret = st.slider("Rendite %", 0.0, 15.0, 7.5)
    exp_vol = st.slider("Vola %", 5.0, 40.0, 15.0)
    infl = st.number_input("Inflation %", 0.0, 10.0, 2.0)
    schwelle = st.slider("K3-Schwelle", 0.0, 1.0, 0.5)
    
    # HIER IST DIE NEUE CHECKBOX FÜR DEN SEED
    use_seed = st.checkbox("Zufall einfrieren (Seed)", value=True)
h_df = lade_marktdaten(portfolio_mix)
t1, t2 = st.tabs(["📊 Backtest", "🔮 Monte-Carlo"])

with t1:
    s_jahr = st.number_input("Startjahr", 2000, 2024, 2016)
    
    if not h_df.empty:
        d3, _, dp, _, _ = simulationen.simuliere_historie(h_df, s_jahr, alt_j, k1_s, k2_s, k3_s, r_std, r_a, a_a, r_b, a_b, g_s, infl/100, k1_j, k2_j, schwelle)
        st.metric("Endvermögen", f"{dp['Gesamt'].iloc[-1]:,.0f} €")
        
        chart_data = dp.copy()
        hover = alt.selection_point(fields=['Jahr'], nearest=True, on='mouseover', empty=False)
        base = alt.Chart(chart_data).encode(x='Jahr:O')
        l1 = base.mark_line(color='#1f77b4', strokeWidth=3).encode(y=alt.Y('Gesamt:Q', scale=alt.Scale(zero=False)))
        l2 = base.mark_line(color='#ff7f0e', strokeDash=[5,5]).encode(y='Vollinvest:Q')
        sel = base.mark_point().encode(opacity=alt.value(0), tooltip=[alt.Tooltip('Jahr:O'), alt.Tooltip('Gesamt:Q', format=',.0f'), alt.Tooltip('Vollinvest:Q', format=',.0f')]).add_params(hover)
        st.altair_chart(alt.layer(l1, l2, sel, l1.mark_point().transform_filter(hover)).properties(height=400), use_container_width=True)
        
        st.subheader("📋 Monatliche Detail-Daten")
        st.dataframe(d3.style.format({
            "Rendite Mix": "{:.1f}%", 
            "K1": "{:,.0f} €", "K2": "{:,.0f} €", "K3": "{:,.0f} €", 
            "Gesamt": "{:,.0f} €", "Vollinvest": "{:,.0f} €", 
            "Netto_Rente": "{:,.0f} €", "Brutto_K3": "{:,.0f} €"
        }), height=400)
        
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
            d3_export = d3.round({"Rendite Mix": 1})
            dp_export = dp.round({"Rendite Mix": 1})
            d3_export.to_excel(wr, sheet_name='1_Dreikorb_Details', index=False)
            d3_export[["Jahr","Monat","Rendite Mix","Vollinvest","Netto_Rente"]].to_excel(wr, sheet_name='2_Vollinvest', index=False)
            dp_export.to_excel(wr, sheet_name='3_Vergleich_Jahr', index=False)
        st.download_button("📥 Excel laden", buf.getvalue(), "Dreikorb_Analyse.xlsx")
    else:
        st.error("📉 **Keine Marktdaten empfangen!**")
        st.warning("Yahoo Finance hat die Verbindung kurzzeitig blockiert. Das passiert oft, wenn Slider zu schnell gezogen werden (Spamschutz).\n\n👉 **Lösung:** Warte ca. 5-10 Sekunden und verändere einen Slider noch einmal leicht, um die Daten neu zu laden.")

with t2:
    if st.button("🚀 Start Monte Carlo", use_container_width=True):
        res, rate = simulationen.run_monte_carlo(100, alt_j, alt_z, k1_s, k2_s, k3_s, r_std, r_a, a_a, r_b, a_b, g_s, exp_ret, exp_vol, infl, k1_j, k2_j, schwelle, seed=use_seed)
        st.subheader(f"Erfolgsquote: {rate:.1%}")
        x = np.linspace(alt_j, alt_z, res.shape[1])
        df_mc = pd.DataFrame({"Alter": x, "Median": np.median(res, axis=0), "P10": np.percentile(res, 10, axis=0), "P90": np.percentile(res, 90, axis=0)})
        c_mc = alt.Chart(df_mc).encode(x='Alter:Q')
        st.altair_chart((c_mc.mark_area(opacity=0.3, color='lightblue').encode(y='P10:Q', y2='P90:Q') + c_mc.mark_line(color='blue').encode(y='Median:Q')).properties(height=400), use_container_width=True)
        
    if st.button("💡 Maximale Rente"):
        with st.spinner("Rechne..."):
            max_r = simulationen.berechne_swr(100, alt_j, alt_z, k1_s, k2_s, k3_s, g_s, exp_ret, exp_vol, infl, k1_j, k2_j, schwelle, seed=use_seed)
            st.success(f"Max. sichere Rente: {max_r} € / Monat")

st.divider()
try:
    with open("README.md", "r", encoding="utf-8") as f: st.markdown(f.read())
except FileNotFoundError: st.warning("README.md fehlt.")
