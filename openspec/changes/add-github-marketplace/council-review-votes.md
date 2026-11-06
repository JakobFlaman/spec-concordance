# Council-Review: Einzelvoten add-github-marketplace

Datum: 2026-11-06 · Gemeinsamer Review-Lauf mit dem Change `define-gate-standard`; hier nur die Voten zu diesem Change, unverändert übernommen.

### Security

**add-github-marketplace** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [S1] major Jeder Commit auf main geht ohne weiteren Schritt an alle Installationen (Out of Scope: «bis dahin erhalten Installationen den Stand des Standardzweigs»). Das Plugin bringt Agenten und Skills mit, die beim Nutzer Bash ausführen (z. B. council-test-management mit `tools: … Bash`, project-init ruft `<plugin>/scripts/check-conventions.py` auf). Die CI prüft erst nach dem Push (`on: push: branches: [main]`). Damit ist main ein Verteilkanal für ausführbaren Code, der an keiner Stelle geschützt ist. – Fundstelle: design.md «Grenzen», proposal.md «Out of Scope» – Auflage: In «Grenzen» festhalten, dass main der Verteilkanal ist, und eine Massnahme festlegen: entweder Branch-Schutz für main (nur über PR mit grünen Checks) oder die Installation an einen Tag bzw. ein Release binden.
- [S2] minor Der README-Hinweis `gh auth setup-git` hängt den gh-Token als Git-Credential-Helper ein. Der Token hat in der Regel den Scope `repo`, also Schreibrechte auf alle privaten Repositories des Kontos. Für eine reine Installation reicht Lesezugriff. – Fundstelle: design.md Tabelle «Privates Repository», spec DI-002 – Auflage: Im README zusätzlich einen Weg mit minimalen Rechten nennen (feingranularer Token mit nur Lesezugriff auf dieses Repository oder SSH-Schlüssel). Der Text darf nie Tokens in URLs oder in Dateien im Projekt zeigen.
- [S3] minor Die Einträge `owner` in marketplace.json und `author` in plugin.json können Personendaten enthalten, zum Beispiel eine E-Mail-Adresse. – Fundstelle: spec DI-001 – Auflage: Nur den Namen angeben, keine private E-Mail-Adresse.

Begründung: Keine neuen Geheimnisse, keine neuen Abhängigkeiten; CI-Prüfung nur Standardbibliothek, `permissions: contents: read` bleibt. Offen ist nur, wie ausführbarer Code über main ausgeliefert wird. Kein Veto, weil das Repository privat ist und nur der Maintainer schreibt. Gegenprüfung: keine Geheimnisse oder Personendaten im Repository (grep).

### Architektur

**add-github-marketplace** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [A1] major Der Pfad zum Plugin ist als Schnittstelle nicht festgelegt. DI-003 verlangt, dass `project-init` Vorlagen, `openspec-context.md` und `CLAUDE.md` «aus dem Plugin-Verzeichnis» bezieht; der Skill spricht nur von «des Plugins» bzw. `<plugin>/scripts/…`. Nach der Installation liegt das Plugin im Plugin-Cache. Claude Code ersetzt in Plugin-Skills `${CLAUDE_PLUGIN_ROOT}` (Doku «Skills», string substitutions), im Design nicht genannt. – Fundstelle: design.md «Neues Projekt»; tasks.md 2.4; DI-003 – Auflage: `${CLAUDE_PLUGIN_ROOT}` als Mechanismus festlegen; Szenario prüft, dass alle Plugin-Pfade im Skill diese Variable verwenden; manueller Test 3.1 um `project-init` in leerem Ordner ergänzen.
- [A2] major Grundsatzentscheid (Repository = Marktplatz, Stamm als Quelle, Updates über Version) ohne ADR; `docs/adr/` existiert nicht. – Fundstelle: design.md «Entscheid» – Auflage: ADR anlegen, Inhalt aus design.md übernehmen oder darauf verweisen.
- [A3] minor Aussagen zur Aktualisierung widersprechen sich (Out of Scope «Stand des Standardzweigs» vs. Doku: bei gesetzter `version` bleiben Nutzer auf der Kopie vom Installationszeitpunkt; verschiedene Stände tragen 0.1.0). – Fundstelle: proposal.md vs. design.md – Auflage: Proposal korrigieren; in den Grenzen festhalten, dass 0.1.0 bis zum Release keinen eindeutigen Stand bezeichnet.
- [A4] minor Rückbau und Namensstabilität fehlen: `spec-concordance@spec-concordance` landet in `enabledPlugins`; späteres Umbenennen oder Entfernen bricht Installationen. – Fundstelle: design.md «Grenzen» – Auflage: Festhalten, dass Plugin- und Marktplatzname stabile Kennungen sind; Änderungen nur über `renames`.
ADR nötig: ja, «Plugin-Repository als eigener Marktplatz (Quelle ./, Updates über plugin.json-version)»

