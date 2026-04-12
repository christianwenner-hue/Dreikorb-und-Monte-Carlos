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

### 🔮 Die Monte-Carlo-Simulation (Das Multiversum deines Ruhestands)

Während der historische Backtest dir zeigt, wie deine Strategie in der *Vergangenheit* (z. B. 2008) abgeschnitten hätte, wirft die Monte-Carlo-Simulation einen Blick in alle möglichen *Zukünfte*. Da niemand weiß, wie sich die Börse in den nächsten 30 Jahren exakt verhalten wird, berechnet das System nicht nur eine einzige Zukunft, sondern erschafft ein **"Multiversum" aus bis zu 5.000 verschiedenen Lebensläufen**. 

#### 1. Auf welche Daten greift das System zu? (Die zwei Motoren)
Bevor die Simulation startet, wählst du aus, aus welchem Daten-Pool das System die zukünftigen Börsenkurse würfeln soll:

* **Methode A: Historisch (Bootstrapping):** Das ist der Realitäts-Check. Das System lädt alle echten, historisch gemessenen Monatsrenditen deines gewählten Index-Mixes herunter. Wenn es nun eine neue Zukunft simuliert, greift es blind in diesen großen Topf voller historischer Monate und zieht einen zufälligen heraus (z. B. den Krisen-Monat Oktober 1987, dann den Boom-Monat November 2020 usw.). Das nennt sich *Ziehen mit Zurücklegen*. So entstehen tausende neue, wilde Börsenverläufe, die aber alle aus echten, extremen historischen Marktschwankungen (Crashs und Rallyes) bestehen.
* **Methode B: Mathematisch (Normalverteilung):** Das ist das akademische Modell. Du gibst über die Slider eine fiktive erwartete Rendite (z. B. 7,5 %) und eine Schwankungsbreite (Vola, z. B. 15 %) vor. Das System berechnet daraus eine klassische Glockenkurve und zieht für jeden Zukunftsmonat eine rein mathematische, zufällige Rendite.

#### 2. Was passiert in EINEM Durchlauf (Szenario)?
Ein einziger Durchlauf repräsentiert **einen kompletten Lebenspfad** von deinem Startalter (z. B. 53 Jahre) bis zu deinem Zielalter (z. B. 95 Jahre). Das sind 42 Jahre oder exakt **504 Monate**. 

Für jeden einzelnen dieser 504 Monate rechnet das System im Hintergrund deine komplette Strategie-Logik durch:
1. **Marktschwankung:** Das System würfelt die Rendite für den aktuellen Monat und passt den Wert deines Aktienkorbs (K3) an.
2. **Inflation:** Deine garantierte Netto-Rente sowie die Ziel-Stände deiner Puffer (K1 & K2) werden um die Inflationsrate erhöht.
3. **Der Krisen-Check:** Das System prüft deinen Drawdown. Liegt Korb 3 nahe am Allzeithoch oder herrscht Krise?
4. **Steuer & Entnahme:** Das mitatmende Kassenbuch berechnet deinen exakten, aktuellen Kursgewinnanteil. Die Steuer wird abgezogen und die Rente (je nach Krisen-Status) aus K3 oder den Puffern entnommen.
5. **Rebalancing:** Wenn Börsen-Boom herrscht, werden leere Puffer aus Korb 3 wieder aufgefüllt.

Wenn der Monat abgeschlossen ist, geht das System in den nächsten Monat. Geht dir vor dem Zielalter das Geld komplett aus (Depotwert = 0), gilt dieser eine Lebenspfad als "Gescheitert". Überlebt dein Depot bis zum 95. Lebensjahr, gilt der Pfad als "Erfolgreich".

#### 3. Was macht das System gesamthaft?
Das System durchläuft dieses komplette 504-Monats-Szenario nicht nur einmal, sondern (je nach Slider) **z. B. 5.000 Mal**. Bei 5.000 Loops führt dein Computer in wenigen Sekunden über 2,5 Millionen Einzelmonats-Berechnungen durch.

Am Ende sammelt das Programm alle 5.000 Lebensläufe ein und wertet sie statistisch für dich aus:
* **Erfolgsquote:** Wie viele der 5.000 simulierten Zukünfte hast du finanziell überlebt? (Zeigt z. B. 98,5 %).
* **Der Median (Blaue Linie):** Das ist der mittlere Weg. Genau 50 % der Simulationen liefen besser, 50 % liefen schlechter. Dies ist der wahrscheinlichste Ausgang deines Ruhestands.
* **P10 & P90 (Der hellblaue Schlauch):** Das P10 (10. Perzentil) ist dein realistischer **Worst-Case**. Nur 10 % aller durchgespielten Crash-Szenarien verliefen noch schlimmer als diese untere Kante. Das P90 ist dein **Best-Case**.
* **Der SWR-Rechner (Maximale Rente):** Wenn du auf den Button klickst, spielt das System dieses 5.000-fache Multiversum dutzende Male hintereinander mit verschiedenen Entnahmebeträgen durch. Es sucht vollautomatisch genau den Euro-Betrag für deine Rente, bei dem die Erfolgsquote am Ende bei punktgenau 95 % liegt.

 durchhält.

### 📥 Excel-Export
Der Export liefert detaillierte monatliche Daten für deine persönliche Archivierung und tiefergehende Analysen.
