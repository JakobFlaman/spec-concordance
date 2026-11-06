# Das Vorgehensmodell

Gleiche Phasen, gleiche Bausteine, gleiche Vorlagen für jedes Vorhaben.

## 1. Phasen

| Phase | Ziel | Artefakt | Gate |
|---|---|---|---|
| Idee & Nutzen | Warum? Für wen? | 01 Projektsteckbrief | – |
| Marktanalyse | Was gibt es schon, wo ist die Lücke? | 02 Marktanalyse | – |
| Geschäftsmodell | Wie entsteht Wert? Open-Core-Schnitt | 03 Open-Core-Modell | – |
| Anforderungen | Was muss es können? | 04 Anforderungen → OpenSpec-Specs | **Phasen-Gate 1** (Council + Maintainer) |
| Architektur & Design | Wie bauen wir es? | 07 ADRs | **Phasen-Gate 2** |
| Umsetzung | Iterativ bauen | OpenSpec-Changes | Qualitäts-Gate je Change |
| Qualitätssicherung | Funktioniert es, ist es sicher? | 08 Teststrategie, Test-Reports | Qualitäts-Gate je Release |
| Betrieb & Weiterentwicklung | Läuft es dauerhaft? | 09 Betrieb, 10 Roadmap | – |

Die ersten vier Phasen werden einmal sauber durchlaufen. Ab der Umsetzung arbeitet das Projekt in Changes: jede Änderung ist ein OpenSpec-Change mit Council-Review und Qualitäts-Gate.

## 2. Querschnittsbausteine

Diese Bausteine sind keine Phase, sondern in jeder Phase aktiv:

- **Rollen- und Berechtigungskonzept** (05) – Rollen im Produkt und im Projekt
- **Audit und Nachvollziehbarkeit** (06) – was protokolliert wird und wer es sieht
- **Testing** (08) – Strategie pro Ebene, Abnahmekriterien ab Phase Anforderungen
- **Open Source + Added Value** (03) – Lizenz, Schnitt, Beitragsregeln
- **Dokumentation** – Markdown als einzige Quelle
- **Sicherheit und Datenschutz** – Threat-Modell, DSG/DSGVO
- **Feedback und Fehlerbehebung** (11) – Eingang, Klassifikation, Rückkopplung

## 3. Der Council

Sechs Rollen prüfen jede Spezifikation und jeden Change unabhängig voneinander:

| Rolle | Blickwinkel | Besonderheit |
|---|---|---|
| Security | Berechtigungen, Datenschutz, Angriffsfläche | Vetorecht |
| Architektur | Schichten, Schnittstellen, ADRs | – |
| Support/Betrieb | Fehlermeldungen, Diagnose, Updates | – |
| Entwicklung | Machbarkeit, Aufwand, Testbarkeit | – |
| Fachbereich | Nutzen, Verständlichkeit | um Fachrollen erweiterbar |
| Testmanagement | Abdeckung, Regression, Reporting | rot = kein Archivieren |

Die Rollen sind als Subagenten umgesetzt (`agents/`). Sie sehen die Voten der anderen nicht. Widersprüche werden im Protokoll benannt, nicht geglättet.

## 4. Der Change-Kreislauf

```
Meldung ─▶ change-proposal ─▶ council-review ─▶ Umsetzung ─▶ quality-gate ─▶ archive
   ▲                                                                          │
   └────────── Rückkopplung: Tests · Doku · Rollenkonzept · Roadmap ◀─────────┘
```

**Grenzen vor der Umsetzung.** Ist das Ergebnis eines Changes eine automatische Prüfung, Erkennung oder Entscheidung, nennt `design.md` vor dem Council-Review im Abschnitt «Grenzen», was bewusst nicht abgedeckt ist und wogegen geprüft wird. Zusagen wie «nie» oder «in jedem Fall» stehen nur mit Vergleichsmassstab und Grenzen.

**Massstab des Qualitäts-Gates.** Gate-Punkt G7 prüft, ob die Spezifikation nachgeführt ist und mit dem Verhalten übereinstimmt. Nicht erfüllt ist er bei einer gebrochenen ausdrücklichen Zusage oder einem Verstoss, der *realistisch* (kann bei der normalen Arbeit entstehen) und still durchgeht. *Konstruierte* Fälle (absichtliche Verschleierung) und Fälle innerhalb gültiger Grenzen sind Beobachtungen; im Zweifel gilt «realistisch». Bei Anforderungen mit Sicherheitszweck zählen auch konstruierte Fälle, ausser Security hat der Grenze zugestimmt.

**Gate-Protokoll und Eskalation.** Jeder Gate-Lauf steht in `gate-log.md` im Change, ebenso jeder Entscheid des Maintainers (Umstufen, Verschieben in einen Folge-Change, Bestätigen einer Grenze). Scheitert das Gate dreimal in Folge am selben Punkt – bei G3 und G7 zur selben Anforderung –, wird vor dem nächsten Lauf der Maintainer zum Massstab gefragt. Hintergrund: Im Trockenlauf am Plugin brauchte das Gate ohne festen Massstab 19 Läufe (`docs/de/pilot-blattwerk.md`, T1–T8).

