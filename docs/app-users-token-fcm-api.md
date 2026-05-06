# AppUsers Token FCM API

## Objetivo

Esta API separa el manejo de `token_fcm` del CRUD general de `AppUsers`.

Regla funcional:

- `token_fcm` ya no se envía ni se recibe en los endpoints generales de `AppUsers`.
- El token se maneja solo con endpoints dedicados.
- Se mantiene un solo token FCM por `AppUser`.

## Base Path

Todos los endpoints de este módulo usan el prefijo:

```text
/appUsers
```

## Contratos vigentes

### 1. Consultar token FCM por usuario

**Endpoint**

```http
GET /appUsers/{id}/token-fcm
```

**Path Params**

```json
{
  "id": 123
}
```

**Response 200**

```json
{
  "id": 123,
  "token_fcm": "fcm_token_value"
}
```

**Response 200 cuando el usuario existe pero no tiene token**

```json
{
  "id": 123,
  "token_fcm": null
}
```

**Response 404**

```json
{
  "detail": "App user not found"
}
```

### 2. Registrar o reemplazar token FCM

**Endpoint**

```http
PUT /appUsers/{id}/token-fcm
Content-Type: application/json
```

**Body**

```json
{
  "token_fcm": "fcm_token_value"
}
```

**Response 200**

```json
{
  "result": true
}
```

**Response 404**

```json
{
  "detail": "App user not found"
}
```

Notas:

- Este endpoint funciona como upsert sobre el campo `token_fcm` del usuario.
- Si el usuario existe, el token actual se reemplaza por el nuevo valor.

### 3. Eliminar token FCM en logout

**Endpoint**

```http
DELETE /appUsers/{id}/token-fcm
```

**Response 200**

```json
{
  "result": true
}
```

**Response 404**

```json
{
  "detail": "App user not found"
}
```

Notas:

- Este endpoint limpia el token del usuario y lo deja en `null` en base de datos.
- Está pensado para el flujo de logout del cliente móvil o web.

## Endpoints generales de AppUsers que ya no usan token_fcm

Estos endpoints ya no aceptan ni regresan `token_fcm`:

### POST /appUsers/create

**Request**

```json
{
  "client_id": 10,
  "name": "Juan",
  "lastname": "Perez",
  "email": "juan@correo.com",
  "password": "secret123",
  "phone_number": "5551234567"
}
```

**Response 200**

```json
{
  "id": 25,
  "result": 25
}
```

### PUT /appUsers/update/{id}

**Request permitido**

```json
{
  "name": "Juan",
  "lastname": "Perez",
  "email": "juan@correo.com",
  "password": "secret123",
  "phone_number": "5551234567",
  "client_id": 10
}
```

**Response 200**

```json
{
  "result": true
}
```

### GET /appUsers/get/{id}

**Response 200**

```json
{
  "id": 25,
  "client_id": 10,
  "name": "Juan",
  "lastname": "Perez",
  "email": "juan@correo.com",
  "password": "secret123",
  "phone_number": "5551234567"
}
```

### GET /appUsers/get_all

**Response 200**

```json
[
  {
    "id": 25,
    "client_id": 10,
    "name": "Juan",
    "lastname": "Perez",
    "email": "juan@correo.com",
    "password": "secret123",
    "phone_number": "5551234567"
  }
]
```

### GET /appUsers/by_client/{client_id}

**Response 200**

```json
[
  {
    "id": 25,
    "client_id": 10,
    "name": "Juan",
    "lastname": "Perez",
    "email": "juan@correo.com",
    "password": "secret123",
    "phone_number": "5551234567"
  }
]
```

### POST /appUsers/auth

**Request**

```json
{
  "email": "juan@correo.com",
  "password": "secret123"
}
```

**Response 200**

```json
{
  "id": 25,
  "client_id": 10,
  "client_name": "Cliente Demo",
  "name": "Juan",
  "lastname": "Perez",
  "email": "juan@correo.com",
  "phone_number": "5551234567"
}
```

**Response 401**

```json
{
  "detail": "Invalid credentials"
}
```

## Interfaces sugeridas para frontend

```ts
export interface AppUserFcmTokenResponse {
  id: number;
  token_fcm: string | null;
}

export interface AppUserUpsertFcmTokenRequest {
  token_fcm: string;
}

export interface ResponseBoolModel {
  result: boolean;
}

export interface ResponseIntModel {
  id: number;
  result: number;
}

export interface AppUserAuthResponse {
  id: number | null;
  client_id: number | null;
  client_name: string | null;
  name: string | null;
  lastname: string | null;
  email: string | null;
  phone_number: string | null;
}

export interface AppUserResponse {
  id: number;
  client_id: number | null;
  name: string | null;
  lastname: string | null;
  email: string | null;
  password: string | null;
  phone_number: string | null;
}
```

## Flujo recomendado para frontend

1. Autenticar al usuario con `POST /appUsers/auth`.
2. Obtener el `id` del usuario autenticado.
3. Cuando el cliente obtenga o refresque el token de Firebase, llamar `PUT /appUsers/{id}/token-fcm`.
4. Si se necesita depurar estado del dispositivo, usar `GET /appUsers/{id}/token-fcm`.
5. En logout, llamar `DELETE /appUsers/{id}/token-fcm`.

## Reglas importantes para el agente de frontend

- No mandar `token_fcm` en `POST /appUsers/create`.
- No mandar `token_fcm` en `PUT /appUsers/update/{id}`.
- No esperar `token_fcm` en `GET /appUsers/get/{id}`.
- No esperar `token_fcm` en `GET /appUsers/get_all`.
- No esperar `token_fcm` en `GET /appUsers/by_client/{client_id}`.
- No esperar `token_fcm` en `POST /appUsers/auth`.
- El único origen de verdad para el token es `GET /appUsers/{id}/token-fcm`.
- El único endpoint para registrar o reemplazar token es `PUT /appUsers/{id}/token-fcm`.
- El único endpoint para limpiar token en logout es `DELETE /appUsers/{id}/token-fcm`.

## Ejemplos rápidos con fetch

### Registrar token

```ts
await fetch(`/appUsers/${userId}/token-fcm`, {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ token_fcm: fcmToken }),
});
```

### Consultar token

```ts
const response = await fetch(`/appUsers/${userId}/token-fcm`);
const data = await response.json();
```

### Limpiar token en logout

```ts
await fetch(`/appUsers/${userId}/token-fcm`, {
  method: "DELETE",
});
```