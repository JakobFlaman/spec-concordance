# Design: Installation direkt aus GitHub

## Entscheid

Das Plugin-Repository ist zugleich sein eigener Marktplatz. Die Datei `.claude-plugin/marketplace.json` liegt neben `plugin.json` und verweist mit der relativen Quelle `./` auf den Repository-Stamm.

| Punkt | Festlegung | Begründung |
|---|---|---|
| Marktplatz-Name | `spec-concordance` | Gleich wie das Plugin; kein reservierter Name; Installationskennung `spec-concordance@spec-concordance` |
| Eintrag | `name` = `spec-concordance` (= `name` in `plugin.json`), `source` = `./`, `description` | Abweichende Namen sind laut Claude-Code-Doku die häufigste Fehlerursache |
| Version | nur in `plugin.json`, nicht im Marktplatz-Eintrag | Doppelte Angabe meldet `claude plugin validate` als Widerspruch; CLAUDE.md bindet die Version an `plugin.json` und CHANGELOG |
| Installationsbefehl | `/plugin install spec-concordance --marketplace JakobFlaman/spec-concordance` (ab Claude Code 2.1.275); sonst `/plugin marketplace add JakobFlaman/spec-concordance` und `/plugin install spec-concordance@spec-concordance` | Einschritt-Befehl schlägt `claude plugin validate` selbst vor |
| Privates Repository | Claude Code nutzt die Git-Zugangsdaten des Rechners und fragt nicht nach; README nennt `gh auth login` und `gh auth setup-git` | Laut Claude-Code-Doku «Grant access to a private marketplace» |
| Neues Projekt | leerer Ordner, `git init`, dann `/spec-concordance:project-init` | `project-init` liest Vorlagen und `template-project/` bereits aus dem Plugin |
| Prüfung | Python-Test (nur Standardbibliothek) und CI-Schritt: Pflichtfelder, Name gleich, Quelle `./`, keine Version im Eintrag | `claude plugin validate` braucht Claude Code in der CI – zusätzliche Abhängigkeit; lokal und im Gate wird es zusätzlich ausgeführt |

## Alternativen

| Alternative | Verworfen, weil |
|---|---|
| Lokaler Klon + «lokales Plugin hinzufügen» (heute) | Umweg, den der Maintainer nicht will; Updates nur per `git pull` |
| Eigenes Marktplatz-Repository, das auf dieses verweist | Zweites Repository ohne Nutzen, solange es nur ein Plugin gibt |
| Plugin in Unterordner `plugins/spec-concordance/` verschieben | Grosser Umbau aller Pfade; der Stamm als Quelle ist zulässig (`"."` bzw. `"./"`) |

## Grenzen

- Wer das private Repository nicht lesen darf, kann nicht installieren. Das ist gewollt.
- Nutzer erhalten Änderungen erst, wenn `version` in `plugin.json` steigt (oder nach Neuinstallation). Releases bleiben Aufgabe des Maintainers.
- Der ganze Repository-Inhalt (auch `tests/`, `openspec/`) landet im Plugin-Cache. Das ist unschädlich und hält die Pfade einfach.
- Die Installation selbst wird nicht in der CI geprüft (bräuchte Claude Code und Zugangsdaten), sondern einmal manuell im Gate.
