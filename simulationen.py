import pandas as pd
import numpy as np
import math

def berechne_brutto_und_steuer(netto, gewinn_pct):
    # Berücksichtigt 25% Abgeltungsteuer + Soli (26,375%) 
    # sowie 30% Teilfreistellung für Aktienfonds
    eff_steuer = 0.26375 * 0.7 
    brutto = netto / (1 - (gewinn_pct * eff_steuer))
    return brutto, brutto - netto

def get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, infl_m):
    akt_alt = alt_s + (m / 12)
    if akt_alt < alt_a:
        basis = r_a if r_a > 0 else r_std
    elif akt_alt < alt_b:
        basis = r_b if r_b > 0 else r_std
    else:
        basis = r_std
    return basis * (1 + infl_m)**m
def simuliere_historie(df, s_jahr, alt_s, k1_s, k2_s, k3_s, r_std, r_a, alt_a, r_b, alt_b, g_s, infl_pa, k1_j, k2_j, schwelle):
    results = []
    infl_m = (1 + infl_pa)**(1/12) - 1
    k1, k2, k3 = float(k1_s), float(k2_s), float(k3_s)
    k_voll = (k1 + k2 + k3)
    k3_ath = k3 
    
    # INITIALISIERUNG DES KASSENBUCHS
    kaufwert = k3 * (1 - g_s)
    
    # Tracking für die durchschnittliche Jahresrendite (TWR)
    twr_faktor = 1.0
    monate_count = 0
    
    df_slice = df[df['Jahr'] >= s_jahr].copy()
    
    for m, (_, row) in enumerate(df_slice.iterrows()):
        monate_count += 1
        rendite = row['Rendite_Monat']
        
        # Echte Brutto-Performance des Mixes vor Entnahmen messen
        ges_alt = k1 + k2 + k3
        if ges_alt > 0:
            w1, w2, w3 = k1 / ges_alt, k2 / ges_alt, k3 / ges_alt
            ret_m = w1 * (1.015**(1/12) - 1) + w2 * (1.030**(1/12) - 1) + w3 * rendite
            twr_faktor *= (1 + ret_m)
            
        n_b = get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, infl_m)
        k1_lim, k2_lim = n_b * k1_j * 12, n_b * k2_j * 12
        
        k3 *= (1 + rendite)
        k_voll *= (1 + rendite)
        
        if k3 > k3_ath:
            k3_ath = k3
            
        gewinn_abs = k3 - kaufwert
        g_akt = gewinn_abs / k3 if gewinn_abs > 0 and k3 > 0 else 0
            
        b_v, _ = berechne_brutto_und_steuer(n_b, g_akt)
        k_voll -= b_v
        
        brutto_monat = 0
        
        if k3 >= (k3_ath * (1 - schwelle)) and k3 > 0:
            status = "Normal"
            b_r, _ = berechne_brutto_und_steuer(n_b, g_akt)
            k3 -= b_r
            kaufwert -= b_r * (1 - g_akt) 
            brutto_monat = b_r
            
            if k1 < k1_lim:
                diff = k1_lim - k1
                b_ref, _ = berechne_brutto_und_steuer(diff, g_akt)
                if k3 > b_ref: 
                    k3 -= b_ref
                    kaufwert -= b_ref * (1 - g_akt)
                    k1 += diff
            if k2 < k2_lim:
                diff = k2_lim - k2
                b_ref, _ = berechne_brutto_und_steuer(diff, g_akt)
                if k3 > b_ref: 
                    k3 -= b_ref
                    kaufwert -= b_ref * (1 - g_akt)
                    k2 += diff
        else:
            status = "Krise"
            brutto_monat = n_b 
            rem = n_b
            if k1 >= rem: 
                k1 -= rem
            else:
                rem -= k1
                k1 = 0
                if k2 >= rem: 
                    k2 -= rem
                else: 
                    b_n, _ = berechne_brutto_und_steuer(rem-k2, g_akt)
                    k3 -= b_n
                    kaufwert -= b_n * (1 - g_akt)
                    k2 = 0
                
        k1 *= (1.015**(1/12)); k2 *= (1.030**(1/12))
        
        results.append({
            "Jahr": int(row['Jahr']), "Monat": int(row['Monat']), 
            "Rendite Mix": rendite * 100, "K1": math.ceil(k1), "K2": math.ceil(k2), 
            "K3": math.ceil(k3), "K3 ATH": math.ceil(k3_ath), 
            "Gesamt": math.ceil(k1+k2+k3), "Vollinvest": math.ceil(k_voll), 
            "Netto_Rente": math.ceil(n_b), "Brutto_Entnahme": math.ceil(brutto_monat), "Status": status
        })
        
    res_df = pd.DataFrame(results)
    
    # Durchschnittliche Rendite p.a. (CAGR)
    cagr_pa = (twr_faktor ** (12 / monate_count) - 1) if monate_count > 0 else 0
    
    return res_df, cagr_pa, res_df.groupby("Jahr").last().reset_index(), None, None
