# Council-Review: Einzelvoten define-gate-standard

Datum: 2026-11-06 · Gemeinsamer Review-Lauf mit dem Change `add-github-marketplace`; hier nur die Voten zu diesem Change, unverändert übernommen.

### Security

**define-gate-standard** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [S1] major QG-002 stuft «absichtlich konstruierte Fälle (Verschleierung)» pauschal zur Beobachtung herab. Bei Anforderungen mit Sicherheitszweck ist die absichtliche Umgehung aber genau das Bedrohungsmodell (Erkennung von Geheimnissen, Eingabevalidierung, Berechtigungsprüfungen). Ein gezielter Bypass würde so nie ❌. – Fundstelle: specs/quality-gate/spec.md QG-002, design.md Zeile «realistisch» – Auflage: Ausnahme ergänzen: Bei Anforderungen mit Sicherheitszweck (Klassifikation `security` oder Befund der Rolle Security) gilt ein konstruierter Fall als realistisch, ausser er ist als Grenze in design.md dokumentiert und Security hat im Council zugestimmt. Dazu ein Szenario und einen Test.
- [S2] minor Der Maintainer kann eine Einordnung umstufen (design.md «Einordnung»). Die Spec verlangt aber nicht, dass die Umstufung festgehalten wird. – Fundstelle: design.md Tabelle «Einordnung», spec QG-002 – Auflage: Umstufungen mit Begründung im Gate-Ergebnis bzw. im Change festhalten.

Begründung: Behebt T1/T2 sinnvoll; Grenzen vor dem Review helfen auch Security. Die pauschale Herabstufung wäre für sicherheitsrelevante Prüflogik falsch und muss vor dem Archivieren eingeschränkt werden.

### Architektur

**define-gate-standard** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [A1] major Geltungsbereich von QG-003 unscharf und uneinheitlich («Prüf-, Erkennungs- oder Automatisierungslogik» vs. «Prüf- und/oder Automatisierungslogik»); niemand legt fest, wer entscheidet. Neuer offener Massstab – genau das, was T1 beheben will. – Fundstelle: spec QG-003; proposal.md; tasks.md 1.3 – Auflage: Begriff einheitlich, positive Definition, Entscheidungsinstanz nennen (z. B. Council, im Zweifel Pflicht).
- [A2] major «Im Zweifel realistisch» und «der Maintainer kann umstufen» stehen nur im Design, nicht in QG-002. – Fundstelle: design.md «Einordnung»; spec QG-002 – Auflage: als Anforderungstext mit Szenario in QG-002.
- [A3] major Für die Eskalation fehlt ein Zustand: kein Ablageort für Läufe und Antwort des Maintainers; «dieselbe Anforderung» bei Gate-Punkten ohne Anforderungsbezug offen. – Fundstelle: spec QG-004; design.md «Grenzen» – Auflage: Ablage festlegen (Gate-Protokoll im Change-Ordner mit Lauf, Punkt, Anforderung, Ergebnis), Zählregel präzisieren.
- [A4] major `.github/PULL_REQUEST_TEMPLATE.md` Z. 15 führt weiterhin «G7 Spezifikation nachgeführt»; keine Task. – Fundstelle: tasks.md Abschnitt 2 – Auflage: Task zum Nachführen der PR-Vorlage.
- [A5] minor Modulschnitt: Capability heisst `quality-gate`, QG-003 regelt aber `change-proposal` und `council-review`. – Fundstelle: specs/quality-gate/spec.md – Auflage: Schnitt begründen oder QG-003 in eigene Capability (z. B. `change-process`).
ADR nötig: nein (Prozessregel, im Design mit Alternativen begründet)

Begründung: Behebt T1, T2 und T8 (Eskalation) an den richtigen Stellen ohne Duplikation; Rückbau unkritisch. Auflagen schliessen Unschärfen, die sonst neue Gate-Schlaufen erzeugen würden.

### Support/Betrieb

