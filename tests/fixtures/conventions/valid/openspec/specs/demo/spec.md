## Purpose

Testdaten: gültige Anforderungen nach der Konvention.

## Requirements

### Requirement: Volltextsuche (LA-F-105, Must)
Das System SHALL Text finden. Die Wörter `SHOULD` und «MAY» sind hier nur erwähnt.

#### Scenario: Suche
- **WHEN** gesucht wird
- **THEN** SHOULD in einem Szenario ist keine Anforderung

### Requirement: Suche über Dokumente (LA-F-105, Should)
Das System SHALL über mehrere Dokumente suchen.

#### Scenario: Zwei Dokumente
- **WHEN** zwei Dokumente offen sind
- **THEN** werden beide durchsucht

### Requirement: Vorlesen (LA-F-112, Could)
Das System SHALL vorlesen.

#### Scenario: Vorlesen
- **WHEN** vorlesen gewählt wird
- **THEN** wird vorgelesen

### Requirement: Startzeit (N-001, Must)
Das System SHALL in 2 s starten.

#### Scenario: Start
- **WHEN** gestartet wird
- **THEN** ist das Fenster nach 2 s bedienbar

### Requirement: Darstellungsmodi (LA-F-110, Should)
Das System SHALL einen Dunkelmodus bieten. Ein deutsches Zitat „MAY“ ist eine Erwähnung.

```text
Beispiel aus einer Quelle: The system SHOULD support dark mode.
```

#### Scenario: Dunkel
- **WHEN** umgeschaltet wird
- **THEN** ist es dunkel
