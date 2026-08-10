# API CreateDocuments - Contexto para Frontend

## Endpoint
```
POST /createDocuments/
```

## Body (JSON)
```json
{
  "GC": null,
  "fole": false,
  "foim": false,
  "fosp": false,
  "fosc": false,
  "foos": false,
  "fobc": false,
  "foem": false,
  "fopc02": false,
  "fopp02": false,
  "employee_id": 1,
  "equipment_id": 1,
  "date_created": "2026-08-07",
  "status": "Abierto"
}
```

## Campos del Body

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| GC | string \| null | null | Código GC (si se envía, NO genera file) |
| fole | boolean | false | Formato: Levantamiento (FO-LE-01) |
| foim | boolean | false | Formato: Inspección (FO-IM-01) |
| fosp | boolean | false | Formato: Servicio (FO-SP-01) |
| fosc | boolean | false | Formato: Servicio con cliente (FO-SC-01) |
| foos | boolean | false | Formato: Orden de servicio (FO-OS-01) |
| fobc | boolean | false | Formato: Bitácora de carga (FO-BC-01) |
| foem | boolean | false | Formato: Empleo (FO-EM-01) |
| fopc02 | boolean | false | Formato: Préstamo de equipo (FO-PC-02) |
| fopp02 | boolean | false | Formato: Préstamo de piezas (FO-PP-02) |
| employee_id | number | (requerido) | ID del empleado |
| equipment_id | number | (requerido) | ID del equipo |
| date_created | string | "YYYY-MM-DD" (hoy) | Fecha de creación |
| status | string | "Abierto" | Estado del documento |

## Comportamiento de Generación de File

| Genera file | Formatos |
|-------------|----------|
| ✅ Sí | fosp, fosc, foos, fobc, foem |
| ❌ No | fole, foim |
| ❌ No | fopc02, fopp02 |

**Regla**: Se genera UN SOLO file compartido para todos los formatos que lo requieran en la misma petición.

**Excepción**: Si `GC` tiene valor, NO se genera file aunque se envíen formatos que normalmente lo generan.

## Ejemplo: Crear solo fosp (genera file)
```json
{
  "fosp": true,
  "employee_id": 5,
  "equipment_id": 10
}
```

## Ejemplo: Crear fosp + fosc + fopc02 (genera 1 file)
```json
{
  "fosp": true,
  "fosc": true,
  "fopc02": true,
  "employee_id": 5,
  "equipment_id": 10
}
```

## Ejemplo: Crear fole + foim (NO genera file)
```json
{
  "fole": true,
  "foim": true,
  "employee_id": 5,
  "equipment_id": 10
}
```

## Ejemplo: Crear fopc02 + fopp02 (NO genera file)
```json
{
  "fopc02": true,
  "fopp02": true,
  "employee_id": 5,
  "equipment_id": 10
}
```

## Respuesta
- **Éxito**: `true` (boolean)
- **Error**: Excepción con mensaje de error

## Notas para el Modal
1. El usuario selecciona qué formatos crear con checkboxes o toggle switches
2. Los formatos fopc02 y fopp02 son nuevos - agregar al menú/modal
3. No es necesario mostrar info de file al usuario, el sistema lo gestiona internamente
4. Se pueden crear múltiples formatos en una sola petición