Begründung: Fügt sich sauber ein; Quelle `./` laut Doku zulässig; Name und Version nur an einer Stelle. Versionsangaben stimmen mit Doku (`/plugin install … --marketplace` ab 2.1.275, Shell-Form ab 2.1.292). Offen: Pfad-Schnittstelle von `project-init`.

### Support/Betrieb

**add-github-marketplace** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [O1] major Update-Pfad nicht festgelegt; Proposal und Design widersprechen sich. Out of Scope sagt, Installationen erhielten «bis dahin den Stand des Standardzweigs»; `plugin.json` setzt aber `version: 0.1.0`, und laut Claude-Code-Doku («Release a new version») bleiben Nutzer auf ihrer zwischengespeicherten Kopie, bis sich die Version ändert. Automatische Aktualisierung ist bei Drittanbieter-Marktplätzen standardmässig aus. Mehrere Stände tragen dieselbe Bezeichnung «0.1.0»; Fehlermeldungen lassen sich keinem Stand zuordnen. – Fundstelle: proposal.md «Out of Scope», design.md «Grenzen», DI-002 – Auflage: Satz im Proposal korrigieren; DI-002 um Update-Anleitung im README erweitern (`/plugin marketplace update spec-concordance` bzw. `claude plugin update spec-concordance@spec-concordance`, «Änderungen nur bei Versionssprung», Auto-Update einschalten); ausdrücklich entscheiden, ob vor dem Veröffentlichen 0.2.0 freigegeben oder `version` weggelassen wird.
- [O2] major Ohne Klon: `project-init` Schritt 4 ruft `python3 <plugin>/scripts/check-conventions.py` auf, Vorlagen kommen aus `templates/` und `template-project/` «des Plugins». Wie der Agent das Plugin-Verzeichnis im Cache findet, ist nicht festgelegt; Task 2.4 und Szenario prüfen nur den Wortlaut. – Fundstelle: DI-003, tasks.md 2.4, skills/project-init/SKILL.md Schritt 1, 3, 4 – Auflage: Mechanismus im Design festlegen und belegen; manuellen Test 3.1 um einen Lauf von `/spec-concordance:project-init` in einem leeren Ordner erweitern, inkl. `check-conventions.py`.
- [O3] minor Für das private Repository nur `gh auth login`/`gh auth setup-git` genannt. Claude Code versucht bei `owner/repo` zuerst SSH (Schlüssel ohne Passwortabfrage); `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` umgeht die SSH-Prüfung; kein Hinweis zum Fehlerbild. – Fundstelle: design.md «Privates Repository», DI-002 – Auflage: SSH und HTTPS kurz beschreiben, auf Fehlerbehebung der Claude-Code-Doku verweisen.
- [O4] minor Kein Migrationshinweis für bestehende Klon-Installationen. – Fundstelle: proposal.md – Auflage: Satz «Umstieg von der Klon-Installation» ins README.
- [O5] minor `/plugin install … --marketplace` verlangt eine Bestätigung und öffnet die Plugin-Details; erst dort wird installiert. – Fundstelle: DI-002 – Auflage: Im README sagen, dass Bestätigungen folgen.

Begründung: Repository-Stamm als Marktplatz ist schlank und vertretbar; CI-Prüfung und manueller Test angemessen. Offen: Updates (O1) und Auffinden des Plugins ohne Klon (O2).

