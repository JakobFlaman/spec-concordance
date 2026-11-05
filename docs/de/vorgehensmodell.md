# Das Vorgehensmodell

Gleiche Phasen, gleiche Bausteine, gleiche Vorlagen für jedes Vorhaben.

## 1. Phasen

| Phase | Ziel | Artefakt | Gate |
|---|---|---|---|
| Idee & Nutzen | Warum? Für wen? | 01 Projektsteckbrief | – |
| Marktanalyse | Was gibt es schon, wo ist die Lücke? | 02 Marktanalyse | – |
| Geschäftsmodell | Wie entsteht Wert? Open-Core-Schnitt | 03 Open-Core-Modell | – |
| Anforderungen | Was muss es können? | 04 Anforderungen → OpenSpec-Specs | **Phasen-Gate 1** (Council + Maintainer) |
| Architektur & Design | Wie bauen wir es? | 07 ADRs | **Phasen-Gate 2** |
| Umsetzung | Iterativ bauen | OpenSpec-Changes | Qualitäts-Gate je Change |
| Qualitätssicherung | Funktioniert es, ist es sicher? | 08 Teststrategie, Test-Reports | Qualitäts-Gate je Release |
| Betrieb & Weiterentwicklung | Läuft es dauerhaft? | 09 Betrieb, 10 Roadmap | – |

Die ersten vier Phasen werden einmal sauber durchlaufen. Ab der Umsetzung arbeitet das Projekt in Changes: jede Änderung ist ein OpenSpec-Change mit Council-Review und Qualitäts-Gate.

## 2. Querschnittsbausteine

Diese Bausteine sind keine Phase, sondern in jeder Phase aktiv:

- **Rollen- und Berechtigungskonzept** (05) – Rollen im Produkt und im Projekt
- **Audit und Nachvollziehbarkeit** (06) – was protokolliert wird und wer es sieht
- **Testing** (08) – Strategie pro Ebene, Abnahmekriterien ab Phase Anforderungen
- **Open Source + Added Value** (03) – Lizenz, Schnitt, Beitragsregeln
- **Dokumentation** – Markdown als einzige Quelle
- **Sicherheit und Datenschutz** – Threat-Modell, DSG/DSGVO
- **Feedback und Fehlerbehebung** (11) – Eingang, Klassifikation, Rückkopplung

## 3. Der Council

Sechs Rollen prüfen jede Spezifikation und jeden Change unabhängig voneinander:

| Rolle | Blickwinkel | Besonderheit |
|---|---|---|
| Security | Berechtigungen, Datenschutz, Angriffsfläche | Vetorecht |
| Architektur | Schichten, Schnittstellen, ADRs | – |
| Support/Betrieb | Fehlermeldungen, Diagnose, Updates | – |
| Entwicklung | Machbarkeit, Aufwand, Testbarkeit | – |
| Fachbereich | Nutzen, Verständlichkeit | um Fachrollen erweiterbar |
| Testmanagement | Abdeckung, Regression, Reporting | rot = kein Archivieren |

Die Rollen sind als Subagenten umgesetzt (`agents/`). Sie sehen die Voten der anderen nicht. Widersprüche werden im Protokoll benannt, nicht geglättet.

## 4. Der Change-Kreislauf

```
Meldung ─▶ change-proposal ─▶ council-review ─▶ Umsetzung ─▶ quality-gate ─▶ archive
   ▲                                                                          │
   └────────── Rückkopplung: Tests · Doku · Rollenkonzept · Roadmap ◀─────────┘
```

## 5. Grundsätze

1. **Die Spezifikation ist die Wahrheit.** Code, der nicht der Spec entspricht, ist ein Fehler – oder die Spec muss per Change angepasst werden.
2. **Keine Selbstabnahme.** Wer umsetzt, prüft nicht.
3. **Harte Gates.** Rot bleibt rot.
4. **Der Mensch entscheidet an den Gates.** Die KI bereitet vor, der Maintainer gibt frei.
5. **Jede Meldung bekommt eine Antwort.**

## 6. Abgrenzung zu OpenSpec, Spec Kit und BMAD

| | OpenSpec | Spec Kit | BMAD | spec-concordance |
|---|---|---|---|---|
| Lebende Specs, Change-Zyklus | ✅ | – | – | ✅ (via OpenSpec) |
| Frühe Phasen (Markt, Geschäftsmodell) | – | – | ✅ | ✅ |
| Rollen-Reviews | – | – | ✅ (Agenten bauen) | ✅ (Agenten prüfen) |
| Harte Qualitäts-Gates | – | teilweise | – | ✅ |
| Feedback-Rückkopplung | – | – | – | ✅ |
