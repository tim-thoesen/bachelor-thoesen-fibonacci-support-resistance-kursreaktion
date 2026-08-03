# Vergleich von Fibonacci-Retracements und horizontalen Support-/Resistance-Niveaus zur Analyse von Kursreaktionen

**Autor:** Tim Hendrik Thösen  
**Bachelorarbeit - Data and Information Science - TH Köln, 2026**

Dieses Repository enthält die Python-Implementierung der Bachelorarbeit zum Vergleich von Fibonacci-Retracements und horizontalen Support- und Resistance-Niveaus. Untersucht werden die Häufigkeit und Stärke von Kursreaktionen nach dem Erreichen der durch beide Ansätze abgeleiteten technischen Preisniveaus.

---

## Jupyter-Notebooks

### [1. Datenerhebung und Aufbereitung](1.datenerhebungAufbereitung.ipynb)

Download der historischen Kursdaten über `yfinance`, Aufbereitung der Datensätze und Erstellung der Metadaten zu den untersuchten Finanzinstrumenten und Marktphasen.

### [2. Berechnung der Analyseparameter](2.analyseparameter.ipynb)

Berechnung der Standardabweichungen, Reaktionsschwellen und Reaktionsfenster für die Hauptanalyse und die Robustheitsprüfung.

### [3. Eventanalyse](3.eventanalyse.ipynb)

Enthält die Funktionen von Fibonacci-Retracements und horizontalen Support- und Resistance-Niveaus sowie die definierte Eventlogik und deren Anwendung über alle Analyseeinheiten.

### [4. Auswertung](4.auswertung.ipynb)

Aggregation der Ergebnisse entsprechend der in Kapitel 3.9 beschriebenen Auswertung.

---

## Installation

Repository lokal herunterladen:

```bash
git clone https://github.com/tim-thoesen/bachelor-thoesen-fibonacci-support-resistance-kursreaktion.git
```

Benötigte Python-Bibliotheken installieren:

```bash
pip install -r requirements.txt
```

---

## Streamlit-Dashboard

Die Ergebnisse können über das Streamlit-Dashboard interaktiv betrachtet werden.

Start des Dashboards:

```bash
streamlit run streamlitApp.py
```

---

## Hinweis zu den Kursdaten

Die historischen Kursdaten wurden am **02.03.2026** heruntergeladen und im Repository gespeichert. Für die Reproduktion der Analyse sollte dieser Datenstand verwendet werden.

Von einem erneuten Download ist abzusehen, da `yfinance` historische Daten nachträglich anpassen kann. Dadurch könnten Abweichungen von den in der Arbeit dargestellten Ergebnissen entstehen.