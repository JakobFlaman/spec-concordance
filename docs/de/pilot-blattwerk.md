# Pilot 1: Blattwerk (PDF-Viewer & -Editor)

Datum: 2026-11-05 · Projekt-Repository: `pdf-concordance` · Stand: Phasen-Gate 1, Council-Review durchgeführt

Erkenntnisse aus dem ersten Einsatz von spec-concordance an einem echten Vorhaben. Jede Erkenntnis wird als eigener Change am Plugin umgesetzt.

## Ablauf

1. Bestehendes Lastenheft (61 Anforderungen) aus einem Claude Doc übernommen
2. Artefakte 01–04 daraus abgeleitet, 05–11 als Gerüst
3. OpenSpec initialisiert, Phase 1 als Change `add-viewer-phase-1` (10 Capabilities, 26 Requirements, 30 Tasks)
4. `openspec validate --strict` bestanden (nach Anpassung, siehe P1)
5. Council-Review mit sechs unabhängigen Rollen: 5 × Zustimmung mit Auflagen, 1 × Ablehnung (Testmanagement, Teststrategie leer) → nicht freigegeben, 27 Auflagen

Das Gate hat gewirkt: Die Ablehnung ist berechtigt, und mehrere Rollen haben dieselben Kernlücken unabhängig voneinander gefunden (Rendering-Soll von vier Rollen, verschlüsselte Dateien von drei).

## Erkenntnisse für das Plugin

| Nr. | Erkenntnis | Vorschlag | Priorität |
|---|---|---|---|
| P1 | OpenSpec verlangt SHALL/MUST in jeder Anforderung und meldet SHOULD/MAY. MoSCoW-Prioritäten passen nicht ins RFC-2119-Schema. | Konvention ins Plugin: immer SHALL, Priorität im Titel `(ID, Should)`; Regel in `project-init` und `openspec/config.yaml` der Startvorlage | hoch |
| P2 | Projekte haben eigene Veto-Regeln (z. B. Security erst ab Phase 3, Architektur nur bei Technologiewahl). Die Rollen kennen sie nur, weil der Auftrag sie auf CLAUDE.md verwies. | `council-review` übergibt jeder Rolle CLAUDE.md und eine Veto-Tabelle aus `.spec-concordance/council.md` | hoch |
| P3 | Testmanagement-Regel «Testlauf rot oder nicht ausgeführt = Ablehnung» passt nicht für Phasen-Gates ohne Code. | Gate-Typ unterscheiden: Phasen-Gate (Prüfbarkeit, Strategie) vs. Change-/Release-Gate (Testlauf) | hoch |
| P4 | Querschnitts-Artefakte (05, 08, 09) waren als «vor Gate 1» markiert, aber leer; erst das Council hat es gemerkt. | Pro Phasen-Gate eine Pflichtliste der Artefakte; `project-init` prüft sie vor dem Review | hoch |
| P5 | Veto «bei Gates durch Jakob» und KI-Rolle Testmanagement überschneiden sich. | Klarstellen: KI-Votum ist Empfehlung, Veto liegt beim benannten Menschen; Protokoll trennt beides | mittel |
| P6 | Beim Import des Lastenhefts aus dem Claude Doc gingen die Quellen-URLs verloren. | Import-Hilfe (Skript) für Claude Docs und Word, die Links und Tabellen erhält | mittel |
| P7 | Kürzungen gegenüber dem Lastenheft beim Überführen in Specs fielen mehreren Rollen auf. | `change-proposal`: Pflichtabschnitt «Abweichungen von der Quelle» im Proposal | mittel |
| P8 | Viele Befunde betreffen Testbarkeit (Soll-Herkunft, Toleranz, Messverfahren). | Vorlage 08 um «Soll-Ergebnis: Herkunft, Metrik, Schwellwert» je Testart erweitern | mittel |
| P9 | Begriff «Gate n» doppelt belegt (Phasen-Gate vs. Release). | Begriffe im Vorgehensmodell festlegen: Phasen-Gate P1…P4, Release-Gate R0.5 … | niedrig |
| P10 | Sechs Rollen à ca. 100k Tokens und 1–1,5 Minuten. | Kosten/Dauer in der Doku nennen; Option «Schnellreview» mit 3 Rollen für kleine Changes | niedrig |

