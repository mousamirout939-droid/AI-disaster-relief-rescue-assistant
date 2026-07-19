# API Documentation

Full interactive docs (Swagger UI) are always available at `/docs` when the server is
running, and the raw OpenAPI schema at `/openapi.json`. This file summarizes the
resource groups; see `docs/api/*.md` for endpoint-level detail on the most-used ones.

All endpoints are prefixed with `/api` and return a consistent envelope:
```json
{ "success": true, "message": "...", "data": { ... } }
```

| Prefix | Resource | Auth |
|---|---|---|
| `/api/auth` | Register, login, refresh, change password, current user | Mixed |
| `/api/users` | Profile read/update | Required |
| `/api/admin` | Dashboard stats, user management | Admin only |
| `/api/reports` | Submit/list/update disaster reports (+ AI image analysis) | Mixed |
| `/api/disasters` | Classified disaster events | Public read, admin write |
| `/api/shelters` | Shelter CRUD + nearby search | Public read, admin write |
| `/api/hospitals` | Hospital CRUD + nearby search | Public read, admin write |
| `/api/rescue-teams` | Rescue team CRUD, nearby search, dispatch | Public read, admin write |
| `/api/ai` | Standalone image detection + chatbot | Public |
| `/api/alerts` | Weather/disaster alerts | Public read, admin write |
| `/api/notifications` | In-app notifications | Required |
| `/api/weather` | Current weather at a location | Public |
| `/api/translate` | Multi-language emergency phrases | Public |
| `/api/routes/safe` | Hazard-aware safe routing | Public |
| `/api/emergency` | SOS trigger + emergency contacts | Required |
| `/api/volunteers` | Volunteer registration + admin approval | Mixed |

See `api/authentication.md`, `api/disaster_api.md`, `api/hospital_api.md`,
`api/shelter_api.md`, `api/rescue_api.md`, `api/ai_api.md`,
`api/notification_api.md`, and `api/weather_api.md` for request/response examples.
