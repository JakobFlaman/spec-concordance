# Probe zu define-gate-standard (Task 3.1)

Eingaben der manuellen Probe vom 2026-11-06, damit sie wiederholt werden kann. Die Regeldateien entsprechen dem Stand von Commit `47f608b` (Skills `quality-gate`, `change-proposal`, Rolle `council-test-management`).

| Datei | Fall |
|---|---|
| `fall1-befund.md` | Befund Gate-Lauf 17 von `add-priority-convention` |
| `fall2-befund.md` | Befund Gate-Lauf 18 von `add-priority-convention` (vereinfacht: Grenze als beim Review vorhanden angenommen; im Trockenlauf bestätigte sie der Maintainer nach Lauf 18) |
| `fall3/` | synthetischer Change «Prüfung auf Geheimnisse» ohne Abschnitt «Grenzen» |
| `fall4/gate-log.md` | synthetisches Gate-Protokoll mit drei Fehlschlägen G7 zu RC-001 |

Auftrag an den unabhängigen Agenten (wörtlich, Pfade angepasst):

> Lies zuerst die drei Regeldateien. Wende sie dann genau an – nur diese Regeln, nicht dein eigenes Urteil darüber, was sinnvoll wäre.
> 1. `fall1-befund.md`: Du führst das Qualitäts-Gate aus und hast diesen Befund zu G7. Ordne ihn nach dem Skill quality-gate ein und sage, ob G7 deswegen ✅ oder ❌ ist. Begründe mit der Regelstelle.
> 2. `fall2-befund.md`: dasselbe.
> 3. `fall3/`: Du bist die Rolle Testmanagement im Council-Review dieses Changes (nach der Rollendatei). Gib dein Votum im Format der Rollendatei ab. Prüfe insbesondere die Prüffragen der Rolle; einen Testlauf gibt es noch nicht (Vorprüfung).
> 4. `fall4/gate-log.md`: Du sollst den nächsten (vierten) Gate-Lauf ausführen. Was tust du laut Skill quality-gate als Erstes? Führe keinen Lauf aus, beschreibe nur deinen ersten Schritt und begründe ihn mit der Regelstelle.
