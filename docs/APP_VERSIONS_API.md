# API Documentation: App Versions

## Overview

API for managing application versions. Supports full CRUD operations and a version check endpoint to validate if the frontend version is up to date.

**Base URL:** `/app-versions`

---

## Endpoints

### 1. Create Version

**`POST /app-versions/create`**

Creates a new app version record.

**Request Body:**

```json
{
  "version_number": 1.2,
  "platform": "Android"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version_number` | `float` | Yes | Version number (e.g. 1.0, 2.5) |
| `platform` | `string` | No | Platform name (e.g. "Android", "iOS") |

**Response (200):**

```json
{
  "id": 5,
  "result": 5
}
```

---

### 2. Get Version by ID

**`GET /app-versions/get/{id}`**

Returns a single version record by its ID.

**Path Params:**

| Param | Type | Description |
|-------|------|-------------|
| `id` | `int` | Version record ID |

**Response (200):**

```json
{
  "id": 5,
  "version_number": 1.2,
  "platform": "Android"
}
```

**Response (404):**

```json
{
  "detail": "App version not found"
}
```

---

### 3. Get All Versions

**`GET /app-versions/get_all`**

Returns all registered version records.

**Response (200):**

```json
[
  {
    "id": 1,
    "version_number": 1.0,
    "platform": "Android"
  },
  {
    "id": 2,
    "version_number": 1.1,
    "platform": "iOS"
  },
  {
    "id": 3,
    "version_number": 1.2,
    "platform": "Android"
  }
]
```

---

### 4. Update Version

**`PUT /app-versions/update/{id}`**

Updates an existing version record. Only provided fields are updated.

**Path Params:**

| Param | Type | Description |
|-------|------|-------------|
| `id` | `int` | Version record ID |

**Request Body:**

```json
{
  "version_number": 1.3,
  "platform": "Android"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version_number` | `float` | No | New version number |
| `platform` | `string` | No | New platform name |

**Response (200):**

```json
{
  "result": true
}
```

**Response (404):**

```json
{
  "detail": "App version not found"
}
```

---

### 5. Delete Version

**`DELETE /app-versions/delete/{id}`**

Deletes a version record.

**Path Params:**

| Param | Type | Description |
|-------|------|-------------|
| `id` | `int` | Version record ID |

**Response (200):**

```json
{
  "result": true
}
```

**Response (404):**

```json
{
  "detail": "App version not found"
}
```

---

### 6. Check Version (Frontend Validation)

**`GET /app-versions/check_version/{version}`**

Compares the frontend version against the latest version registered in the database. Use this to determine if the user needs to update the app.

**Logic:**

- If `frontend_version < latest_version` → returns `false` (update required)
- If `frontend_version >= latest_version` → returns `false` (no update needed)

**Path Params:**

| Param | Type | Description |
|-------|------|-------------|
| `version` | `float` | Current frontend version number |

**Response (200):**

```json
{
  "result": true
}
```

**Response examples:**

| Frontend Version | Latest DB Version | Result | Meaning |
|------------------|-------------------|--------|---------|
| `1.0` | `1.2` | `false` | Frontend is outdated, update required |
| `1.2` | `1.2` | `true` | Frontend is up to date |
| `1.5` | `1.2` | `true` | Frontend is newer than latest registered |

---

## Frontend Integration Example

```javascript
// Check if app version is up to date
async function checkAppVersion(currentVersion) {
  const response = await fetch(`/app-versions/check_version/${currentVersion}`);
  const data = await response.json();

  if (!data.result) {
    // Show update prompt to user
    showUpdateNotification();
  }
}

// Example usage
checkAppVersion(1.2);
```

---

## Database Table

```sql
CREATE TABLE public.app_versions
(
    id bigserial,
    version_number double precision,
    platform character varying(200),
    PRIMARY KEY (id)
);
```
