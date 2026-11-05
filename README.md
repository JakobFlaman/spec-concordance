# spec-concordance

> 🇬🇧 [English version](README.en.md)

**Ein Vorgehensmodell für spezifikationsgetriebene Entwicklung mit KI – mit Rollen-Reviews und harten Qualitäts-Gates.**

Der Name lehnt sich an das Schweizer Konkordanzprinzip an: Alle relevanten Sichtweisen sitzen am Tisch, bevor entschieden wird.

`spec-concordance` setzt auf [OpenSpec](https://github.com/Fission-AI/OpenSpec) auf und ergänzt es um das, was den bestehenden Spec-Driven-Development-Werkzeugen fehlt:

| Baustein | Was er leistet |
|---|---|
| **Phasenmodell** | Gleiche Phasen für jedes Vorhaben: Idee & Nutzen → Marktanalyse → Geschäftsmodell → Anforderungen → Architektur → Umsetzung → QS → Betrieb |
| **Council** | Sechs Rollen (Security, Architektur, Support/Betrieb, Entwicklung, Fachbereich, Testmanagement) prüfen jede Spezifikation und jeden Change und geben ein begründetes Votum ab |
| **Qualitäts-Gates** | Kein Change wird abgeschlossen ohne grüne Tests, Council-Votum und aktualisierte Spezifikation |
| **Vorlagen** | Elf Projekt-Artefakte vom Steckbrief bis zum Feedback- und Fehlerprozess |
| **Feedback-Schleife** | Fehler → Regressionstest, wiederkehrende Fragen → Doku, Wünsche → Roadmap |

## Warum

KI-Agenten erzeugen schnell plausiblen Code. Ohne Spezifikation driftet er von der Absicht weg, ohne Gates sinkt die Qualität unbemerkt. `spec-concordance` macht die Spezifikation zur lebenden Wahrheit des Projekts und lässt die KI ihre eigene Arbeit nicht selbst abnehmen.

## Aufbau

```
.claude-plugin/       Plugin-Manifest für Claude Code
agents/               Council-Rollen (je eine Datei pro Rolle)
skills/               Arbeitsabläufe: Projekt-Start, Council-Review, Change, Qualitäts-Gate
templates/de/         Vorlagen für die elf Projekt-Artefakte (Deutsch = Quelle)
templates/en/         Englische Übersetzungen (aus der deutschen Quelle erzeugt)
template-project/     Startvorlage für ein neues Projekt
docs/de/              Vorgehensmodell im Detail
docs/en/              English documentation
scripts/              Hilfsskripte (z. B. Prüfung veralteter Übersetzungen)
```

## Schnellstart

Voraussetzungen: [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), Node.js 20+, Git, Python 3.10+ (für die Prüfskripte).

```bash
# 1. OpenSpec installieren
npm install -g @fission-ai/openspec@latest

# 2. Plugin in Claude Code einbinden (lokaler Klon)
git clone https://github.com/<owner>/spec-concordance.git
# in Claude Code: /plugin → lokales Plugin aus ./spec-concordance hinzufügen

# 3. Neues Projekt aus der Startvorlage
cp -r spec-concordance/template-project mein-projekt
cd mein-projekt && git init && openspec init
```

Danach in Claude Code:

| Befehl | Zweck |
|---|---|
| `/spec-concordance:project-init` | Phase «Idee & Nutzen» bis «Anforderungen» geführt durchlaufen, Artefakte anlegen |
| `/spec-concordance:change-proposal` | Meldung, Wunsch oder Fehler in einen OpenSpec-Change überführen |
| `/spec-concordance:council-review` | Spezifikation oder Change aus allen sechs Rollen prüfen |
| `/spec-concordance:quality-gate` | Prüfen, ob ein Change abgeschlossen werden darf |

## Status

Frühes Stadium (0.1). Siehe [CHANGELOG](CHANGELOG.md).

## Sprachen

Deutsch ist die Quellsprache, Englisch wird daraus abgeleitet. `scripts/check-i18n.py` meldet veraltete Übersetzungen.

## Lizenz

[MIT](LICENSE) © 2026 Jakob Flaman

Baut auf OpenSpec (MIT) auf und ist von GitHub Spec Kit (MIT) und BMAD-METHOD (MIT) inspiriert. «BMAD» ist eine Marke der BMad Code, LLC; dieses Projekt steht in keiner Verbindung dazu.
