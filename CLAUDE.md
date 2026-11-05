# CLAUDE.md – Konventionen für dieses Repository

Dieses Repository ist das Plugin `spec-concordance` selbst. Es wird nach seinem eigenen Vorgehensmodell entwickelt («dogfooding»).

## Grundsätze

1. **Deutsch ist die Quellsprache.** Inhalte zuerst in `de` schreiben oder ändern. Englische Fassungen werden daraus abgeleitet und tragen im Kopf `source-hash` der deutschen Quelle.
2. **Spezifikation vor Code.** Jede inhaltliche Änderung läuft als OpenSpec-Change unter `openspec/changes/`.
3. **Keine Selbstabnahme.** Ein Change wird erst archiviert, wenn `/spec-concordance:quality-gate` bestanden ist.
4. **Rollen sind Dateien.** Neue oder geänderte Council-Rollen nur in `agents/` – nie im Fliesstext von Skills duplizieren.
5. **Kleine Schritte.** Ein Change = ein Thema.

## Schreibstil

- Schweizer Rechtschreibung (ss statt ß), sachlich, direkt, ohne Werbesprache.
- Fachbegriffe beim ersten Auftreten kurz erklären.
- Vorlagen enthalten Leitfragen statt Beispieltext, der kopiert wird.

## Namen

- Datei-, Ordner- und technische Namen (IDs, Frontmatter `name`, Befehle) sind **englisch**, kleingeschrieben, mit Bindestrich (`council-business.md`, `01-project-brief.md`).
- Inhalte sind deutsch (Quellsprache), Übersetzungen liegen in `en`-Ordnern.

## Struktur

- `agents/` – eine Datei pro Council-Rolle, Frontmatter `name`, `description`, `tools`
- `skills/<name>/SKILL.md` – Arbeitsabläufe
- `templates/<sprache>/NN-name.md` – nummerierte Artefakt-Vorlagen
- `docs/<sprache>/` – Erläuterungen zum Vorgehensmodell

## Versionierung

Semantic Versioning. Version in `.claude-plugin/plugin.json` und `CHANGELOG.md` immer gemeinsam ändern.
