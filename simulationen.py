import pandas as pd
import numpy as np
import math

def berechne_brutto_und_steuer(netto, gewinn_pct):
    eff_steuer = 0.26375 * 0.7 
    brutto = netto / (1 - (gewinn_pct * eff_steuer))
    return brutto, brutto - netto

def get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, infl_m):
    akt_alt = alt_s + (m / 12)
    # Fallback-Logik: Wenn Rente A oder B auf 0 stehen, wird die Standardrente genutzt
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
    k_voll, g_akt = (k1 + k2 + k3), g_s
    df_slice = df[df['Jahr'] >= s_jahr].copy()
    
    for m, (_, row) in enumerate(df_slice.iterrows()):
        n_b = get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, infl_m)
        k1_lim, k2_lim = n_b * k1_j * 12, n_b * k2_j * 12
        rendite = row['Rendite_Monat']
        
        k3 *= (1 + rendite); k_voll *= (1 + rendite)
        b_v, _ = berechne_brutto_und_steuer(n_b, g_akt); k_voll -= b_v
        
        if rendite > 0:
            g_akt = (((k3/(1+rendite))*g_akt) + (k3 - k3/(1+rendite))) / k3 if k3 > 0 else 0
        
        b_k3_ges = 0
        if (k3 * g_akt) > (n_b * 12 * schwelle) and k3 > 0:
            status = "Normal"
            b_r, _ = berechne_brutto_und_steuer(n_b, g_akt); k3 -= b_r; b_k3_ges += b_r
            if k1 < k1_lim:
                diff = k1_lim - k1
                b_ref, _ = berechne_brutto_und_steuer(diff, g_akt)
                if k3 > b_ref: k3 -= b_ref; k1 += diff; b_k3_ges += b_ref
            if k2 < k2_lim:
                diff = k2_lim - k2
                b_ref, _ = berechne_brutto_und_steuer(diff, g_akt)
                if k3 > b_ref: k3 -= b_ref; k2 += diff; b_k3_ges += b_ref
        else:
            status = "Krise"
            rem = n_b
            if k1 >= rem: k1 -= rem
            else:
                rem -= k1; k1 = 0
                if k2 >= rem: k2 -= rem
                else: b_n, _ = berechne_brutto_und_steuer(rem-k2, g_akt); k3 -= b_n; k2 = 0
                
        k1 *= (1.015**(1/12)); k2 *= (1.030**(1/12))
        
        results.append({
            "Jahr": int(row['Jahr']), 
            "Monat": int(row['Monat']), 
            "Rendite Mix": rendite * 100, 
            "K1": math.ceil(k1), 
            "K2": math.ceil(k2), 
            "K3": math.ceil(k3), 
            "Gesamt": math.ceil(k1+k2+k3), 
            "Vollinvest": math.ceil(k_voll), 
            "Netto_Rente": math.ceil(n_b), 
            "Brutto_K3": math.ceil(b_k3_ges), 
            "Status": status
        })
        
    res_df = pd.DataFrame(results)
    return res_df, None, res_df.groupby("Jahr").last().reset_index(), None, None

def run_monte_carlo(n, alt_s, alt_z, k1_s, k2_s, k3_s, r_std, r_a, alt_a, r_b, alt_b, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed=True):
    if seed: np.random.seed(42)
    monate = int((alt_z - alt_s) * 12)
    results = np.zeros((n, monate))
    inf_m, mu_m, sig_m = (1+infl/100)**(1/12)-1, (1+ret/100)**(1/12)-1, (vol/100)/np.sqrt(12)
    success = 0
    for i in range(n):
        k1, k2, k3, g_akt, alive = k1_s, k2_s, k3_s, g_s, True
        for m in range(monate):
            r = np.random.normal(mu_m, sig_m); k3 *= (1+r)
            if r > 0: g_akt = (((k3/(1+r))*g_akt) + (k3-k3/(1+r)))/k3 if k3 > 0 else 0
            n_b = get_monatliche_rente(m, alt_s, r_std, r_a, alt_a, r_b, alt_b, inf_m)
            if (k3*g_akt) > (n_b*12*schwelle) and k3 > 0: k3 -= berechne_brutto_und_steuer(n_b, g_akt)[0]
            else:
                rem = n_b
                if k1 >= rem: k1 -= rem
                else:
                    rem -= k1; k1 = 0
                    if k2 >= rem: k2 -= rem
                    else: k3 -= berechne_brutto_und_steuer(rem-k2, g_akt)[0]; k2 = 0
            k1 *= (1.015**(1/12)); k2 *= (1.03**(1/12))
            results[i,m] = k1+k2+k3
            if results[i,m] <= 0: alive = False; break
        if alive: success += 1
    return results, success/n

def berechne_swr(n, alt_s, alt_z, k1_s, k2_s, k3_s, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed=True):
    low, high, best = 0, 20000, 0
    for _ in range(12):
        mid = (low + high) / 2
        _, rate = run_monte_carlo(n, alt_s, alt_z, k1_s, k2_s, k3_s, mid, mid, alt_s, mid, alt_s, g_s, ret, vol, infl, k1_j, k2_j, schwelle, seed)
        if rate >= 0.95: best, low = mid, mid
        else: high = mid
    return int(best)