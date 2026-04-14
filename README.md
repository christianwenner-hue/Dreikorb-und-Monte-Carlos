# 📘 Handbuch: Dreikorb-Strategie Profi v12.0

Dieses Cockpit ist ein hochpräzises Simulationswerkzeug für die Entnahmephase komplexer Depots. Es kombiniert historische Marktdaten mit stochastischen Zukunftsprognosen (Monte Carlo) und einem modernen Dashboard-Layout.

## 🏗️ Die Korb-Architektur
Die Strategie basiert auf einer dynamischen Drei-Säulen-Struktur:

1. **Korb 1 (Cash):** Sofort verfügbare Liquidität. Verzinsung: 1,5% p.a.
2. **Korb 2 (Anleihen/Festgeld):** Sicherheits-Reserve. Verzinsung: 3,0% p.a.
3. **Korb 3 (Aktien-Portfolio):** Frei konfigurierbarer Mix aus **Nasdaq 100, S&P 500, Russell 2000 und DAX**.

---

## 🚀 Kern-Features & Bedienung

### 1. Dashboard-Header
Alle Steuerungselemente befinden sich übersichtlich in vier Spalten am oberen Bildschirmrand. 
* **Schrittweiten:** Portfolio-Mix-Slider lassen sich in **5%-Schritten** justieren. Die Startwerte der Körbe (K1-K3) lassen sich komfortabel in **5.000 €-Schritten** anpassen.

### 2. Mitatmende Steuer-Logik & Dynamischer Kaufwert
Das System schätzt Steuern nicht pauschal, sondern führt im Hintergrund ein exaktes Kassenbuch über deinen steuerfreien **Kaufwert** (das ursprünglich investierte Grundkapital). Dabei werden die **25% Kapitalertragsteuer (+Soli)** sowie die **30% Teilfreistellung** für Aktienfonds berücksichtigt.
* **Der Start:** Über den Slider **"Gewinn %"** definierst du den initialen Gewinnanteil deines Depots.
* **Dynamische Kursgewinne:** Wächst dein Depot in der Simulation durch Börsen-Rallyes an, steigt automatisch auch der prozentuale Gewinnanteil in deinem Portfolio (z. B. auf 60 % oder 80 %). Die berechnete Steuerlast *atmet* realistisch mit deinen Depotkursen mit.
* **Die Entnahme:** Bei jedem Verkauf berechnet das System deinen aktuellen Gewinnanteil und entnimmt exakt so viel Brutto, wie nötig ist. Der verkaufte Anteil des Grundkapitals wird sauber vom Kaufwert abgezogen.

### 3. Inflations-Management
Alle Rentenphasen sowie die Ziel-Limits der Sicherheitskörbe (K1/K2) werden monatlich an die gewählte Inflationsrate angepasst, um die reale Kaufkraft zu erhalten.

### 4. 🔄 Automatisches Rebalancing (Die Puffer-Slider)
Über die Slider **"K1 Jahre"** und **"K2 Jahre"** steuerst du, wie groß deine Sicherheitsnetze in *Jahresausgaben* sein sollen.
* **Gewinne ernten:** Befindet sich der Markt im Normal-Modus, prüft das System jeden Monat, ob K1 oder K2 unter ihr Ziel-Limit gefallen sind.
* **Auffüllen:** Fehlt Geld in den Puffern, verkauft das System in guten Börsenzeiten automatisch zusätzliche Aktienanteile aus Korb 3, um K1 und K2 wieder bis zum Rand aufzufüllen. So gehst du immer mit maximal gefüllten Puffern in den nächsten Crash.

---

## 🚦 Krisen-Modus: Die Drawdown-Regel (Detail)

Das Tool entscheidet **jeden Monat neu**, ob Korb 3 "gesund" genug für eine Entnahme ist oder ob zum Schutz der Substanz auf die Puffer (K1/K2) zugegriffen werden muss.

