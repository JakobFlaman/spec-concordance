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
| Aufruf | `python3 scripts/check-conventions.py [--warn] [--id-pattern REGEX] [STAMM ...]`; STAMM ist ein Projektordner mit `openspec/`, Standard: aktueller Ordner |
| Quelle der Struktur | `openspec list --specs --json`, `openspec list --json` (aktive Changes, archivierte sind nicht enthalten), `openspec show <spec> --type spec --json`, `openspec show <change> --json --deltas-only`; jeweils im Projektstamm ausgeführt |
| Geprüft | Basis-Anforderungen und ADDED-/MODIFIED-Deltas: RC-001 (Anforderungstext laut OpenSpec), RC-002, RC-007 (pro Spec-Datei); MODIFIED zusätzlich RC-004 gegen die Basis-Spec derselben Capability und die RENAMED-Ziele desselben Changes; RENAMED: Zieltitel auf RC-002; REMOVED wird nicht geprüft |
| Anforderungstext | so, wie OpenSpec ihn liefert (ohne Szenarien und Codeblöcke); Inline-Code mit beliebig vielen Backticks und Zitate («…», "…", „…“) gelten als Erwähnung |
| Zeilennummer | wird zur Ausgabe in der Spec-Datei gesucht (erste Kopfzeile ausserhalb von Codeblöcken, die den Namen enthält); nicht gefunden → Zeile 0 |
| Ausgabe | eine Zeile je Verstoss: `<datei>:<zeile>: <RC-ID>: <Meldung> – «<Titel>» – siehe docs/de/process-model.md, Abschnitt «Anforderungen in OpenSpec»`; am Ende Zusammenfassung |
| Exitcodes | 0 = keine Verstösse (oder `--warn`), 1 = Verstösse, 2 = Bedien-/Eingabefehler (Stamm ohne `openspec/`, OpenSpec-CLI fehlt oder meldet einen Fehler, ungültiges Muster, keine Anforderungen gefunden) |
| ID-Muster | Standard `[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]+` |
| Abhängigkeiten | Python-Standardbibliothek (≥ 3.10) und OpenSpec-CLI (≥ 1.16, MIT, Node.js) im `PATH` oder über `OPENSPEC_BIN` |
| Sicherheit | liest nur, schreibt nichts, führt keine Inhalte aus; einziger Fremdaufruf ist die OpenSpec-CLI mit festen Argumenten (Liste, keine Shell), Namen von Specs und Changes stammen aus deren eigener Ausgabe |

## Tests

`python3 -m unittest discover -s tests -v`. Testdaten unter `tests/fixtures/conventions/` sind eigene kleine OpenSpec-Projekte (Ordner mit `openspec/`); die CI prüft nur den Stamm des Plugin-Repositorys. Tests, die die OpenSpec-CLI brauchen, setzen sie voraus (in der CI installiert).
