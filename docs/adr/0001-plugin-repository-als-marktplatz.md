# ADR 0001: Plugin-Repository als eigener Marktplatz

- Status: angenommen
- Datum: 2026-11-06
- Change: `add-github-marketplace`

## Kontext

spec-concordance wurde bisher über einen lokalen Klon und das Plugin-Menü von Claude Code eingebunden. Der Maintainer will eine Installation direkt aus GitHub, beschrieben im README. Claude Code installiert Plugins aus Marktplätzen (Git-Repositories mit `.claude-plugin/marketplace.json`).

## Entscheid

Das Plugin-Repository ist zugleich Marktplatz. `marketplace.json` listet genau ein Plugin mit der Quelle `./` (Repository-Stamm). Die Version steht nur in `plugin.json`; Nutzer erhalten Neues über Releases (Versionssprung). Skills beziehen Plugin-Dateien über `${CLAUDE_PLUGIN_ROOT}`. `main` wird nur über Pull Requests mit grüner CI geändert.

Einzelheiten und Begründungen: `openspec/changes/add-github-marketplace/design.md` (nach dem Archivieren unter `openspec/changes/archive/`).

## Folgen

- Installation mit einem Befehl, ohne Klon; Updates nur bei Versionssprung.
- Plugin- und Marktplatzname sind stabile Kennungen (Änderung nur über `renames`).
- Jeder Change braucht einen Pull Request; die Freigabe G11 ist das Mergen.
- Mehrere Plugins im selben Repository würden einen Umbau in Unterordner erfordern.
