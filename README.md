# 📘 Handbuch: Dreikorb-Strategie Profi v11.0

Dieses Cockpit ist ein hochpräzises Simulationswerkzeug für die Entnahmephase komplexer Depots. Es kombiniert historische Marktdaten mit stochastischen Zukunftsprognosen (Monte Carlo) und einem modernen Dashboard-Layout.

## 🏗️ Die Korb-Architektur
Die Strategie basiert auf einer dynamischen Drei-Säulen-Struktur:

1. **Korb 1 (Cash):** Sofort verfügbare Liquidität. Verzinsung: 1,5% p.a.
2. **Korb 2 (Anleihen/Festgeld):** Sicherheits-Reserve. Verzinsung: 3,0% p.a.
3. **Korb 3 (Aktien-Portfolio):** Frei konfigurierbarer Mix aus **Nasdaq 100, S&P 500, Russell 2000 und DAX**. (MSCI World wurde zugunsten einer längeren historischen Datenhistorie entfernt).

---

## 🚀 Kern-Features & Bedienung

### 1. Dashboard-Header
Alle Steuerungselemente befinden sich nun übersichtlich in vier Spalten am oberen Bildschirmrand. 
* **Schrittweiten:** Portfolio-Mix-Slider lassen sich in **5%-Schritten** justieren. Die Startwerte der Körbe (K1-K3) lassen sich komfortabel in **5.000 €-Schritten** anpassen.

### 2. Dynamische Steuer-Logik (Brutto/Netto)
Das System berücksichtigt die **25% Kapitalertragsteuer (+Soli)** sowie die **30% Teilfreistellung** für Aktienfonds. Über den Slider **"Gewinn %"** definierst du den kalkulatorischen Gewinnanteil deines Depots zum Startzeitpunkt. Das Programm berechnet daraufhin automatisch, wie viel Brutto verkauft werden muss, um deine gewünschte Netto-Rente zu erzielen.

### 3. Inflations-Management
Alle Rentenphasen sowie die Ziel-Limits der Sicherheitskörbe (K1/K2) werden monatlich an die gewählte Inflationsrate angepasst, um die reale Kaufkraft zu erhalten.

### 4. 🔄 Automatisches Rebalancing (Die Puffer-Slider)
Über die Slider **"K1 Jahre"** und **"K2 Jahre"** in der Spalte *Puffer & MC* steuerst du, wie groß deine Sicherheitsnetze sein sollen. Die Werte definieren die Puffer-Größe in *Jahresausgaben* (Beispiel: Bei 30.000 € Jahresrente und "K1 Jahre" auf 1.5 strebt das System einen Cash-Puffer von 45.000 € an).

* **Gewinne ernten:** Befindet sich der Markt im Normal-Modus (Korb 3 ist nahe am Allzeithoch), prüft das System jeden Monat, ob K1 oder K2 unter ihr Ziel-Limit gefallen sind – sei es durch vorherige Krisenentnahmen oder durch die ansteigende Inflation.
* **Auffüllen:** Fehlt Geld in den Puffern, verkauft das System in guten Börsenzeiten automatisch zusätzliche Aktienanteile aus Korb 3 (inklusive exakter Steuerberechnung), um K1 und K2 wieder bis zum Rand aufzufüllen. So gehst du immer mit maximal gefüllten Puffern in den nächsten Crash.

---

## 🚦 Krisen-Modus: Die Drawdown-Regel (Detail)

Das Tool entscheidet **jeden Monat neu**, ob Korb 3 "gesund" genug für eine Entnahme ist oder ob zum Schutz der Substanz auf die Puffer (K1/K2) zugegriffen werden muss.

Der Krisen-Modus basiert auf der **Drawdown-Toleranz**. Das System merkt sich für den gesamten Simulationsverlauf den jeweils höchsten erreichten Stand deines Aktien-Depots (**Allzeithoch / ATH**).

**So funktioniert der monatliche Check:**
1. Das System prüft den aktuellen Wert von Korb 3.
2. Es vergleicht diesen Wert mit dem bisherigen Allzeithoch (ATH).
3. Liegt der aktuelle Wert um mehr als die eingestellte **Drawdown-Toleranz %** unter dem ATH, wird der Krisen-Modus aktiviert.

**💡 Ein konkretes Rechenbeispiel:**
* Dein Korb 3 hat ein Allzeithoch von **1.000.000 €** erreicht.
* Du hast eine **Drawdown-Toleranz von 10 %** eingestellt.
* Die Krise wird ausgelöst, sobald der Depotwert unter **900.000 €** fällt.

**Szenario A (Normal-Modus):** Das Depot liegt innerhalb der Toleranz (z. B. bei 950.000 €). Die Rente wird normal aus Korb 3 entnommen. Gleichzeitig greift das **Rebalancing** (siehe Punkt 4), um K1 und K2 aufzufüllen.

**Szenario B (Krisen-Modus - Das Einfrieren):** Der Markt korrigiert stark, das Depot fällt auf 850.000 €.
* **Korb 3 wird sofort eingefroren.** Es finden keine Aktienverkäufe im Tief statt.
* Die Rente wird stattdessen aus dem Cash-Bestand (**K1**) entnommen.
* Ist K1 leer, greift das System auf die Anleihen (**K2**) zurück.
* Korb 3 bleibt unangetastet, bis er sich wieder auf über 900.000 € erholt hat oder die Puffer leer sind.

---

## 📊 Simulations-Module

### Backtest Historie
Ermöglicht den Stresstest durch echte historische Krisen (z. B. Dotcom-Blase 2000 oder Finanzkrise 2008). 
* **Blau:** Dreikorb-Strategie (mit aktivem Drawdown-Schutz und Rebalancing).
* **Orange (gestrichelt):** Vollinvest-Szenario (100% Aktien, kein Schutz).

### Monte-Carlo & SWR
* **Daten-Basis:** Wähle zwischen der mathematischen Normalverteilung oder dem **Historischen Bootstrapping**, das echte historische Monatsrenditen zufällig kombiniert.
* **Median Brutto-Entnahme:** Der Chart zeigt dir genau, wie viel Brutto-Kapital im Median über 5.000 Simulationsläufe inkl. Steuern abgeflossen ist.
* **SWR (Maximale Rente):** Ermittelt den maximalen **Netto-Betrag**, den du monatlich entnehmen kannst, damit dein Depot in 95 % aller simulierten Zukünfte bis zum Zielalter durchhält.

### 📥 Excel-Export
Der Export liefert detaillierte monatliche Daten für deine persönliche Archivierung und tiefergehende Analysen.
