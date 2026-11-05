# CLAUDE.md – <Projektname>

Dieses Projekt arbeitet nach dem Vorgehensmodell [spec-concordance](https://github.com/<owner>/spec-concordance) auf Basis von OpenSpec.

## Projekt

- **Name:** <Projektname>
- **Zweck:** siehe `docs/artefakte/01-projektsteckbrief.md`
- **Lizenz:** <MIT | Apache-2.0 | EPL-2.0 | AGPL-3.0>
- **Namensraum / Paket-ID:** <z. B. org.beispiel.produkt>
- **Maintainer:** <Name>

## Befehle

```bash
# Build
<befehl>
# Tests (wird vom Qualitäts-Gate ausgeführt)
<befehl>
# Lint / Format
<befehl>
```

## Arbeitsweise

1. Jede Änderung läuft als OpenSpec-Change (`/spec-concordance:change-proposal`).
2. Vor der Umsetzung: `/spec-concordance:council-review`.
3. Vor dem Archivieren: `/spec-concordance:quality-gate` – kein Archivieren bei Rot.
4. Bei Bugfixes zuerst einen Regressionstest schreiben, der den Fehler zeigt.
5. Architekturentscheide als ADR unter `docs/adr/`.

## Konventionen

- Datei-Header: <Projektname, Zweck, Copyright/SPDX-Lizenz, Kurz-Changelog>
- Schreibstil Doku: <Sprache, Rechtschreibung>
- Fehlermeldungen: sprechend, mit Fehlercode, Verweis auf `docs/errors.md`

## Projektspezifische Council-Rollen

Zusätzliche Fachrollen liegen unter `.spec-concordance/roles/`.