### Entwicklung

**add-github-marketplace** – Votum: ZUSTIMMUNG MIT AUFLAGEN
Aufwand: S – grösste Unsicherheit: wie `project-init` im Plugin-Cache den Plugin-Pfad findet
- [E1] major `project-init` nennt die Quelle nur als «`templates/<sprache>/` des Plugins» und `python3 <plugin>/scripts/…`. Task 2.4 legt nicht fest, wie der Plugin-Pfad gefunden wird; ein Agent muss raten, wo die installierte Kopie im Cache liegt. Das Szenario «project-init nutzt das Plugin» lässt sich so nicht als Test formulieren. – Fundstelle: tasks.md 2.4, spec DI-003, skills/project-init/SKILL.md Schritte 1, 3–5 – Auflage: Weg zum Plugin-Pfad festlegen (Basisverzeichnis des Skills oder Plugin-Variable), mit kurzem Spike prüfen; im Szenario die konkrete Zeichenkette nennen, die der Test sucht.
- [E2] minor «Validierung mit Claude Code» (DI-001) und «Installation in sauberer Umgebung» (DI-002) sind nicht automatisiert; nur das zweite ist als manuell gekennzeichnet, und zwar im THEN-Text statt mit dem Hinweis-Block wie bei RC-003/RC-005. – Fundstelle: specs/distribution/spec.md – Auflage: Beide als «> Manueller Test …» kennzeichnen, Nachweis in Task 1.4 bzw. 3.1.
- [E3] minor Spike auf einer Kopie mit Claude Code 2.1.318 und `source: "./"`: `claude plugin validate .` besteht, meldet aber zwei Warnungen (keine Beschreibung auf Marktplatz-Ebene; `CLAUDE.md` im Stamm wird nicht als Kontext geladen). Version 2.1.275 und Einschritt-Befehl bestätigt. – Fundstelle: design.md «Eintrag», «Grenzen» – Auflage: Beschreibung auf Marktplatz-Ebene in Task 1.1; die `CLAUDE.md`-Warnung als Grenze festhalten.
- [E4] minor Task 1.2 zählt die Pflichtfelder nicht auf; Task 1.3 überschneidet sich mit dem bestehenden Testlauf. – Fundstelle: tasks.md 1.2/1.3 – Auflage: Felder nennen (`name`, `owner.name`, `plugins[].name`, `plugins[].source`); festlegen, ob 1.3 einen eigenen Schritt braucht.
- [E5] minor `README.en.md` hat keinen Kopf mit `source-hash`, wie CLAUDE.md verlangt; `check-i18n.py` erfasst die READMEs nicht. – Fundstelle: README.en.md, tasks.md 2.2 – Auflage: Kopf setzen oder als eigenen Change vormerken.

Begründung: Klein, machbar, abgegrenzt; Spike bestätigt die Kernannahmen. Offen: wie der Skill im installierten Zustand zu seinen Vorlagen kommt.

### Fachbereich

**add-github-marketplace** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [F1] major – Für installierte Nutzer fehlt der Weg zur Aktualisierung. Laut design.md erhalten sie Änderungen erst, wenn `version` steigt. Der alte Weg wird gerade wegen «Updates nur per git pull» verworfen, aber DI-002/DI-003 verlangen im README keinen Abschnitt zum Aktualisieren. – Fundstelle: design.md «Grenzen» und «Alternativen»; specs/distribution/spec.md DI-002 – Auflage: DI-002 um «Aktualisieren» ergänzen (Befehl zum Nachladen des Marktplatzes bzw. Plugins, Hinweis, dass Änderungen nur mit einem Release kommen), mit Szenario und Test-Task.
- [F2] minor – Nach dem Wegfall des Klons müssen die Voraussetzungen erhalten bleiben: OpenSpec-CLI (`project-init` führt `openspec init` aus) und Python für `check-conventions.py`. Für Nutzer ohne Klon ist unklar, wo `<plugin>/scripts/check-conventions.py` liegt. – Fundstelle: DI-003; tasks.md 2.1/2.4; skills/project-init/SKILL.md Schritt 4 – Auflage: Im README die Voraussetzungen ausdrücklich behalten und erklären, wie ein Mensch die Prüfskripte ohne Klon aufruft (oder dass das nur über den Skill geht).
- [F3] minor – Es fehlt der Umstieg von der heutigen lokalen Installation, die zumindest der Maintainer selbst nutzt. – Fundstelle: proposal.md «What Changes» – Auflage: README-Hinweis: zuerst das lokale Plugin entfernen, dann aus GitHub installieren.
- [F4] minor – «Marktplatz» wird nur im Proposal erklärt, nicht im README. Offen ist, was bei fehlendem Zugriff passiert und an wen man sich wendet. – Fundstelle: DI-002 – Auflage: Begriff im README beim ersten Auftreten erklären und «Zugriff beim Maintainer anfragen» nennen.

