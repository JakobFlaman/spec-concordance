# Befund aus einem Gate-Lauf (Change: Prüfskript für die Anforderungskonvention RC-001)

Anforderung RC-001: Im Anforderungstext darf das Schlüsselwort SHOULD nicht stehen; das Prüfskript meldet es mit Exit 1.

Fund: Eine Spec-Datei enthält unter einem Listenpunkt einen eingerückten Codeblock, dessen Schliesser versehentlich in Spalte 1 steht (häufiger Fehler beim Einfügen von Codebeispielen). Danach lesen OpenSpec und CommonMark alle folgenden Codeblöcke versetzt. Ein später folgender, normal formatierter Satz «Der Nutzer SHOULD bestaetigen.» wird von CommonMark als Text dargestellt, das Prüfskript blendet ihn aber als Code aus und endet mit Exit 0.

In design.md des Changes steht keine Grenze, die diesen Fall ausnimmt.
