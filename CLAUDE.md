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

## Befehle

```bash
# Tests (wird vom Qualitäts-Gate G2 ausgeführt)
python3 -m unittest discover -s tests -v
# Prüfungen
python3 scripts/check-conventions.py          # im Projektstamm; braucht OpenSpec-CLI ≥ 1.16
python3 scripts/check-i18n.py
openspec validate --all --strict
```

## Arbeitsweise mit Git

`main` ist der Verteilkanal: Wer das Plugin aus GitHub installiert, erhält den Stand von `main`. Deshalb gilt (Entscheid Maintainer, ADR 0001):

- **Keine direkten Commits auf `main`.** Jeder Change entsteht auf einem eigenen Branch (`change/<change-id>`) und kommt über einen Pull Request nach `main`.
- **Grüne CI ist Pflicht.** Ein Pull Request wird erst gemergt, wenn der Status-Check `checks` bestanden ist.
- **Freigabe G11 = Mergen.** Der Maintainer gibt einen Change frei, indem er den Pull Request mergt. Nach bestandenem Qualitäts-Gate kommt das Archivieren (`openspec archive`) als letzter Commit in den Pull Request; wirksam wird es erst mit dem Mergen.

Einstellungen für den Branch-Schutz in GitHub (*Settings → Branches → Add branch ruleset* bzw. *Branch protection rule* für `main`):

- *Require a pull request before merging* (ohne Pflicht-Approvals, solange der Maintainer allein ist)
- *Require status checks to pass* mit dem Check `checks`
- *Block force pushes* und *Restrict deletions*

## Versionierung

Semantic Versioning. Version in `.claude-plugin/plugin.json` und `CHANGELOG.md` immer gemeinsam ändern.
