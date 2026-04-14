# 📘 Handbuch: Dreikorb-Strategie Profi v12.0

Dieses Cockpit ist ein hochpräzises Simulationswerkzeug für die Entnahmephase komplexer Depots. Es kombiniert historische Marktdaten mit stochastischen Zukunftsprognosen (Monte Carlo) und einem modernen Dashboard-Layout.

---

## 1. Die Korb-Architektur
Die Strategie basiert auf einer dynamischen Drei-Säulen-Struktur, die Sicherheit und Rendite kombiniert:

* **1.1. Korb 1 (Cash):** Sofort verfügbare Liquidität. Verzinsung: 1,5% p.a.
* **1.2. Korb 2 (Anleihen/Festgeld):** Sicherheits-Reserve. Verzinsung: 3,0% p.a.
* **1.3. Korb 3 (Aktien-Portfolio):** Frei konfigurierbarer Mix aus Nasdaq 100, S&P 500, Russell 2000 und DAX.

---

## 2. Kern-Features & Bedienung

### 2.1. Dashboard-Header & Setup
Alle Steuerungselemente befinden sich übersichtlich in vier Spalten am oberen Bildschirmrand. 
* **Schrittweiten:** Portfolio-Mix-Slider lassen sich in 5%-Schritten justieren. Die Startwerte der Körbe (K1-K3) lassen sich komfortabel in 5.000 €-Schritten anpassen.

### 2.2. Mitatmende Steuer-Logik & Dynamischer Kaufwert
Das System schätzt Steuern nicht pauschal, sondern führt im Hintergrund ein exaktes Kassenbuch über deinen steuerfreien **Kaufwert** (das ursprünglich investierte Grundkapital). Dabei werden die 25% Kapitalertragsteuer (+Soli) sowie die 30% Teilfreistellung für Aktienfonds berücksichtigt.
* **Der Start:** Über den Slider "Gewinn %" definierst du den initialen Gewinnanteil deines Depots.
* **Dynamische Kursgewinne:** Wächst dein Depot in der Simulation durch Börsen-Rallyes an, steigt automatisch auch der prozentuale Gewinnanteil in deinem Portfolio (z. B. auf 60 % oder 80 %). Die berechnete Steuerlast *atmet* realistisch mit deinen Depotkursen mit.
* **Die Entnahme:** Bei jedem Verkauf berechnet das System deinen aktuellen Gewinnanteil und entnimmt exakt so viel Brutto, wie nötig ist. Der verkaufte Anteil des Grundkapitals wird sauber vom Kaufwert abgezogen.

### 2.3. Inflations-Management
Alle Rentenphasen sowie die Ziel-Limits der Sicherheitskörbe (K1/K2) werden monatlich an die gewählte Inflationsrate angepasst, um die reale Kaufkraft zu erhalten.

### 2.4. Automatisches Rebalancing (Die Puffer-Slider)
Über die Slider "K1 Jahre" und "K2 Jahre" steuerst du, wie groß deine Sicherheitsnetze in *Jahresausgaben* sein sollen.
* **Gewinne ernten:** Befindet sich der Markt im Normal-Modus, prüft das System jeden Monat, ob K1 oder K2 unter ihr Ziel-Limit gefallen sind.
* **Auffüllen:** Fehlt Geld in den Puffern, verkauft das System in guten Börsenzeiten automatisch zusätzliche Aktienanteile aus Korb 3, um K1 und K2 wieder bis zum Rand aufzufüllen. So gehst du immer mit maximal gefüllten Puffern in den nächsten Crash.

---

## 3. Krisen-Modus: Die Drawdown-Regel

Das Tool entscheidet **jeden Monat neu**, ob Korb 3 "gesund" genug für eine Entnahme ist oder ob zum Schutz der Substanz auf die Puffer (K1/K2) zugegriffen werden muss. Der Krisen-Modus basiert auf der **Drawdown-Toleranz**. 

Das System merkt sich für den gesamten Simulationsverlauf das bisherige **Allzeithoch (ATH)** deines Aktien-Depots. Liegt der aktuelle Korb-3-Wert um mehr als die eingestellte Drawdown-Toleranz % unter dem ATH, wird der Krisen-Modus aktiviert:

