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

## Folgen

- Eine Umpriorisierung ist in OpenSpec eine Umbenennung (RENAMED mit FROM/TO). Das Prüfskript erkennt den typischen Fehler (MODIFIED mit nur geänderter Priorität) und weist darauf hin (RC-004).
- Für Lastenheft-Gewohnte wirkt «Should mit SHALL» widersprüchlich; Doku und Vorlage 04 erklären es.
- Bestehende Projekte migrieren über RENAMED; bis dahin läuft die Prüfung mit `--warn`.

## Schnittstelle `scripts/check-conventions.py`

| Aspekt | Festlegung |
|---|---|
| Aufruf | `python3 scripts/check-conventions.py [--warn] [--id-pattern REGEX] [PFAD ...]`; ohne Pfad: `openspec/specs openspec/changes` |
| Eingabe | rekursiv alle `spec.md` unter den Pfaden; nur `openspec/changes/archive/` wird übersprungen, nicht beliebige Ordner namens «archive» |
| Codeblöcke | eingezäunte Codeblöcke (```` ``` ````, `~~~`) gelten dateiweit als Erwähnung: Überschriften darin sind weder Abschnitte noch Anforderungen, Schlüsselwörter darin keine Verstösse |
| Geprüft | Basis-Specs (`## Requirements`) sowie `## ADDED` und `## MODIFIED Requirements`; `## REMOVED` und `## RENAMED` werden nur für RC-004 gelesen |
| Basis für RC-004 | `openspec/specs/<capability>/spec.md` relativ zum Projektstamm (Elternordner von `openspec/`) |
| Ausgabe | eine Zeile je Verstoss: `<datei>:<zeile>: <RC-ID>: <Meldung> – «<Titel>» – siehe docs/de/process-model.md, Abschnitt «Anforderungen in OpenSpec»`; am Ende Zusammenfassung |
| Exitcodes | 0 = keine Verstösse (oder `--warn`), 1 = Verstösse, 2 = Bedien-/Eingabefehler (Pfad fehlt, keine `spec.md` gefunden, ungültiges Muster) |
| ID-Muster | Standard `[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]+` |
| Abhängigkeiten | nur Python-Standardbibliothek (≥ 3.10) |
| Sicherheit | liest nur, schreibt nichts, führt keine Inhalte aus (kein eval/exec, keine Shell), braucht keine Zugangsdaten |

## Tests

`python3 -m unittest discover -s tests -v` (nur Standardbibliothek). Testdaten unter `tests/fixtures/conventions/`; die CI scannt nur `openspec/`, nicht `tests/`.
