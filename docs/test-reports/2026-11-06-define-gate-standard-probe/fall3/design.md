# Design: Prüfung auf Geheimnisse

| Punkt | Festlegung |
|---|---|
| Muster | reguläre Ausdrücke für GitHub-Tokens, OpenAI-Schlüssel, `password=` |
| Ausgabe | Datei und Zeile, Exit 1 bei Fund |
| Zusage | Kein Geheimnis gelangt je unbemerkt in eine Spec-Datei. |