## 5. Anforderungen in OpenSpec

OpenSpec verlangt in jeder Anforderung das Schlüsselwort SHALL oder MUST. Diese Schlüsselwörter stammen aus RFC 2119, einem Standard für Verbindlichkeitsstufen in Spezifikationen (SHALL = verbindlich, SHOULD = empfohlen, MAY = optional). Lastenhefte priorisieren dagegen nach MoSCoW. Damit beides zusammengeht, gilt für funktionale und nicht-funktionale Anforderungen:

| Regel | Inhalt |
|---|---|
| RC-001 | Im Anforderungstext steht immer SHALL. Das ist nur die von OpenSpec verlangte Syntax – die Verbindlichkeit legt allein die Priorität im Titel fest. |
| RC-002 | Titel in der Form `<Titel> (<ID>, <Must\|Should\|Could>)`, z. B. `Darstellungsmodi (LA-F-110, Should)`. Die ID ist die stabile Kennung aus der Anforderungsquelle. Won't-Anforderungen stehen in der Roadmap, nicht in OpenSpec. |
| RC-003 | Eine Quellanforderung mit gemischter Priorität («Must / Should») wird in je eine Anforderung pro Priorität mit derselben ID getrennt. Ist die Aufteilung unklar, entscheidet der Maintainer. |
| RC-004 | Eine Umpriorisierung ist eine Umbenennung: RENAMED mit FROM/TO, nicht MODIFIED. |
| RC-007 | Innerhalb einer Spec-Datei kommt jede Kombination aus ID und Priorität nur einmal vor. |

**Beispiel Umpriorisierung** (Should wird Must):

```markdown
## RENAMED Requirements

- FROM: `### Requirement: Darstellungsmodi (LA-F-110, Should)`
- TO: `### Requirement: Darstellungsmodi (LA-F-110, Must)`
```

**Prüfung:** `python3 scripts/check-conventions.py [STAMM ...]` im Projektstamm (Ordner mit `openspec/`) meldet Verstösse mit Datei, Zeile der Anforderung, Regel und Titel. Die Prüfung liest die Struktur über die OpenSpec-CLI (ab 1.16), damit sie dieselben Anforderungen sieht wie OpenSpec; die CLI wird über `OPENSPEC_BIN` oder `openspec` im `PATH` gefunden. Exitcodes: 0 = in Ordnung, 1 = Verstösse, 2 = Bedien- oder Eingabefehler.

| Meldung (Exit 2) | Abhilfe |
|---|---|
| OpenSpec-CLI nicht gefunden / zu alt | `npm install -g @fission-ai/openspec@1.16.0` oder `OPENSPEC_BIN` setzen |
| enthält kein openspec/ | im Projektstamm aufrufen, nicht in `openspec/specs` |
| OpenSpec meldet für «…» | Meldung von OpenSpec beheben, z. B. fehlende `proposal.md`; `openspec validate --all --strict` zeigt Details |
| Unerwartete Struktur von OpenSpec | OpenSpec-Version prüfen; getestet ist 1.16.0 |

**Migration bestehender Projekte:** Zuerst die Regeln mit `project-init` (Schritt «OpenSpec initialisieren») in `openspec/config.yaml` übernehmen. Dann die Prüfung mit `--warn` laufen lassen – sie meldet alle Verstösse, bricht aber nicht ab. Die Titel bestehender Anforderungen werden in einem eigenen Change per RENAMED umgestellt; danach läuft die Prüfung ohne `--warn`.

## 6. Grundsätze

1. **Die Spezifikation ist die Wahrheit.** Code, der nicht der Spec entspricht, ist ein Fehler – oder die Spec muss per Change angepasst werden.
2. **Keine Selbstabnahme.** Wer umsetzt, prüft nicht.
3. **Harte Gates.** Rot bleibt rot.
4. **Der Mensch entscheidet an den Gates.** Die KI bereitet vor, der Maintainer gibt frei.
5. **Jede Meldung bekommt eine Antwort.**

## 7. Abgrenzung zu OpenSpec, Spec Kit und BMAD

| | OpenSpec | Spec Kit | BMAD | spec-concordance |
|---|---|---|---|---|
| Lebende Specs, Change-Zyklus | ✅ | – | – | ✅ (via OpenSpec) |
| Frühe Phasen (Markt, Geschäftsmodell) | – | – | ✅ | ✅ |
| Rollen-Reviews | – | – | ✅ (Agenten bauen) | ✅ (Agenten prüfen) |
| Harte Qualitäts-Gates | – | teilweise | – | ✅ |
| Feedback-Rückkopplung | – | – | – | ✅ |
