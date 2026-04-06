# 📘 Handbuch: Dreikorb-Strategie Profi v10.5

Dieses Cockpit ist ein hochpräzises Simulationswerkzeug für die Entnahmephase komplexer Depots. Es kombiniert historische Marktdaten mit stochastischen Zukunftsprognosen (Monte Carlo).

## 🏗️ Die Korb-Architektur
Die Strategie basiert auf einer dynamischen Drei-Säulen-Struktur:

1.  **Korb 1 (Cash):** Sofort verfügbare Liquidität. Verzinsung: 1,5% p.a.
2.  **Korb 2 (Anleihen/Festgeld):** Sicherheits-Reserve. Verzinsung: 3,0% p.a.
3.  **Korb 3 (Aktien-Portfolio):** Frei konfigurierbarer Mix aus MSCI World, Nasdaq 100, S&P 500 und DAX.

---

## 🚀 Kern-Optimierungen der v10.5

### 1. Dynamische Steuer-Logik (Brutto/Netto)
Das System rechnet nicht mit fiktiven Werten, sondern ermittelt den realen Kapitalbedarf. Es berücksichtigt die **25% Kapitalertragsteuer (+Soli)** sowie die **30% Teilfreistellung** für Aktienfonds. Das Programm berechnet automatisch, wie viel Brutto aus Korb 3 verkauft werden muss, um die gewünschte Netto-Rente auf das Konto zu bringen. Es wird nur der reine *Gewinnanteil* besteuert, nicht das Grundkapital.

### 2. Inflations-Management
Alle Rentenphasen und auch die Ziel-Limits der Sicherheitskörbe (K1/K2) werden monatlich an die gewählte Inflationsrate angepasst. Dein Lebensstandard bleibt somit kaufkraftbereinigt konstant.

### 3. Die 1-Jahr-Startregel
Um massive Steuer-Ausschläge im ersten Monat zu vermeiden, startet die Simulation technisch immer mit einem Puffer von **12 Monaten (1 Jahr)** in K1 und K2. Die Slider in der Sidebar definieren das **Ziel-Level**, welches das System bei den nächsten Marktgewinnen automatisch anstrebt.

---

## 🚦 Krisen-Modus & K3-Schwelle (Detail)

Das Tool entscheidet **jeden Monat neu**, aus welchem Korb die Rente entnommen wird. Dies geschieht durch einen Gesundheits-Check deines Aktienkorbs (Korb 3), um das sogenannte *Sequence of Returns Risk* (Verkauf von Aktien im Tief) zu verhindern.

Das Herzstück ist die **K3-Schwelle**. Sie definiert, wie hoch die reinen *Aktiengewinne* in deinem Depot mindestens sein müssen, bevor das System Korb 3 schützt.

**So funktioniert der monatliche Check:**
1. Der Markt schwankt im aktuellen Monat. Der Wert von Korb 3 und damit dein Aktiengewinn sinkt oder steigt.
2. Das System vergleicht diesen brandaktuellen Gewinn mit deiner Schwelle. 
3. *Formel: Schmerzgrenze = (Gewünschte Jahresrente) × (K3-Schwelle).*

**💡 Ein konkretes Rechenbeispiel:**
* Deine Netto-Rente beträgt 2.500 € pro Monat (entspricht **30.000 € Jahresrente**).
* Du hast die K3-Schwelle auf **0.5** (50%) gestellt.
* Deine Schmerzgrenze liegt somit bei **15.000 €**.

**Szenario A (Normal-Modus):** Die Börse steht gut. Die reinen Gewinne in Korb 3 betragen aktuell 50.000 €. Da dies über der Schmerzgrenze von 15.000 € liegt, wird die Rente normal aus Korb 3 entnommen. Sind K1 oder K2 durch Inflation unter ihr Ziel gefallen, werden sie mit den Gewinnen aus K3 wieder aufgefüllt.

**Szenario B (Krisen-Modus - Das Einfrieren):** Die Börse stürzt ab. Die reinen Gewinne in Korb 3 schmelzen auf nur noch 10.000 € zusammen. Da dies *unter* der Schmerzgrenze liegt, zieht das System die Notbremse:
* Korb 3 wird sofort **eingefroren**. Es werden keine Aktien mehr zu Schleuderpreisen verkauft.
* Die 2.500 € Rente werden nun vom Bar-Puffer (K1) abgebucht.
* Ist K1 leer, greift das System auf die Anleihen (K2) zurück.
* Korb 3 bleibt unangetastet liegen und kann sich erholen. Erst wenn die Gewinne wieder über 15.000 € klettern (oder alle Puffer restlos leer sind), wird Korb 3 wieder "aufgetaut".

