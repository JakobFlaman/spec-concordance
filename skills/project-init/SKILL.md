---
name: project-init
description: Führt durch die frühen Phasen eines neuen Vorhabens (Idee & Nutzen, Marktanalyse, Geschäftsmodell, Anforderungen) und legt die Projekt-Artefakte aus den Vorlagen an. Verwenden beim Start eines neuen Projekts oder wenn ein bestehendes Projekt auf spec-concordance umgestellt wird.
---

# Projekt-Start

## Ablauf

Arbeite die Phasen der Reihe nach ab. Stelle pro Phase die Leitfragen aus der jeweiligen Vorlage, höchstens drei auf einmal. Was schon vorliegt (Lastenheft, Notizen, bestehendes Repo), zuerst lesen und nicht erneut erfragen.

| Phase | Vorlage | Ergebnis |
|---|---|---|
| 1. Idee & Nutzen | `01-project-brief.md` | Problem, Zielgruppe, Nutzenversprechen, Abgrenzung |
| 2. Marktanalyse | `02-market-analysis.md` | Alternativenmatrix mit Quellen, Lücke, Positionierung |
| 3. Geschäftsmodell | `03-open-core-model.md` | Schnitt offener Kern / Added Value, Lizenz |
| 4. Anforderungen | `04-requirements.md` | Anforderungen mit MoSCoW und Abnahmekriterien |
| Querschnitt | `05`–`11` | Gerüst anlegen, Inhalte im Lauf des Projekts |

1. **Vorlagen kopieren** aus `templates/<sprache>/` des Plugins nach `docs/artifacts/` im Projekt.
2. **Phase 1–4 ausfüllen** im Dialog. Für die Marktanalyse im Web recherchieren und Quellen angeben; Annahmen als solche kennzeichnen.
3. **Anforderungen in OpenSpec überführen:** Aus `04-requirements.md` die Must- und Should-Anforderungen als Specs unter `openspec/specs/<capability>/` anlegen.
4. **CLAUDE.md** des Projekts aus `template-project/CLAUDE.md` erstellen und Projektname, Testbefehl, Namensraum und Lizenz eintragen.
5. **Phasen-Gate:** Council-Review über Steckbrief, Open-Core-Modell und Anforderungen (`/spec-concordance:council-review`). Erst nach Freigabe durch den Maintainer beginnt die Architekturphase.

## Regeln

- Leitfragen beantworten lassen, nicht selbst erfinden. Fehlt eine Antwort, als offen markieren.
- Keine Technologieentscheide vor Phase 4 – die gehören in die Architektur und als ADR festgehalten.
