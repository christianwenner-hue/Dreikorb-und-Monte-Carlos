import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import math, io
from mathe_utils import lade_marktdaten
import simulationen

# --- UI SETUP ---
st.set_page_config(page_title="Dreikorb Profi v10.9", layout="wide")
st.title("📊 Dreikorb-Strategie Cockpit")

# --- HEADER LAYOUT (4 SPALTEN) ---
c_setup, c_mix, c_rente, c_mc = st.columns(4)

with c_setup:
    st.subheader("🏢 Setup")
    k1_s = st.number_input("K1 Cash", 0.0, value=30000.0, step=5000.0)
    k2_s = st.number_input("K2 Anleihen", 0.0, value=30000.0, step=5000.0)
    k3_s = st.number_input("K3 Aktien", 0.0, value=520000.0, step=5000.0)
    g_s = st.slider("Gewinn %", 0, 100, 30) / 100

with c_mix:
    st.subheader("📂 Portfolio-Mix")
    w_ndx = st.slider("Nasdaq 100 %", 0, 100, 25, step=5)
    w_sp = st.slider("S&P 500 %", 0, 100, 25, step=5)
    w_rut = st.slider("Russell 2000 %", 0, 100, 50, step=5)
    w_dax = st.slider("DAX %", 0, 100, 0, step=5)
    
    total_w = w_ndx + w_sp + w_rut + w_dax
    if total_w == 100:
        st.success("✅ Allokation: 100%")
        portfolio_mix = {"^NDX": w_ndx, "^GSPC": w_sp, "^RUT": w_rut, "^GDAXI": w_dax}
    elif total_w > 0:
        st.warning(f"⚠️ Normiert auf 100% (Summe war {total_w}%)")
        f = 100.0 / total_w
        portfolio_mix = {"^NDX": w_ndx*f, "^GSPC": w_sp*f, "^RUT": w_rut*f, "^GDAXI": w_dax*f}
    else:
        st.error("❗ Bitte Mix wählen.")
        portfolio_mix = {"^NDX": 25, "^GSPC": 25, "^RUT": 50, "^GDAXI": 0}

with c_rente:
    st.subheader("💰 Rente")
    alt_j = st.number_input("Alter", 18, 100, 53)
    r_a = st.number_input("Rente A", 0, 10000, value=2500)
    a_a = st.number_input("Bis A", alt_j, 110, 65)
    r_b = st.number_input("Rente B", 0, 10000, value=1100)
    a_b = st.number_input("Bis B", a_a, 110, 95)
    r_std = st.number_input("Standard Rente", 0, 10000, value=2500)
    alt_z = st.number_input("Ziel Alter", a_b, 110, 95)
with c_mc:
    st.subheader("🛡️ Puffer & MC")
    k1_j = st.slider("K1 Jahre", 0.5, 3.0, 1.0)
    k2_j = st.slider("K2 Jahre", 1.0, 5.0, 1.0)
    exp_ret = st.slider("Rendite %", 0.0, 15.0, 7.5)
    exp_vol = st.slider("Vola %", 5.0, 40.0, 15.0)
    infl = st.number_input("Inflation %", 0.0, 10.0, 2.0)
    schwelle = st.slider("Drawdown Toleranz %", 0, 50, 10) / 100.0
    n_sim = st.slider("Anzahl Simulationen (Loops)", 100, 5000, 1000, step=100)
    mc_methode_ui = st.radio("MC Daten-Basis", ["Mathematisch (Normalverteilung)", "Historisch (Bootstrapping)"])
    use_seed = st.checkbox("Zufall einfrieren (Seed)", value=True)

st.divider() # Optische Trennung zwischen Header und Charts

h_df = lade_marktdaten(portfolio_mix)
t1, t2 = st.tabs(["📊 Backtest", "🔮 Monte-Carlo"])

