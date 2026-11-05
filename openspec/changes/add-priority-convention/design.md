# Design: Prioritätskonvention

Ersetzt einen ADR, solange das Plugin kein `docs/adr/` führt (Auflage A6).

## Entscheid

1. Alle Anforderungen verwenden SHALL. Die Verbindlichkeit ergibt sich allein aus der MoSCoW-Priorität im Titel.
2. Die Priorität steht im Titel: `<Titel> (<ID>, <Must|Should|Could>)`.
3. Won't wird nicht in OpenSpec geführt (Roadmap).

## Kontext

OpenSpec erwartet SHALL/MUST (RFC 2119: SHALL = verbindlich, SHOULD = empfohlen, MAY = optional) und meldet SHOULD/MAY, mit `--strict` als Fehler. Lastenhefte priorisieren nach MoSCoW. Beides muss zusammengehen, ohne OpenSpec zu verändern.

## Alternativen

| Alternative | Vorteil | Nachteil | Entscheid |
|---|---|---|---|
| SHOULD/MAY verwenden, Warnungen in Kauf nehmen | RFC-2119-treu | `--strict` und Gate G0 scheitern; Warnungen werden ignoriert | verworfen |
| Priorität als eigene Zeile im Anforderungstext (`Priorität: Should`) | Titel stabil, Umpriorisierung ist MODIFIED | Zeile kann vom Agenten weggelassen werden; nicht im Inhaltsverzeichnis und in `openspec list` sichtbar | verworfen |
| Priorität im Titel | sichtbar in jeder Übersicht, maschinell prüfbar, im Pilot erprobt | Umpriorisierung ist RENAMED (siehe Folgen) | **gewählt** |
| Eigenes Frontmatter / Metadatenblock | sauber getrennt | von OpenSpec nicht unterstützt | verworfen |

Für die Prüfung (Revision 2):

| Alternative | Vorteil | Nachteil | Entscheid |
|---|---|---|---|
| Eigener Markdown-Parser in Python | keine Node-Abhängigkeit | weicht laufend von OpenSpec ab (fünf Gate-Läufe) | verworfen |
| OpenSpec-CLI als Parser | sieht exakt dieselben Anforderungen wie OpenSpec | Node/OpenSpec nötig, langsamer | **gewählt** |

## Folgen

- Eine Umpriorisierung ist in OpenSpec eine Umbenennung (RENAMED mit FROM/TO). Das Prüfskript erkennt den typischen Fehler (MODIFIED mit nur geänderter Priorität) und weist darauf hin (RC-004).
- Für Lastenheft-Gewohnte wirkt «Should mit SHALL» widersprüchlich; Doku und Vorlage 04 erklären es.
- Bestehende Projekte migrieren über RENAMED; bis dahin läuft die Prüfung mit `--warn`.

## Schnittstelle `scripts/check-conventions.py`

Revision 2 (nach Gate-Lauf 7): Das Skript parst Markdown nicht mehr selbst, sondern liest die Struktur über die OpenSpec-CLI. Die Läufe 3 bis 7 scheiterten alle an Abweichungen zwischen eigenem Parser und OpenSpec (Codeblöcke, Kopfzeilen-Varianten, RENAMED-Syntax, verschachtelte Capabilities, Basis-Specs ohne Präfix). Ein Nachbau bleibt lückenhaft; die CLI ist für Gate G0 ohnehin Pflicht.