## Erkenntnisse aus dem Trockenlauf am Plugin

Der erste vollständige Zyklus (Change `add-priority-convention`: Proposal → Council-Review → Umsetzung → Qualitäts-Gate → Freigabe → Archiv) lief am Plugin selbst. Das Gate brauchte 19 Läufe, davon 18 nicht bestanden. Jeder Befund war echt; die Zahl der Läufe zeigt aber Lücken im Ablauf.

| Nr. | Erkenntnis | Vorschlag | Priorität |
|---|---|---|---|
| T1 | Der Massstab für G7 («Spec ↔ Verhalten») war offen. Ein unabhängiger, adversarialer Prüfer findet bei einer Näherung (hier: Markdown ohne Parser) immer einen weiteren Randfall. Erst der Entscheid nach Lauf 18 – realistische Durchlässe sind Blocker, absichtliche Verschleierung ist dokumentierte Grenze – hat die Schlaufe beendet. | `quality-gate`: G7-Massstab ausdrücklich festlegen (gebrochene Zusage oder realistischer stiller Durchlass); Grenzen gehören vor der Umsetzung ins Design, nicht danach | hoch |
| T2 | Zusagen wie «nie ein stiller Durchlass» oder «in jedem Fall» in Spec und Design sind Einladungen an den Prüfer. Sie wurden mehrfach präzisiert. | `change-proposal`: absolute Zusagen nur mit genanntem Vergleichsmassstab und Grenzen | hoch |
| T3 | Sonderfälle aufzuzählen hat nicht konvergiert (Läufe 10–13). Konvergiert hat erst die positive Festlegung («sicher ist nur …») zusammen mit einem Vergleichstest gegen eine Referenz (markdown-it) mit Gegenprobe. | Für Prüflogik mit Näherung: positive Regel + Vergleichstest mit Gegenprobe als Standardmuster in `docs/de/process-model.md` | hoch |
| T4 | Einen Parser nachzubauen weicht vom Original ab (Läufe 1–7). Die Struktur aus der OpenSpec-CLI zu lesen hat diese Klasse von Befunden beendet. | Grundsatz: Werkzeug-Ausgabe statt Nachbau; als Prüffrage für die Rolle Architektur | mittel |
| T5 | Einzelvoten des Councils sind für die Nachvollziehbarkeit nötig: Eine zusammengefasste Auflage gab ein Votum falsch wieder (N1, Lauf 8). | `council-review`: Einzelvoten immer ablegen, Zusammenfassung zitiert wörtlich | mittel |
| T6 | Das Plugin hatte keine eigene Basis-Spec und keine Artefakte 01–11; Abnahmekriterien kamen nur aus dem Change. | Für das Plugin selbst Basis-Specs nach und nach aus archivierten Changes aufbauen (ab jetzt `requirement-conventions`) | mittel |
| T7 | G1a verlangt Rückverfolgbarkeit jeder Task; Abschluss-Tasks (CHANGELOG, Test-Summary) haben keine Anforderung. | `quality-gate` G1a: Ausnahme für Abschluss-Tasks festhalten | niedrig |
| T8 | Aufwand: 19 Gate-Läufe à rund 110–140k Tokens und 2–7 Minuten, dazu Council-Review und Nachtrag. | Kosten in der Doku nennen; nach drei nicht bestandenen Läufen zum selben Punkt den Maintainer zum Massstab befragen | mittel |

## Folge-Changes

| Herkunft | Change | Repository |
|---|---|---|
| add-priority-convention, W1 | Prüfskript für die CI von Projekten bereitstellen | spec-concordance |
| add-priority-convention, Praxistest | 15 Anforderungstitel nach RC-002 umstellen (RENAMED bzw. vor dem Archivieren direkt im Change) | pdf-concordance |
| add-priority-convention, Gate-Lauf 9 | GitHub-Actions in der CI per Commit-SHA statt Major-Tag fixieren (S3) | spec-concordance |
| add-priority-convention, Gate-Lauf 19 (B1) | Zeilen in `check-conventions.py` mit `split("\n")` statt `splitlines()` trennen (U+2028, U+0085, `\f`), wie OpenSpec und CommonMark | spec-concordance |
| add-github-marketplace, Council D16 | `source-hash`-Kopf für README.en.md bzw. READMEs in `check-i18n.py` aufnehmen | spec-concordance |