with t1:
    s_jahr = st.number_input("Startjahr", 2000, 2024, 2016)
    if not h_df.empty:
        d3, _, dp, _, _ = simulationen.simuliere_historie(h_df, s_jahr, alt_j, k1_s, k2_s, k3_s, r_std, r_a, a_a, r_b, a_b, g_s, infl/100, k1_j, k2_j, schwelle)
        
        end_val_bt = int(dp['Gesamt'].iloc[-1])
        st.metric("Endvermögen", f"{end_val_bt:,}".replace(",", ".") + " €")
        
        chart_data = dp.copy()
        hover = alt.selection_point(fields=['Jahr'], nearest=True, on='mouseover', empty=False)
        base = alt.Chart(chart_data).encode(x='Jahr:O')
        l1 = base.mark_line(color='#1f77b4', strokeWidth=3).encode(y=alt.Y('Gesamt:Q', scale=alt.Scale(zero=False)))
        l2 = base.mark_line(color='#ff7f0e', strokeDash=[5,5]).encode(y='Vollinvest:Q')
        
        sel = base.mark_point().encode(
            opacity=alt.value(0), 
            tooltip=[
                alt.Tooltip('Jahr:O', title='Jahr'), 
                alt.Tooltip('Status:N', title='Phase'),
                alt.Tooltip('Brutto_Entnahme:Q', format=',.0f', title='Reale Entnahme Brutto (M) €'),
                alt.Tooltip('Netto_Rente:Q', format=',.0f', title='Ziel-Rente Netto (M) €'),
                alt.Tooltip('Gesamt:Q', format=',.0f', title='Dreikorb (Gesamt) €'), 
                alt.Tooltip('Vollinvest:Q', format=',.0f', title='Vollinvest €')
            ]
        ).add_params(hover)
        
        st.altair_chart(alt.layer(l1, l2, sel, l1.mark_point().transform_filter(hover)).properties(height=400), use_container_width=True)
        
        st.subheader("📋 Monatliche Detail-Daten")
        st.dataframe(d3.style.format({
            "Rendite Mix": "{:.1f}%", 
            "K1": "{:,.0f} €", "K2": "{:,.0f} €", "K3": "{:,.0f} €", 
            "Gesamt": "{:,.0f} €", "Vollinvest": "{:,.0f} €", 
            "Netto_Rente": "{:,.0f} €", "Brutto_Entnahme": "{:,.0f} €"
        }), height=400)
        
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
            d3.to_excel(wr, sheet_name='1_Dreikorb_Details', index=False)
            dp.to_excel(wr, sheet_name='2_Vergleich_Jahr', index=False)
        st.download_button("📥 Excel laden", buf.getvalue(), "Dreikorb_Analyse.xlsx")
    else:
        st.error("📉 Keine Marktdaten.")
with t2:
    methode_param = "math" if "Mathematisch" in mc_methode_ui else "hist"
    
    # NEU: Transparente Warnung, falls Fallback greift
    if methode_param == "hist" and h_df.empty:
        st.warning("⚠️ Yahoo Finance liefert aktuell keine Daten. Das System nutzt als Fallback die mathematische Normalverteilung.")
        
    if st.button("🚀 Start Monte Carlo", use_container_width=True):
        res, res_brutto, rate = simulationen.run_monte_carlo(n_sim, alt_j, alt_z, k1_s, k2_s, k3_s, r_std, r_a, a_a, r_b, a_b, g_s, exp_ret, exp_vol, infl, k1_j, k2_j, schwelle, seed=use_seed, method=methode_param, h_df=h_df)
        
        monate = res.shape[1]
        x = np.linspace(alt_j, alt_z, monate)
        inf_m = (1 + infl / 100)**(1/12) - 1
        renten_netto = [simulationen.get_monatliche_rente(m, alt_j, r_std, r_a, a_a, r_b, a_b, inf_m) for m in range(monate)]
        
        df_mc = pd.DataFrame({
            "Alter": x, 
            "Median": np.median(res, axis=0), 
            "P10": np.percentile(res, 10, axis=0), 
            "P90": np.percentile(res, 90, axis=0),
            "Entnahme_Netto": renten_netto, 
            "Entnahme_Brutto_Median": np.median(res_brutto, axis=0) 
        })
        
        c1, c2 = st.columns(2)
        c1.metric("Erfolgsquote", f"{rate:.1%}")
        end_val_mc = int(df_mc['Median'].iloc[-1])
        c2.metric("Median Endvermögen", f"{end_val_mc:,}".replace(",", ".") + " €")
        
        c_mc = alt.Chart(df_mc).encode(x=alt.X('Alter:Q', title='Alter'))
        area = c_mc.mark_area(opacity=0.3, color='lightblue').encode(y='P10:Q', y2='P90:Q', tooltip=alt.value(None))
        line = c_mc.mark_line(color='blue', size=3).encode(
            y='Median:Q',
            tooltip=[
                alt.Tooltip('Alter:Q', format='.0f', title='Alter'),
                alt.Tooltip('Entnahme_Brutto_Median:Q', format=',.0f', title='Reale Entnahme Brutto (Median) €'),
                alt.Tooltip('Entnahme_Netto:Q', format=',.0f', title='Ziel-Rente Netto (M) €'),
                alt.Tooltip('Median:Q', format=',.0f', title='Median €'),
                alt.Tooltip('P10:Q', format=',.0f', title='P10 €'),
                alt.Tooltip('P90:Q', format=',.0f', title='P90 €')
            ]
        )
        st.altair_chart((area + line).properties(height=400), use_container_width=True)
        
    if st.button("💡 Maximale Rente"):
        with st.spinner("Rechne..."):
            max_r = simulationen.berechne_swr(n_sim, alt_j, alt_z, k1_s, k2_s, k3_s, g_s, exp_ret, exp_vol, infl, k1_j, k2_j, schwelle, seed=use_seed, method=methode_param, h_df=h_df)
            st.success(f"Max. sichere Rente: {int(max_r):,}".replace(",", ".") + " € / Monat")

st.divider()
try:
    with open("README.md", "r", encoding="utf-8") as f: st.markdown(f.read())
except FileNotFoundError: st.warning("README.md fehlt.")
