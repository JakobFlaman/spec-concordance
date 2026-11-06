# Befund aus einem Gate-Lauf (Change: Prüfskript für die Anforderungskonvention RC-001)

Anforderung RC-001: Im Anforderungstext darf das Schlüsselwort SHOULD nicht stehen; das Prüfskript meldet es mit Exit 1.

Fund: Der Text «Der Nutzer SH<!-- > -->OULD bestaetigen.» wird von CommonMark als «Der Nutzer SHOULD bestaetigen.» dargestellt. Das Prüfskript erkennt das zerteilte Wort nicht und endet mit Exit 0. Das Wort wird nur zerteilt, wenn jemand absichtlich einen HTML-Kommentar mit «>» mitten ins Wort setzt.

design.md des Changes, Abschnitt «Grenzen» (stand so beim Council-Review): «Nicht erkannt wird ein Schlüsselwort, das absichtlich durch komplexes Markup zerteilt ist: HTML-Kommentare oder -Tags mit `>` im Inhalt …». Die Anforderung hat keinen Sicherheitszweck.
