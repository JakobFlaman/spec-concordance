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
.claude-plugin/       Plugin-Manifest und Marktplatz-Datei für Claude Code
agents/               Council-Rollen (je eine Datei pro Rolle)
skills/               Arbeitsabläufe: Projekt-Start, Council-Review, Change, Qualitäts-Gate
templates/de/         Vorlagen für die elf Projekt-Artefakte (Deutsch = Quelle)
templates/en/         Englische Übersetzungen (aus der deutschen Quelle erzeugt)
template-project/     Startvorlage für ein neues Projekt
docs/de/              Vorgehensmodell im Detail
docs/adr/             Architekturentscheide
docs/en/              English documentation
scripts/              Hilfsskripte (z. B. Prüfung veralteter Übersetzungen)
```

## Schnellstart

Voraussetzungen: [Claude Code](https://code.claude.com/docs) ab Version 2.1.275, Node.js 20+, Git, Python 3.10+ (für die Prüfskripte) und die OpenSpec-CLI ab 1.16.

### 1. OpenSpec installieren

```bash
npm install -g @fission-ai/openspec@1.16.0
```

### 2. Plugin direkt aus GitHub installieren

Dieses Repository ist zugleich ein *Marktplatz* – ein Plugin-Katalog, aus dem Claude Code Plugins installiert. Ein Klon ist nicht nötig. In Claude Code eingeben:

```
/plugin install spec-concordance --marketplace JakobFlaman/spec-concordance
```

Claude Code fragt nach einer Bestätigung und zeigt die Details des Plugins; dort die Installation bestätigen.

Ältere Claude-Code-Versionen (vor 2.1.275) brauchen zwei Schritte:

```
/plugin marketplace add JakobFlaman/spec-concordance
/plugin install spec-concordance@spec-concordance
```

Im Terminal statt in Claude Code: `claude plugin marketplace add JakobFlaman/spec-concordance`, danach `claude plugin install spec-concordance@spec-concordance`.

**Zugriff.** Solange das Repository öffentlich ist, braucht es nichts weiter. Ist es privat, verwendet Claude Code die Git-Zugangsdaten dieses Rechners und fragt nicht nach:

- **SSH** (wird zuerst versucht): ein Schlüssel ohne Passwortabfrage, zum Beispiel im `ssh-agent` geladen.
- **HTTPS:** ein im Credential-Helper gespeicherter Zugang. Mit minimalen Rechten über einen feingranularen GitHub-Token, der nur dieses Repository lesen darf. `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` überspringt den SSH-Versuch.

Tokens nie in eine URL oder in eine Projektdatei schreiben. Ohne Lesezugriff: Zugriff beim Maintainer anfragen.

### 3. Neues Projekt starten

```bash
mkdir mein-projekt && cd mein-projekt && git init
```

Danach in Claude Code `/spec-concordance:project-init` aufrufen. Der Skill holt Vorlagen und Startvorlage aus dem installierten Plugin, richtet OpenSpec ein und ruft die Konventionsprüfung selbst auf.

### Aktualisieren

Neue Stände kommen nur mit einem Release, also mit einer höheren Version in `plugin.json` (siehe [CHANGELOG](CHANGELOG.md)). Aktualisieren in Claude Code:

```
/plugin marketplace update spec-concordance
```

Automatisch: in `/plugin` unter *Marketplaces* den Marktplatz `spec-concordance` wählen und *Enable auto-update* einschalten.

### Umstieg von der Klon-Installation

Wer das Plugin bisher aus einem lokalen Klon eingebunden hat, entfernt dieses lokale Plugin in `/plugin` und installiert danach wie oben aus GitHub. Den Klon braucht es nur noch, um am Plugin mitzuentwickeln.

### Befehle

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