**define-gate-standard** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [O1] major Die Eskalation (QG-004) zählt Läufe, aber keine Anforderung legt fest, wo Gate-Läufe festgehalten werden. Der Skill gibt das Ergebnis nur als Tabelle im Chat aus; ein unabhängiger Agent hat meist keine Kenntnis früherer Läufe. – Fundstelle: QG-004, design.md «Grenzen», skills/quality-gate/SKILL.md «Ablauf» – Auflage: Protokoll der Gate-Läufe im Change verlangen (Nummer, nicht erfüllte Punkte mit Anforderung, Datum); der Skill liest es vor jedem Lauf; Test, dass die Regel im Skill steht.
- [O2] minor «Dieselbe Anforderung» passt nicht auf Gate-Punkte ohne Anforderungsbezug (G2, G8–G10). – Fundstelle: QG-004 – Auflage: Dort reicht «derselbe Gate-Punkt».
- [O3] minor Kosten und Laufzeit pro Gate-Lauf (T8) nicht übernommen. – Fundstelle: proposal.md – Auflage: Optional Dauer pro Lauf im Protokoll erfassen; sonst Folge-Change.

Begründung: Massstab und frühe Grenzen machen den Ablauf vorhersehbarer; Eskalation ohne festgelegten Lauf-Verlauf aber nicht durchsetzbar.

### Entwicklung

**define-gate-standard** – Votum: ZUSTIMMUNG MIT AUFLAGEN
Aufwand: S – grösste Unsicherheit: Zählung der Gate-Läufe für die Eskalation
- [E1] major Die Eskalation (QG-004) setzt voraus, dass der Gate-Agent frühere Läufe kennt; das Gate läuft aber in unabhängigen Agenten ohne gemeinsames Gedächtnis. Ort und Format für den Lauf-Verlauf fehlen. – Fundstelle: spec QG-004, tasks.md 1.2, design.md «Grenzen» – Auflage: Gate-Protokoll im Change festlegen (z. B. `openspec/changes/<id>/gate-log.md` mit Lauf, Gate-Punkt, Anforderung, Ergebnis) und Task anlegen.
- [E2] major Nach der Umbenennung von G7 ist offen, ob die formale Prüfung der Deltas bleibt; das Gate kann schwächer werden. – Fundstelle: skills/quality-gate/SKILL.md G7, tasks.md 1.1 – Auflage: Festlegen, ob die Vollständigkeit der Deltas in G7 bleibt oder ein eigener Punkt wird.
- [E3] major QG-001 «Realistischer stiller Verstoss», QG-002 «Konstruierter Fall», QG-003 «Change ohne Grenzen», QG-004 «Dritter Fehlschlag» beschreiben Agentenverhalten, sind nicht automatisierbar, aber nicht als manuell gekennzeichnet; G3 wäre nicht erfüllbar. – Fundstelle: specs/quality-gate/spec.md – Auflage: als «> Manueller Test …» kennzeichnen und Nachweis nennen.
- [E4] minor «Im Zweifel realistisch» steht nur im Design. – Auflage: in Anforderung oder Task 1.1 aufnehmen.
- [E5] minor Task 2.1 nennt nicht, welche Formulierungen der Test sucht; `tests/test_skills.py` existiert noch nicht. – Auflage: Schlüsselbegriffe pro Anforderung festlegen, Datei als neu kennzeichnen.
- [E6] minor «Prüf-, Erkennungs- oder Automatisierungslogik» (QG-003) ist Ermessensfrage. – Auflage: Abgrenzungsbeispiele oder Leitfrage im Skill.

Begründung: Setzt T1, T2 und T8 um, klein. Eskalation ohne Lauf-Verlauf nicht umsetzbar; bei G7 droht die formale Prüfung der Deltas verloren zu gehen.

### Fachbereich

**define-gate-standard** – Votum: ZUSTIMMUNG MIT AUFLAGEN
- [F1] major – Die Zweiteilung «realistisch → ❌ / konstruiert → Beobachtung» bildet den Entscheid nicht ab, mit dem der Trockenlauf geendet hat: Lauf 19 wurde mit B1 (U+2028 / `splitlines()`) bestanden, B1 ging als Folge-Change weiter. B1 ist keine absichtliche Verschleierung, nach QG-001 mit «im Zweifel realistisch» also ❌. – Fundstelle: spec.md QG-001/QG-002; design.md «Einordnung»; pilot-blattwerk.md «Folge-Changes» – Auflage: Umgang mit realistischen, aber seltenen Fällen festlegen (❌ oder begründeter Weg in einen Folge-Change); B1 als Referenzfall nennen.
- [F2] major – Nach QG-002 machen Fälle «innerhalb dokumentierter Grenzen» G7 nicht ❌, ohne dass die Grenze schon vor dem Council-Review bestand. So lässt sich eine Grenze nach dem Gate-Befund nachtragen – genau das Nachbessern, das T1 rügt. – Fundstelle: QG-002 Szenario «Konstruierter Fall» – Auflage: Nur Grenzen zählen lassen, die im Council-Review vorlagen; nachträgliche Grenzen nur mit festgehaltenem Entscheid des Maintainers.
- [F3] minor – Nach der Umbenennung von G7 ist offen, ob die bisherige formale Prüfung bleibt (Spec-Deltas vollständig, keine Widersprüche). – Fundstelle: QG-001; skills/quality-gate/SKILL.md G7 – Auflage: Klarstellen, dass G7 beide Teile prüft.
- [F4] minor – «Beobachtung» und «in Folge» sind nicht definiert: Verhältnis zu blocker/major/minor, Rücksetzen des Zählers bei Fehlschlag an anderem Punkt, Ablageort der Maintainer-Antwort. – Fundstelle: QG-002, QG-004 – Auflage: Begriffe im Skill definieren, Ablageort festlegen (z. B. council-review.md, Abschnitt «Gate-Verlauf»).