Begründung: Beantwortet den Wunsch des Maintainers direkt; Umfang klein und abgegrenzt. Lücken im Lebenszyklus nach der Installation (Aktualisieren, Umstieg) und bei der Verständlichkeit.

### Testmanagement

**add-github-marketplace** – Votum: ZUSTIMMUNG MIT AUFLAGEN
Abdeckung: 4 von 7 Abnahmekriterien automatisch geplant (DI-001 «Name weicht ab», DI-002 «Befehle im README», DI-003 «Kein Kopieren», DI-004 «CI-Lauf»); 2 manuell geplant (DI-001 «Validierung», DI-002 «Installation in sauberer Umgebung»); 1 ohne Nachweis. Testlauf: nicht ausgeführt (vor Umsetzung, Prüfbarkeit beurteilt)
- [T1] major Das Szenario «project-init nutzt das Plugin» (DI-003) hat weder einen Test noch einen manuellen Nachweis. Task 2.4 ändert nur den Skill. Das THEN ist nicht prüfbar formuliert: schon heute steht dort «des Plugins». – Fundstelle: spec DI-003; tasks.md 2.4 – Auflage: Konkrete Prüfgrösse festlegen (z. B. ein Pfadpräfix, das jede Vorlagen- und `template-project`-Angabe tragen muss) und einen Texttest einplanen, analog zu `test_project_init_references_snippet`.
- [T2] major Der einzige Nachweis für die Kernanforderung DI-002 ist der manuelle Installationstest. «Saubere Umgebung» ist nicht definiert, die Zwei-Schritt-Variante wird nie ausgeführt. – Fundstelle: spec DI-002; tasks.md 3.1 – Auflage: Protokoll im Voraus festlegen: Claude-Code-Version, Commit-SHA, Art des Git-Zugangs, beide Befehlsvarianten, Ausgabe von `claude plugin list`; Ergebnis in die Test-Summary.
- [T3] minor In der Testliste fehlt «genau ein Plugin-Eintrag» (SHALL in DI-001); offen, wie die Gegenprobe mit abweichendem Namen gebaut wird. – Fundstelle: tasks.md 1.2 – Auflage: Anzahl der Einträge prüfen; Gegenprobe mit synthetischer Fixture unter `tests/fixtures/`, nicht die echte Datei ändern.
- [T4] minor README-Test zu ungenau: `template-project/` steht berechtigt in der Strukturübersicht, das Szenario betrifft nur den Schnellstart. – Fundstelle: tasks.md 2.3; README.md Z. 31 – Auflage: Test auf den Abschnitt Schnellstart beschränken, Muster festlegen (`git clone`, `cp … template-project`); festhalten, dass der Test gegen das heutige README fehlschlägt.
- [T5] minor Für DI-004 und DI-001 «Validierung» ist kein echter Nachweis geplant. – Fundstelle: tasks.md 1.3, 1.4 – Auflage: Run-ID eines grünen CI-Laufs und Ausgabe von `claude plugin validate .` mit Version in der Test-Summary ablegen.

Begründung: Teststrategie im Kern stimmig; Konsistenzprüfung automatisiert mit Gegenprobe; manuelle Installation offen als Grenze benannt. Es fehlen ein prüfbarer Massstab für DI-003 und ein Protokoll für den manuellen Kern-Nachweis.
