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
* **Die Performance:** Das Tool berechnet dir automatisch die echte, zeitgewichtete Rendite (CAGR p.a.) deines Dreikorb-Mixes, völlig unabhängig von den entnommenen Rentenbeträgen.
* **Ansicht:** Zeigt die Dreikorb-Strategie (Blau) im direkten Vergleich zu einem 100% Aktien-Vollinvest-Szenario (Orange).

### 2. 🔮 Die Monte-Carlo-Simulation (Das Multiversum deines Ruhestands)

Während der historische Backtest dir zeigt, wie deine Strategie in der *Vergangenheit* (z. B. 2008) abgeschnitten hätte, wirft die Monte-Carlo-Simulation einen Blick in alle möglichen *Zukünfte*. Da niemand weiß, wie sich die Börse in den nächsten 30 Jahren exakt verhalten wird, berechnet das System nicht nur eine einzige Zukunft, sondern erschafft ein **"Multiversum" aus bis zu 5.000 verschiedenen Lebensläufen**. 

#### 1. Auf welche Daten greift das System zu? (Die zwei Motoren)
Bevor die Simulation startet, wählst du aus, aus welchem Daten-Pool das System die zukünftigen Börsenkurse würfeln soll:

* **Methode A: Historisch (Bootstrapping):** Das ist der Realitäts-Check. Das System lädt alle echten, historisch gemessenen Monatsrenditen deines gewählten Index-Mixes herunter. Wenn es nun eine neue Zukunft simuliert, greift es blind in diesen großen Topf voller historischer Monate und zieht einen zufälligen heraus (z. B. den Krisen-Monat Oktober 1987, dann den Boom-Monat November 2020 usw.). Das nennt sich *Ziehen mit Zurücklegen*. So entstehen tausende neue, wilde Börsenverläufe, die aber alle aus echten, extremen historischen Marktschwankungen (Crashs und Rallyes) bestehen.
* **Methode B: Mathematisch (Normalverteilung):** Das ist das akademische Modell. Du gibst über die Slider eine fiktive erwartete Rendite (z. B. 7,5 %) und eine Schwankungsbreite (Vola, z. B. 15 %) vor. Das System berechnet daraus eine klassische Glockenkurve und zieht für jeden Zukunftsmonat eine rein mathematische, zufällige Rendite.

#### 2. Was passiert in EINEM Durchlauf (Szenario)?
Ein einziger Durchlauf repräsentiert **einen kompletten Lebenspfad** von deinem Startalter bis zu deinem Zielalter (z. B. 42 Jahre = **504 Monate**). 

Für jeden einzelnen dieser Monate rechnet das System im Hintergrund deine komplette Strategie-Logik durch:
1. **Marktschwankung:** Das System würfelt die Rendite für den aktuellen Monat und passt den Wert deines Aktienkorbs (K3) an.
2. **Inflation:** Deine garantierte Netto-Rente sowie die Ziel-Stände deiner Puffer (K1 & K2) werden um die Inflationsrate erhöht.
3. **Der Krisen-Check:** Das System prüft deinen Drawdown. Liegt Korb 3 nahe am Allzeithoch oder herrscht Krise?
4. **Steuer & Entnahme:** Das mitatmende Kassenbuch berechnet deinen exakten, aktuellen Kursgewinnanteil. Die Steuer wird abgezogen und die Rente (je nach Krisen-Status) aus K3 oder den Puffern entnommen.
5. **Rebalancing:** Wenn Börsen-Boom herrscht, werden leere Puffer aus Korb 3 wieder aufgefüllt.

Geht dir vor dem Zielalter das Geld komplett aus, gilt dieser Lebenspfad als "Gescheitert". Überlebt dein Depot bis zum Zielalter, gilt der Pfad als "Erfolgreich".

#### 3. Was macht das System gesamthaft?
Das System durchläuft dieses komplette 504-Monats-Szenario nicht nur einmal, sondern (je nach Slider) **z. B. 5.000 Mal**. Bei 5.000 Loops führt dein Computer in wenigen Sekunden über 2,5 Millionen Einzelmonats-Berechnungen durch. Am Ende sammelt das Programm alle Lebensläufe ein und wertet sie aus:
* **Erfolgsquote:** Wie viele der simulierten Zukünfte hast du finanziell überlebt? (z. B. 98,5 %).
* **Der Median (Blaue Linie):** Der mittlere Weg (50 % liefen besser, 50 % schlechter). Der wahrscheinlichste Ausgang.
* **P10 & P90 (Der hellblaue Schlauch):** Das P10 ist dein **Worst-Case** (nur 10 % liefen schlechter). Das P90 ist dein **Best-Case**.
* **Der SWR-Rechner (Maximale Rente):** Das System sucht vollautomatisch genau den Euro-Betrag für deine Rente, bei dem die Erfolgsquote am Ende bei punktgenau 95 % liegt.

### 3. 🎯 Der Optimizer (Der Autopilot für dein Setup)
Dieses Modul beantwortet die wichtigste Frage: *"Wie muss ich mein aktuelles Gesamtkapital heute aufteilen, um die mathematisch höchste Überlebenswahrscheinlichkeit zu erreichen?"*

* **Was er macht:** Der Optimizer nimmt dein eingegebenes Gesamtkapital (K1 + K2 + K3) und testet vollautomatisch 30 verschiedene Puffer-Strategien durch (von 0,5 bis 3 Jahren Cash und 0 bis 5 Jahren Anleihen). Für jede Kombination feuert er im Hintergrund ein eigenes, schnelles Multiversum (250 Loops) ab.
* **Die absolute Daten-Wahrheit:** Im Gegensatz zum Backtest ignoriert der Optimizer ein manuell gewähltes Startjahr (wie 2016). Er greift für seine Simulationen immer auf die **gesamte, jahrzehntelange Historie der Börse** (bis zurück nach 1927) zu. So wird sichergestellt, dass deine vorgeschlagene Startaufteilung nicht nur in Bullenmärkten funktioniert, sondern echte historische Jahrhundert-Crashs überlebt.
* **Das Ergebnis:** Eine saubere Top-5-Rangliste. Sie zeigt dir die sichersten Setups inkl. der berechneten Start-Euro-Beträge für deine drei Körbe.
* **Die Anwendung:** Nimm das Setup auf Platz 1, trage die empfohlenen Jahre in die Puffer-Slider ("K1 Jahre", "K2 Jahre") ein und übernimm die Euro-Beträge für dein Start-Setup. Dein System ist nun perfekt ausbalanciert.

### 📥 Excel-Export
Der Export im Backtest-Tab liefert detaillierte monatliche Daten für deine persönliche Archivierung und tiefergehende Analysen.
