## ADDED Requirements

### Requirement: Umpriorisierung erklären (RC-010, Must)
Das System SHALL das Beispiel zeigen:

```markdown
## RENAMED Requirements

- FROM: `### Requirement: Darstellungsmodi (LA-F-110, Should)`
- TO: `### Requirement: Darstellungsmodi (LA-F-110, Must)`

### Requirement: Beispiel ohne Priorität (X)
```

Das System SHOULD zusätzlich warnen.

#### Scenario: Beispiel
- **WHEN** das Beispiel gezeigt wird
- **THEN** ist es sichtbar

### Requirement: Ohne Priorität (RC-011)
Das System MAY etwas tun.

#### Scenario: Etwas
- **WHEN** etwas
- **THEN** etwas
