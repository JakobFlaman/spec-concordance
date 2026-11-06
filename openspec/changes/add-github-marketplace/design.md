# Design: Installation direkt aus GitHub

Grundsatzentscheid als ADR: `docs/adr/0001-plugin-repository-als-marktplatz.md`.

## Entscheid

Das Plugin-Repository ist zugleich sein eigener Marktplatz (Plugin-Katalog von Claude Code). Die Datei `.claude-plugin/marketplace.json` liegt neben `plugin.json` und verweist mit der relativen Quelle `./` auf den Repository-Stamm.

| Punkt | Festlegung | Begründung |
|---|---|---|
| Marktplatz-Name | `spec-concordance` | Gleich wie das Plugin; kein reservierter Name; Installationskennung `spec-concordance@spec-concordance` |
| Marktplatz-Felder | `name`, `description`, `owner.name` (nur Name, keine E-Mail-Adresse), `plugins` mit genau einem Eintrag | Pflichtfelder laut Claude-Code-Doku; Beschreibung vermeidet Warnung von `claude plugin validate` (E3); keine Personendaten (S3) |
| Eintrag | `name` = `spec-concordance` (= `name` in `plugin.json`), `source` = `./`, `description` | Abweichende Namen sind laut Claude-Code-Doku die häufigste Fehlerursache |
| Stabile Kennungen | Plugin- und Marktplatzname ändern sich nicht; falls doch, nur über eine `renames`-Zuordnung in `marketplace.json` | Der Name steht als Schlüssel in `enabledPlugins` der Nutzer (A4) |
| Version | nur in `plugin.json`, nicht im Marktplatz-Eintrag | Doppelte Angabe meldet `claude plugin validate` als Widerspruch; CLAUDE.md bindet die Version an `plugin.json` und CHANGELOG |
| Updates | nur über Releases (Entscheid Maintainer): Nutzer erhalten Neues erst, wenn `version` steigt; README nennt `/plugin marketplace update spec-concordance` und das Einschalten der automatischen Aktualisierung | Bewusste Freigabe statt jedem Commit; Claude-Code-Doku «Release a new version» |
| Plugin-Pfad in Skills | `${CLAUDE_PLUGIN_ROOT}` | Claude Code ersetzt die Variable in Plugin-Skills durch das Installationsverzeichnis (Doku «Skills», string substitutions). Ohne Klon gibt es keinen anderen bekannten Pfad |
| Installationsbefehl | `/plugin install spec-concordance --marketplace JakobFlaman/spec-concordance` (ab Claude Code 2.1.275); sonst `/plugin marketplace add JakobFlaman/spec-concordance` und `/plugin install spec-concordance@spec-concordance`. Claude Code fragt vor der Installation nach Bestätigung | Einschritt-Befehl schlägt `claude plugin validate` selbst vor |
| Zugriff | Öffentliches Repository: keiner nötig. Privates Repository: Claude Code nutzt die Git-Zugangsdaten des Rechners und fragt nicht nach; bei `owner/repo` zuerst SSH (Schlüssel ohne Passwortabfrage), sonst HTTPS mit gespeichertem Zugang; `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` erzwingt HTTPS. Empfohlen mit minimalen Rechten: SSH-Schlüssel oder feingranularer Token nur mit Lesezugriff auf dieses Repository; nie Tokens in URLs oder Projektdateien | Claude-Code-Doku «Grant access to a private marketplace»; S2, O3. Das Repository ist öffentlich (Entscheid Maintainer); der Teil zu privat bleibt für den Fall einer Änderung |
| Neues Projekt | leerer Ordner, `git init`, dann `/spec-concordance:project-init` | `project-init` liest Vorlagen und `template-project/` aus dem Plugin |
| Verteilkanal `main` | Änderungen nur über Pull Requests mit grüner CI (Entscheid Maintainer); G11 = Mergen; CI läuft auf `push` nach `main` und auf `pull_request` | S1: Ein Commit auf `main` erreicht neue Installationen sofort. Der Branch-Schutz (Pull Request vor dem Mergen, Status-Check `checks` muss bestehen) wird in GitHub eingerichtet |
| Prüfung | Python-Test im bestehenden Testlauf (nur Standardbibliothek): Pflichtfelder, genau ein Eintrag, Name gleich, Quelle `./`, keine Version im Eintrag, keine E-Mail im `owner`; Gegenprobe mit Fixture | `claude plugin validate` braucht Claude Code in der CI – zusätzliche Abhängigkeit; lokal und im Gate wird es zusätzlich ausgeführt |

## Alternativen

| Alternative | Verworfen, weil |
|---|---|
| Lokaler Klon + «lokales Plugin hinzufügen» (heute) | Umweg, den der Maintainer nicht will; Updates nur per `git pull` |
| Eigenes Marktplatz-Repository, das auf dieses verweist | Zweites Repository ohne Nutzen, solange es nur ein Plugin gibt |
| Plugin in Unterordner `plugins/spec-concordance/` verschieben | Grosser Umbau aller Pfade; der Stamm als Quelle ist zulässig (`"."` bzw. `"./"`) |
| `version` weglassen, jeder Commit erreicht Nutzer | Vom Maintainer verworfen: keine bewusste Freigabe |
| Installation an einen Tag binden (`…#v0.2.0`) | Nutzer müssten für jedes Update einen neuen Befehl ausführen; PR-Pflicht plus Releases schützt ebenso |

## Grenzen

- Bis zum Release 0.2.0 bezeichnet die Version 0.1.0 keinen eindeutigen Stand: Wer heute installiert, erhält den aktuellen Stand von `main`, mit der Bezeichnung 0.1.0.
- Neue Installationen erhalten immer den Stand von `main`. Geschützt ist dieser Kanal nur, wenn der Branch-Schutz in GitHub eingerichtet ist; bis dahin gilt die PR-Pflicht als Arbeitsregel (CLAUDE.md).
- Wer ein privates Repository nicht lesen darf, kann nicht installieren. Das ist gewollt.
- Der ganze Repository-Inhalt (auch `tests/`, `openspec/`) landet im Plugin-Cache. Die `CLAUDE.md` im Stamm lädt Claude Code dabei nicht als Kontext (Warnung von `claude plugin validate`); sie gilt nur für die Arbeit am Plugin selbst.
- Die Installation wird nicht in der CI geprüft (bräuchte Claude Code und Netzzugang), sondern einmal manuell im Gate nach festem Protokoll (`tasks.md` 4.1).
- Der Texttest zu `${CLAUDE_PLUGIN_ROOT}` prüft die Formulierung im Skill, nicht das Verhalten eines Agenten; das Verhalten belegt der manuelle Test.
