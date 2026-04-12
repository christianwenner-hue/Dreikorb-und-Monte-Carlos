import pandas as pd
import numpy as np
import math

def berechne_brutto_und_steuer(netto, gewinn_pct):
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
    k3_ath = k3 # Tracker für das Allzeithoch
    
    df_slice = df[df['Jahr'] >= s_jahr].copy()
    
    for m, (_, row) in enumerate(df_slice.iterrows()):
        n_b = get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, infl_m)
        k1_lim, k2_lim = n_b * k1_j * 12, n_b * k2_j * 12
        rendite = row['Rendite_Monat']
        
        k3 *= (1 + rendite)
        k_voll *= (1 + rendite)
        
        if k3 > k3_ath:
            k3_ath = k3
            
        b_v, _ = berechne_brutto_und_steuer(n_b, g_s)
        k_voll -= b_v
        
        brutto_monat = 0
        
        # DRAWDOWN-CHECK: Ist der aktuelle Wert noch innerhalb der Toleranz vom ATH?
        if k3 >= (k3_ath * (1 - schwelle)) and k3 > 0:
            status = "Normal"
            b_r, _ = berechne_brutto_und_steuer(n_b, g_s)
            k3 -= b_r
            brutto_monat = b_r
            
            # Puffer auffüllen, da Normal-Modus
            if k1 < k1_lim:
                diff = k1_lim - k1
                b_ref, _ = berechne_brutto_und_steuer(diff, g_s)
                if k3 > b_ref: k3 -= b_ref; k1 += diff
            if k2 < k2_lim:
                diff = k2_lim - k2
                b_ref, _ = berechne_brutto_und_steuer(diff, g_s)
                if k3 > b_ref: k3 -= b_ref; k2 += diff
        else:
            status = "Krise"
            brutto_monat = n_b # In der Krise wird K1/K2 genutzt (Brutto = Netto)
            rem = n_b
            if k1 >= rem: 
                k1 -= rem
            else:
                rem -= k1
                k1 = 0
                if k2 >= rem: 
                    k2 -= rem
                else: 
                    b_n, _ = berechne_brutto_und_steuer(rem-k2, g_s)
                    k3 -= b_n
                    k2 = 0
                
        k1 *= (1.015**(1/12)); k2 *= (1.030**(1/12))
        
        results.append({
            "Jahr": int(row['Jahr']), 
            "Monat": int(row['Monat']), 
            "Rendite Mix": rendite * 100, 
            "K1": math.ceil(k1), "K2": math.ceil(k2), "K3": math.ceil(k3), 
            "Gesamt": math.ceil(k1+k2+k3), 
            "Vollinvest": math.ceil(k_voll), 
            "Netto_Rente": math.ceil(n_b), 
            "Brutto_Entnahme": math.ceil(brutto_monat), 
            "Status": status
        })
        
    res_df = pd.DataFrame(results)
    return res_df, None, res_df.groupby("Jahr").last().reset_index(), None, None
def run_monte_carlo(n, alt_s, alt_z, k1_s, k2_s, k3_s, r_std, r_a, alt_a, r_b, alt_b, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed=True, method="math", h_df=None):
    if seed: np.random.seed(42)
    monate = int((alt_z - alt_s) * 12)
    results = np.zeros((n, monate))
    results_brutto = np.zeros((n, monate))
    inf_m = (1+infl/100)**(1/12)-1
    
    # SAUBERER FALLBACK: Wenn Daten fehlen, erzwinge Mathe-Modus
    if method == "hist" and h_df is not None and not h_df.empty:
        hist_renditen = h_df['Rendite_Monat'].dropna().values
    else:
        method = "math" 
        mu_m, sig_m = (1+ret/100)**(1/12)-1, (vol/100)/np.sqrt(12)

    success = 0 # Sauberer Erfolgs-Zähler
    for i in range(n):
        k1, k2, k3, alive = k1_s, k2_s, k3_s, True
        k3_ath = k3
        
        for m in range(monate):
            r = np.random.choice(hist_renditen) if method == "hist" else np.random.normal(mu_m, sig_m)
            k3 *= (1+r)
            
            if k3 > k3_ath:
                k3_ath = k3
            
            n_b = get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, inf_m)
            k1_lim, k2_lim = n_b * k1_j * 12, n_b * k2_j * 12
            
            brutto_ist = 0
            if k3 >= (k3_ath * (1 - schwelle)) and k3 > 0: 
                b_r, _ = berechne_brutto_und_steuer(n_b, g_s)
                k3 -= b_r
                brutto_ist = b_r
                
                if k1 < k1_lim:
                    diff = k1_lim - k1
                    b_ref, _ = berechne_brutto_und_steuer(diff, g_s)
                    if k3 > b_ref: k3 -= b_ref; k1 += diff
                if k2 < k2_lim:
                    diff = k2_lim - k2
                    b_ref, _ = berechne_brutto_und_steuer(diff, g_s)
                    if k3 > b_ref: k3 -= b_ref; k2 += diff
            else:
                brutto_ist = n_b
                rem = n_b
                if k1 >= rem: 
                    k1 -= rem
                else:
                    rem -= k1
                    k1 = 0
                    if k2 >= rem: 
                        k2 -= rem
                    else: 
                        b_n, _ = berechne_brutto_und_steuer(rem-k2, g_s)
                        k3 -= b_n
                        k2 = 0
                        
            k1 *= (1.015**(1/12)); k2 *= (1.03**(1/12))
            results[i,m] = k1+k2+k3
            results_brutto[i,m] = brutto_ist
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