| Aspekt | Festlegung |
|---|---|
| Aufruf | `python3 scripts/check-conventions.py [--warn] [--id-pattern REGEX] [STAMM ...]`; STAMM ist ein Projektordner mit `openspec/`, Standard: aktueller Ordner. Ein Ordner ohne `openspec/` (z. B. `openspec/specs`) → Exit 2 mit Hinweis «Projektstamm angeben» |
| Quelle der Struktur | `openspec list --specs --json` (`specs[].id`), `openspec list --json` (`changes[].name`; nur aktive Changes), `openspec show <spec> --type spec --json` (`requirements[].name/.text`), `openspec show <change> --json --deltas-only` (`deltas[].spec/.operation`, bei ADDED/MODIFIED `requirements[]`, bei RENAMED `rename.from/.to`); jeweils im Projektstamm ausgeführt. Fehler: Exitcode ≠ 0 oder `status[]` mit `severity: error` → Exit 2 mit `message`. Fehlt ein erwartetes Feld → Exit 2 mit Spec-/Change-Name |
| Version | `openspec --version` beim Start; unter 1.16 → Exit 2 mit gefundener und benötigter Version. Getestet mit 1.16.0; die CI installiert genau diese Version |
| Pfadableitung | Basis: `<STAMM>/openspec/specs/<spec-id>/spec.md`; Delta: `<STAMM>/openspec/changes/<change>/specs/<spec-id>/spec.md`; `<spec-id>` kann verschachtelt sein (`area/cap`). Namen von Specs und Changes müssen `^[A-Za-z0-9][A-Za-z0-9._/-]*$` erfüllen und dürfen kein `..` enthalten (OpenSpec kennt kein `--`); gelesene Dateien müssen nach `resolve()` unter `<STAMM>/openspec/` liegen, sonst Exit 2 |
| Geprüft | Basis-Anforderungen und ADDED-/MODIFIED-Deltas: RC-001 (Anforderungstext laut OpenSpec), RC-002, RC-007 (pro Spec-Datei); MODIFIED zusätzlich RC-004 gegen die Basis-Spec derselben Capability und die RENAMED-Ziele desselben Changes; RENAMED: Zieltitel auf RC-002; REMOVED wird nicht geprüft |
| Anforderungstext | so, wie OpenSpec ihn liefert (ohne Szenarien und eingezäunte Codeblöcke ```/~~~; eingerückter Code ohne Zaun bleibt für OpenSpec Text und wird daher geprüft); Inline-Code und Zitate («…», “…”, „…“; gerade Anführungszeichen zählen nicht, sie kommen auch als Zollzeichen vor) gelten als Erwähnung, **nur wenn ihre Grenzen sicher feststehen** – positiv festgelegt statt Sonderfälle aufzuzählen (Gate-Läufe 10–13 haben gezeigt, dass jede Aufzählung Lücken hat). Sicher ist ein Anforderungstext, wenn (a) er keines der Zeichen `\`, `<`, `[` enthält – nach CommonMark können nur Backslash-Maskierung, Autolinks/HTML und Link-Ziele/-Titel Backticks vor Inline-Code verbrauchen – und (b) jeder Backtick-Lauf ein gleich langes Gegenstück auf derselben Zeile hat; dann paart CommonMark die Läufe genauso, und die Absatzgrenzen, die OpenSpec nicht liefert, spielen keine Rolle. Sonst gilt im ganzen Anforderungstext keine Erwähnung. Ausgeblendete Erwähnungen werden durch ein Leerzeichen ersetzt (keine Wortverschmelzung); das Schlüsselwort ist ein ganzes Wort, wobei `_` nicht als Wortzeichen zählt (`_SHOULD_`). **Bewusst strenger als CommonMark** (Entscheid Maintainer nach Gate-Lauf 10): im Zweifel melden – selten ein Fehlalarm (Abhilfe: Erwähnung umformulieren oder auf eine Zeile setzen), nie ein stiller Durchlass. Nachweis: Vergleichstest gegen markdown-it in `tests/fuzz/` (Aufruf in der Datei) |
| Zeilennummer | Kopfzeile der Anforderung (bei RENAMED die TO-Zeile); die Einträge einer Spec-Datei werden vor RC-007 nach dieser Zeile sortiert, weil OpenSpec ADDED vor MODIFIED liefert; wird zur Ausgabe in der Spec-Datei gesucht: Kopfzeilen (`###`) ausserhalb von Codeblöcken, die den Namen enthalten; dem n-ten Vorkommen eines Namens wird die n-te Fundstelle zugeordnet; nicht gefunden → Zeile 0 |
| Ausgabe | eine Zeile je Verstoss: `<datei>:<zeile>: <RC-ID>: <Meldung> – «<Titel>» – siehe docs/de/process-model.md, Abschnitt «Anforderungen in OpenSpec»`; am Ende Zusammenfassung |
| Exitcodes | 0 = keine Verstösse (oder `--warn`), 1 = Verstösse, 2 = Bedien-/Eingabefehler (Stamm ohne `openspec/`, OpenSpec-CLI fehlt, zu alt, Zeitüberschreitung oder Fehler, unerwartete Struktur, ungültiger Name, ungültiges Muster, keine Anforderungen gefunden) |
| ID-Muster | Standard `[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]+` |
| Abhängigkeiten | Ersetzt Auflage S1: Python-Standardbibliothek (≥ 3.10) und OpenSpec-CLI (MIT, Node.js) ab 1.16; in der CI exakt 1.16.0, installiert mit `--ignore-scripts` (keine Installationsskripte des Pakets). Gefunden über `OPENSPEC_BIN` (nur aus der Umgebung, nie aus Repository-Dateien oder Argumenten) oder `openspec` im `PATH` |
| Sicherheit | liest nur, schreibt nichts, führt keine Inhalte aus; einziger Fremdaufruf ist die OpenSpec-CLI mit festen Argumenten (Liste, keine Shell, Timeout 60 s); Namen geprüft (siehe Pfadableitung); für den Aufruf werden `OPENSPEC_*`-Variablen entfernt, die Verzeichnisse umlenken, und `DO_NOT_TRACK=1` gesetzt |

## Tests

`python3 -m unittest discover -s tests -v`. Testdaten unter `tests/fixtures/conventions/` sind eigene kleine OpenSpec-Projekte (Ordner mit `openspec/`); jeder Change hat eine minimale `proposal.md`, ausser genau einem Fixture für RC-008. Die CI prüft nur den Stamm des Plugin-Repositorys. Tests, die die OpenSpec-CLI brauchen, werden lokal ohne CLI sichtbar übersprungen; in der CI (`CI=true`) schlagen sie fehl. Fehlende, zu alte oder fehlerhafte CLI werden über `OPENSPEC_BIN` mit einer Attrappe (Python-Skript) getestet.
