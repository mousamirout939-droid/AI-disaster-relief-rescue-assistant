# Authentication API

## `POST /api/auth/register`
```json
{ "name": "Jane Doe", "email": "jane@example.com", "password": "Password123", "phone": "+911234567890" }
```
→ `201` with `{ access_token, refresh_token, token_type }`

## `POST /api/auth/login`
```json
{ "email": "jane@example.com", "password": "Password123" }
```
→ `200` with the same token shape.

## `POST /api/auth/refresh`
```json
{ "refresh_token": "<token>" }
```
→ `200` with a new `access_token`.

## `GET /api/auth/me`
Header: `Authorization: Bearer <access_token>` → current user profile.

## `POST /api/auth/change-password`
```json
{ "old_password": "...", "new_password": "..." }
```