Begründung: Nutzen klar und belegt (18 nicht bestandene Läufe à 110–140k Tokens). Der Massstab muss aber den tatsächlichen Abschluss des Trockenlaufs abbilden und darf kein Schlupfloch über nachträgliche Grenzen öffnen. Hinweis der Rolle: «ab Claude Code 2.1.275» nicht geprüft, wird im Gate manuell getestet.

### Testmanagement

**define-gate-standard** – Votum: ZUSTIMMUNG MIT AUFLAGEN
Abdeckung: 3 von 7 Abnahmekriterien automatisch geplant (die «Regel/Pflicht im Skill»-Szenarien); 4 ohne geplanten Nachweis. Testlauf: nicht ausgeführt (vor Umsetzung)
- [T1] major Für vier Verhaltensszenarien ist weder Test noch manueller Nachweis vorgesehen: QG-001 «Realistischer stiller Verstoss», QG-002 «Konstruierter Fall», QG-003 «Change ohne Grenzen», QG-004 «Dritter Fehlschlag». Widerspricht der Regel in change-proposal (Abnahmekriterien als automatischer Test formulierbar). – Fundstelle: specs/quality-gate/spec.md; tasks.md 2.1 – Auflage: Für jedes Szenario einen manuellen, reproduzierbaren Nachweis einplanen; Referenzfälle aus dem Trockenlauf: Gate 17 (realistisch, ❌), Gate 18 (konstruiert, Beobachtung); für QG-003 ein Probe-Review auf einen synthetischen Change ohne «Grenzen». Alternativ als manuell kennzeichnen.
- [T2] minor Reine Texttests beweisen nur, dass Wörter vorkommen. – Fundstelle: tasks.md 2.1 – Auflage: Auf feste Formulierungen bzw. Tabellenzeilen prüfen (G7-Zeile, Kriterien (a)/(b), «realistisch»/«konstruiert», «major» in der Rolle) und mit Gegenprobe auf den heutigen Skill zeigen, dass der Test fehlschlägt.
- [T3] minor `tests/test_skills.py` gibt es nicht; die bestehenden Skill-Texttests stehen in `test_check_conventions.py`. – Fundstelle: tasks.md 2.1 – Auflage: «neu anlegen» präzisieren oder bestehende Datei nennen.
- [T4] minor In `.github/PULL_REQUEST_TEMPLATE.md` Z. 15 steht noch der alte G7-Name. – Fundstelle: tasks.md – Auflage: Task und Test ergänzen, damit der alte Name nirgends mehr vorkommt.
- [T5] minor Zählweise für QG-004 offen: Ort der Läufe, Zählung bei Befunden zu mehreren Anforderungen. – Fundstelle: spec QG-004 – Auflage: Gate-Laufprotokoll im Change festlegen, z. B. Tabelle «Vergleich mit Vorlauf» der Test-Summary.

Begründung: Behebt eine belegte Lücke; design.md benennt Grenzen ehrlich. Ausgerechnet die Szenarien zum neuen Verhalten haben keinen Nachweis; der Trockenlauf liefert Referenzfälle.
Hinweis der Rolle: Laut Rollendatei führt «Testlauf: nicht ausgeführt» im Qualitäts-Gate zur Ablehnung; hier als Vorprüfung vor der Umsetzung abgegeben. Im Gate gilt die Regel unverändert.
