# Data Format Specifications

## Texts Table
- `id`: integer, primary key
- `filename`: string
- `language`: string (ISO 639-3)
- `year`: integer (CE)
- `ai_discovered`: boolean (default: false)

## Valency Patterns Table
- `id`: integer, primary key
- `text_id`: integer, foreign key to texts.id
- `verb`: string
- `pattern`: string
- `arguments`: string (comma-separated)

## Annotation JSON Example
```json
{
  "patterns": [
    { "verb": "λέγω", "pattern": "V-S-O", "arguments": ["S", "O"] },
    { "verb": "γράφω", "pattern": "V-S", "arguments": ["S"] }
  ]
}
```