Der Krisen-Modus basiert auf der **Drawdown-Toleranz**. Das System merkt sich für den gesamten Simulationsverlauf das bisherige **Allzeithoch (ATH)** deines Aktien-Depots.
* Liegt der aktuelle Korb-3-Wert um mehr als die eingestellte **Drawdown-Toleranz %** unter dem ATH, wird der Krisen-Modus aktiviert.
* **Szenario A (Normal):** Die Rente wird aus Korb 3 entnommen. Puffer werden bei Bedarf aufgefüllt.
* **Szenario B (Krise):** Korb 3 wird sofort eingefroren (keine Aktienverkäufe im Tief). Die Rente wird aus dem Cash-Bestand (K1) oder den Anleihen (K2) gedeckt.

---

## 📊 Simulations-Module

### 1. Backtest Historie
Ermöglicht den optischen Stresstest durch echte historische Krisen.
* **Die Lupe:** Das eingegebene Startjahr dient lediglich der optischen Eingrenzung für den Chart, damit du dir gezielt bestimmte Epochen (z. B. ab 2008 oder ab 2016) im Detail ansehen kannst.
* **Ansicht:** Zeigt die Dreikorb-Strategie (Blau) im direkten Vergleich zu einem 100% Aktien-Vollinvest-Szenario (Orange).

### 2. Die Monte-Carlo-Simulation (Multiversum)
Berechnet nicht nur eine Zukunft, sondern ein Multiversum aus Tausenden verschiedenen Lebensläufen bis zu deinem Zielalter.
* **Daten-Basis (Historisch vs. Mathematisch):** Zieht entweder zufällige, mathematisch berechnete Renditen (Glockenkurve) oder kombiniert echte, historische Monatsrenditen zufällig neu (*Bootstrapping*).
* **Auswertung:** Liefert die absolute Erfolgsquote, den Median-Verlauf (die wahrscheinlichste Zukunft) sowie einen P10/P90-Schlauch (Worst-Case & Best-Case).
* **SWR-Rechner:** Sucht per Knopfdruck vollautomatisch die exakte monatliche Netto-Rente, mit der du eine Erfolgsquote von exakt 95 % erreichst.

### 3. 🎯 Der Optimizer (Der Autopilot für dein Setup)
Dieses Modul beantwortet die wichtigste Frage: *"Wie muss ich mein aktuelles Gesamtkapital heute aufteilen, um die mathematisch höchste Überlebenswahrscheinlichkeit zu erreichen?"*

* **Was er macht:** Der Optimizer nimmt dein eingegebenes Gesamtkapital (K1 + K2 + K3) und testet vollautomatisch 30 verschiedene Puffer-Strategien durch (von 0,5 bis 3 Jahren Cash und 0 bis 5 Jahren Anleihen). Für jede Kombination feuert er im Hintergrund ein eigenes, schnelles Multiversum (250 Loops) ab.
* **Die absolute Daten-Wahrheit:** Im Gegensatz zum Backtest ignoriert der Optimizer ein manuell gewähltes Startjahr (wie 2016). Er greift für seine Simulationen immer auf die **gesamte, jahrzehntelange Historie der Börse** (bis zurück nach 1927) zu. So wird sichergestellt, dass deine vorgeschlagene Startaufteilung nicht nur in Bullenmärkten funktioniert, sondern echte historische Jahrhundert-Crashs überlebt.
* **Das Ergebnis:** Eine saubere Top-5-Rangliste. Sie zeigt dir die sichersten Setups inkl. der berechneten Start-Euro-Beträge für deine drei Körbe.
* **Die Anwendung:** Nimm das Setup auf Platz 1, trage die empfohlenen Jahre in die Puffer-Slider ("K1 Jahre", "K2 Jahre") ein und übernimm die Euro-Beträge für dein Start-Setup. Dein System ist nun perfekt ausbalanciert.

### 📥 Excel-Export
Der Export im Backtest-Tab liefert detaillierte monatliche Daten für deine persönliche Archivierung und tiefergehende Analysen.