def run_monte_carlo(n, alt_s, alt_z, k1_s, k2_s, k3_s, r_std, r_a, alt_a, r_b, alt_b, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed=True, method="math", h_df=None):
    if seed: np.random.seed(42)
    monate = int((alt_z - alt_s) * 12)
    results = np.zeros((n, monate))
    results_brutto = np.zeros((n, monate))
    inf_m = (1+infl/100)**(1/12)-1
    
    if method == "hist" and h_df is not None and not h_df.empty:
        hist_renditen = h_df['Rendite_Monat'].dropna().values
    else:
        method = "math" 
        mu_m, sig_m = (1+ret/100)**(1/12)-1, (vol/100)/np.sqrt(12)

    success = 0 
    for i in range(n):
        k1, k2, k3, alive = k1_s, k2_s, k3_s, True
        k3_ath = k3
        kaufwert = k3 * (1 - g_s)
        
        for m in range(monate):
            r = np.random.choice(hist_renditen) if method == "hist" else np.random.normal(mu_m, sig_m)
            k3 *= (1+r)
            if k3 > k3_ath: k3_ath = k3
            gewinn_abs = k3 - kaufwert
            g_akt = gewinn_abs / k3 if gewinn_abs > 0 and k3 > 0 else 0
            n_b = get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, inf_m)
            k1_lim, k2_lim = n_b * k1_j * 12, n_b * k2_j * 12
            
            if k3 >= (k3_ath * (1 - schwelle)) and k3 > 0: 
                b_r, _ = berechne_brutto_und_steuer(n_b, g_akt)
                k3 -= b_r; kaufwert -= b_r * (1 - g_akt); brutto_ist = b_r
                if k1 < k1_lim:
                    diff = k1_lim - k1; b_ref, _ = berechne_brutto_und_steuer(diff, g_akt)
                    if k3 > b_ref: k3 -= b_ref; kaufwert -= b_ref * (1 - g_akt); k1 += diff
                if k2 < k2_lim:
                    diff = k2_lim - k2; b_ref, _ = berechne_brutto_und_steuer(diff, g_akt)
                    if k3 > b_ref: k3 -= b_ref; kaufwert -= b_ref * (1 - g_akt); k2 += diff
            else:
                brutto_ist = n_b; rem = n_b
                if k1 >= rem: k1 -= rem
                else:
                    rem -= k1; k1 = 0
                    if k2 >= rem: k2 -= rem
                    else: 
                        b_n, _ = berechne_brutto_und_steuer(rem-k2, g_akt)
                        k3 -= b_n; kaufwert -= b_n * (1 - g_akt); k2 = 0
            k1 *= (1.015**(1/12)); k2 *= (1.03**(1/12))
            results[i,m] = k1+k2+k3; results_brutto[i,m] = brutto_ist
            if results[i,m] <= 0: alive = False; break
        if alive: success += 1
    return results, results_brutto, success / n

def berechne_swr(n, alt_s, alt_z, k1_s, k2_s, k3_s, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed=True, method="math", h_df=None):
    low, high, best = 0, 20000, 0
    for _ in range(12):
        mid = (low + high) / 2
        _, _, rate = run_monte_carlo(n, alt_s, alt_z, k1_s, k2_s, k3_s, mid, mid, alt_s, mid, alt_s, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed, method, h_df)
        if rate >= 0.95: best, low = mid, mid
        else: high = mid
    return int(best)

def optimiere_startaufteilung(total_cap, alt_s, alt_z, r_std, r_a, alt_a, r_b, alt_b, g_s, ret, vol, infl, schwelle, seed, method, h_df):
    k1_grid = [0.5, 1.0, 1.5, 2.0, 3.0]
    k2_grid = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    results_opt = []
    inf_m = (1 + infl / 100)**(1/12) - 1
    n_b_start = get_monatliche_rente(0, alt_s, r_std, r_a, alt_a, r_b, alt_b, inf_m)
    jahresrente_netto = n_b_start * 12
    for k1_j in k1_grid:
        for k2_j in k2_grid:
            k1_start = jahresrente_netto * k1_j
            k2_start = jahresrente_netto * k2_j
            k3_start = total_cap - k1_start - k2_start
            if k3_start < total_cap * 0.2: continue 
            res, _, rate = run_monte_carlo(250, alt_s, alt_z, k1_start, k2_start, k3_start, r_std, r_a, alt_a, r_b, alt_b, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed, method, h_df)
            median_end = np.median(res[:, -1])
            results_opt.append({"K1 Puffer": f"{k1_j} J", "K2 Puffer": f"{k2_j} J", "K1 (Start)": k1_start, "K2 (Start)": k2_start, "K3 (Start)": k3_start, "Erfolgsquote": rate, "Median Endwert": median_end})
    return pd.DataFrame(results_opt).sort_values(by=["Erfolgsquote", "Median Endwert"], ascending=[False, False]).reset_index(drop=True)
