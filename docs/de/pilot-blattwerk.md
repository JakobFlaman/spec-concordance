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

## Folge-Changes

| Herkunft | Change | Repository |
|---|---|---|
| add-priority-convention, W1 | Prüfskript für die CI von Projekten bereitstellen | spec-concordance |
| add-priority-convention, Praxistest | 15 Anforderungstitel nach RC-002 umstellen (RENAMED bzw. vor dem Archivieren direkt im Change) | pdf-concordance |