* **3.1. Szenario A (Normal):** Die Rente wird aus Korb 3 entnommen. Puffer werden bei Bedarf aufgefüllt.
* **3.2. Szenario B (Krise):** Korb 3 wird sofort eingefroren (keine Aktienverkäufe im Tief). Die Rente wird aus dem Cash-Bestand (K1) oder den Anleihen (K2) gedeckt.

---

## 4. Simulations-Module

### 4.1. Backtest Historie
Ermöglicht den optischen Stresstest durch echte historische Krisen.
* **Die Lupe:** Das eingegebene Startjahr dient lediglich der optischen Eingrenzung für den Chart, damit du dir gezielt bestimmte Epochen (z. B. ab 2008 oder ab 2016) im Detail ansehen kannst.
* **Die Performance:** Das Tool berechnet dir automatisch die echte, zeitgewichtete Rendite (CAGR p.a.) deines Dreikorb-Mixes, völlig unabhängig von den entnommenen Rentenbeträgen.
* **Ansicht:** Zeigt die Dreikorb-Strategie (Blau) im direkten Vergleich zu einem 100% Aktien-Vollinvest-Szenario (Orange).

### 4.2. Die Monte-Carlo-Simulation (Multiversum)
Während der historische Backtest die Vergangenheit zeigt, wirft die Monte-Carlo-Simulation einen Blick in die Zukunft. Das System erschafft ein Multiversum aus bis zu 5.000 verschiedenen Lebensläufen.

* **4.2.1. Daten-Basis:** Wähle zwischen *Historisch* (Bootstrapping: Zieht zufällige, echte historische Monatsrenditen inkl. aller echten Crashs) oder *Mathematisch* (Normalverteilung: Zieht Werte basierend auf einer fiktiven Glockenkurve).
* **4.2.2. Der Einzel-Durchlauf:** Ein Durchlauf repräsentiert einen kompletten Lebenspfad (z. B. 42 Jahre = 504 Monate). Für jeden Monat werden Marktschwankung, Inflation, Krisen-Check, Steuern und Rebalancing exakt berechnet.
* **4.2.3. Die Gesamtauswertung:** Das System sammelt alle 5.000 Läufe und ermittelt die Erfolgsquote (z. B. 98,5 %), den Median-Verlauf (wahrscheinlichste Zukunft) und den P10/P90-Schlauch (Worst-/Best-Case).
* **4.2.4. SWR-Rechner (Maximale Rente):** Das System sucht vollautomatisch genau den Euro-Betrag für deine Rente, bei dem die Erfolgsquote am Ende bei punktgenau 95 % liegt.

### 4.3. Der Optimizer (Der Autopilot für dein Setup)
Dieses Modul beantwortet die Frage: *"Wie muss ich mein aktuelles Gesamtkapital heute aufteilen, um die mathematisch höchste Überlebenswahrscheinlichkeit zu erreichen?"*

* **Was er macht:** Der Optimizer testet vollautomatisch 30 verschiedene Puffer-Strategien für dein Gesamtkapital durch (von 0,5 bis 3 Jahren Cash und 0 bis 5 Jahren Anleihen). Für jede Kombination feuert er ein eigenes, schnelles Multiversum (250 Loops) ab.
* **Die Daten-Wahrheit:** Der Optimizer ignoriert das manuell gewählte Startjahr aus dem Backtest. Er greift für seine Simulationen immer auf die *gesamte Historie* (bis zurück nach 1927) zu, um sicherzustellen, dass dein Setup echte Jahrhundert-Crashs überlebt.
* **Das Ergebnis & Die Anwendung:** Du erhältst eine Top-5-Rangliste. Nimm das Setup auf Platz 1, trage die empfohlenen Jahre in die Puffer-Slider ("K1 Jahre", "K2 Jahre") ein und übernimm die Start-Euro-Beträge. Dein System ist nun perfekt ausbalanciert.

---

## 5. Daten-Export

### 5.1. Excel-Export
Der Export-Button im Backtest-Tab liefert detaillierte monatliche Daten (inkl. aller Kontostände, Entnahmen, Steuern und Rebalancing-Aktionen) für deine persönliche Archivierung und tiefergehende Analysen in Excel.
