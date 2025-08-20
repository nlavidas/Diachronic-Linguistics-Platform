# API Documentation

## Base URL
`http://localhost:8000/api`

### Endpoints

#### `GET /texts`
- List all collected texts and their metadata.
- Response: `[{ id, filename, language, year, ai_discovered }]`

#### `GET /annotations/{text_id}`
- Get valency patterns/annotations for a given text.
- Response: `[{ verb, pattern, arguments }]`

#### `POST /publish`
- Register a new text (metadata only).
- Body: `{ filename, language, year }`
- Response: `{ status: "ok", id }`

#### `GET /valency/search`
- Search valency patterns (by pattern, language, year, etc.)

#### `GET /valency/changes`
- Get diachronic statistics for visualization.

#### `GET /parallel?work=...`
- Get parallel translations for a work.

---

## Error Codes
- 404: Not found
- 400: Bad request
- 500: Internal error

---

## Example Usage
```sh
curl http://localhost:8000/api/texts
curl http://localhost:8000/api/annotations/1
```