---

## 📊 Simulations-Module

### Backtest Historie
Vergleicht die Dreikorb-Strategie mit einem **Vollinvest-Szenario**. 
* **Blau:** Dreikorb-Strategie (mit Puffern).
* **Orange (gestrichelt):** 100% Aktienquote (höheres Risiko, keine Puffer-Logik).

### Monte-Carlo & SWR
### 1. Daten-Basis: Mathematisch vs. Historisch
Du kannst nun in der Seitenleiste zwischen zwei Simulationsmethoden wählen:
* **Mathematisch (Normalverteilung):** Das Standard-Verfahren. Renditen werden anhand der eingestellten erwarteten Rendite und Volatilität (Glockenkurve) zufällig erwürfelt.
* **Historisch (Bootstrapping):** Der Realitäts-Check. Die Simulation greift blind in den Topf der *echten, historischen Monatsrenditen* deines gewählten Portfolio-Mixes und zieht für jeden Zukunftsmonat ein zufälliges "Los" (Ziehen mit Zurücklegen). So werden echte Marktrisiken und extreme Crash-Szenarien ("Fat Tails") realistisch in die Zukunft projiziert.

### 2. Dynamische Simulations-Loops
Die Anzahl der berechneten Zukünfte (Lebenspfade) lässt sich über den Slider **"Anzahl Simulationen (Loops)"** flexibel von 100 bis auf 5.000 erhöhen.
* **Tipp:** 100 Loops eignen sich für blitzschnelle Tests. Für statistisch extrem belastbare Ergebnisse (besonders beim Bootstrapping) solltest du 1.000 bis 5.000 Loops wählen.
* **Hinweis:** Bei 5.000 Loops führt das System über 2 Millionen Einzelberechnungen durch. Die Ladezeit kann dann ein paar Sekunden in Anspruch nehmen.

### 3. Exakte Brutto-Entnahme (Median)
Das System schätzt die Steuern nicht mehr nur pauschal, sondern berechnet in der Monte-Carlo-Simulation für jeden der bis zu 5.000 Lebenspfade in jedem einzelnen Monat die *exakt anfallende Steuer* (basierend auf der Teilfreistellung, dem persönlichen Steuersatz und dem simulierten Depotstand). 
Da sich die Steuerlast je nach simuliertem Börsenverlauf ändert, sammelt das System alle 5.000 Brutto-Werte eines Monats und zeigt dir im Chart den **Median der Brutto-Entnahmen** an. Das bietet die fairste und genaueste Schätzung für den realen monatlichen Kapitalabfluss.

### 4. Transparente und glatte Tooltips
Fährst du mit der Maus über den Monte-Carlo-Chart (blaue Linie), erhältst du sofort einen übersichtlichen Einblick in das jeweilige Lebensjahr:
* **Alter:** In vollen Jahren.
* **Ziel-Rente Netto:** Dein garantierter Auszahlungsbetrag nach Inflation.
* **Reale Entnahme Brutto (Median):** Wie viel Kapital (inkl. Steuern) in einem mittleren Szenario verkauft werden musste, um die Netto-Rente zu decken.
* **Median, P10 & P90:** Das wahrscheinlichste Endvermögen sowie der Worst-Case (10. Perzentil) und Best-Case (90. Perzentil) – durchgehend lesbar auf glatte Euro gerundet.

### 5. Zufall einfrieren (Seed)
Über die Checkbox **"Zufall einfrieren (Seed)"** in der Seitenleiste kannst du die Zufallszahlen fixieren. Ist der Haken gesetzt, liefert die Monte-Carlo-Simulation bei unveränderten Einstellungen immer exakt denselben Chart. Das ist ideal, um die exakten Auswirkungen einzelner Slider (z. B. "K1 Jahre" oder "Gewinnanteil") unverfälscht miteinander zu vergleichen.
* **SWR (Safe Withdrawal Rate):** Berechnet die maximal mögliche Rente, die in 95% aller Fälle bis zum Zielalter ausreicht.

## 📥 Excel-Analyse
Der Profi-Export liefert drei spezialisierte Mappen:
1.  **1_Dreikorb_Details:** Kompletter monatlicher Verlauf inkl. Korb-Ständen, Benchmark-Rendite und Steuer-Abzügen.
2.  **2_Vollinvest:** Der direkte Gegenentwurf zum Vergleich der Strategien.
3.  **3_Vergleich_Jahr:** Kompakte Jahressicht für die langfristige Planung.
