---
name: fancyhotel-testing
description: >
  Cómo escribir y correr las pruebas de Fancy Hotel con pytest (unitarias sin BD,
  integración contra MySQL) y cómo documentar pruebas manuales de QA.
  Trigger: al escribir o arreglar tests, al implementar lógica de negocio nueva,
  al cerrar un criterio de aceptación o al hacer de QA en un PR.
license: Apache-2.0
metadata:
  author: equipo-fancyhotel
  version: "1.0"
---

## Cuándo usarla

- Antes de implementar lógica nueva (test primero).
- Al cerrar un criterio de aceptación del SPEC: cada criterio necesita un test o un caso manual.
- Al hacer de QA en un Pull Request.

## Unitario o integración

| Qué se prueba | Tipo | Carpeta |
|---|---|---|
| Función pura: solapamiento de fechas, cálculo de precio, previsión, validación, hash | Unitario (sin BD) | `tests/unit/` |
| Endpoint completo (HTTP → SQL → respuesta) | Integración | `tests/integration/` |
| Pantalla del navegador | Manual (QA) | Caso en el PR |

## Reglas críticas

- **Test primero** para la lógica pura: escribir el test que falla, verlo fallar y recién después implementar.
- Un archivo de integración por dominio (`test_reservations.py`, `test_payments.py`…), con `pytestmark = pytest.mark.integration`.
- La base de tests (`Fancy_Hotel_test`) **se borra y se recrea antes de cada test**: cada test arma sus propios datos y no depende del orden.
- Datos fijos compartidos en `tests/support.py` (`CUSTOMER`, `MANAGER`, `CARD_NUMBER`, `ROOMS`, `LOCATION`). No duplicarlos.
- Fechas **siempre relativas a hoy** con `future(días)`; nunca fechas fijas (el test caduca).
- Para crear reservas usar la fixture `make_reservation(check_in_days=, nights=, room=, extra_bed=)`.
- Un bug corregido lleva un test de regresión con el ID del bug en el docstring (`"""Regresión BUG-1: ..."""`).
- Nombres que describen el comportamiento: `test_cancelled_reservation_frees_the_room`, no `test_cancel_2`.
- Si un test de la IA está mal (asserts triviales o que no prueban el criterio), se corrige y se anota en el AI Log.
- No se mergea con tests en rojo. Los *skipped* por falta de MySQL no cuentan como verdes: levantar Docker y correrlos.

## Ejemplos

```python
# tests/unit/test_overlap.py — lógica pura, sin BD
from fancyhotel.db.rooms import overlaps

def test_partial_overlap_at_start_is_detected():
    """Regresión BUG-1: reserva 10–15, búsqueda 12–20."""
    assert overlaps("2026-11-10", "2026-11-15", "2026-11-12", "2026-11-20")

def test_checkout_day_equal_to_checkin_day_is_not_overlap():
    assert not overlaps("2026-11-10", "2026-11-15", "2026-11-15", "2026-11-18")
```

```python
# tests/integration/test_reservations.py — endpoint completo
import pytest
from tests.support import LOCATION, ROOMS, future

pytestmark = pytest.mark.integration

def test_reserved_room_is_not_offered_for_overlapping_dates(client, make_reservation):
    make_reservation(check_in_days=10, nights=5, room=ROOMS[0])
    response = client.get("/api/searchRoom", query_string={
        "location": LOCATION, "checkIn": future(12), "checkOut": future(20)})
    assert [r["room_number"] for r in response.get_json()["response"]] == [102]
```

## Caso de prueba manual (QA, en el comentario del PR)

```markdown
**CA2.5** — Días llenos deshabilitados
- Datos: `flask --app fancyhotel seed-db`, usuario `Cdemo` / `demo1234`
- Pasos: Portal → Buscar habitación → Atlanta → abrir el calendario
- Esperado: los días sin habitaciones libres aparecen deshabilitados
- Resultado: ✅ / ❌ (captura)
```

## Comandos

```bash
docker compose exec app pytest   # todo, dentro del contenedor (con `docker compose up` corriendo)
docker compose up -d mysql    # o: sólo MySQL, para correrlos desde el venv local
pytest                        # todo
pytest tests/unit             # sólo unitarios (sin MySQL)
pytest -m integration         # sólo integración
pytest -k overlap -v          # filtrar por nombre
```

## Recursos

- Fixtures: [tests/conftest.py](../../../tests/conftest.py) · Datos compartidos: [tests/support.py](../../../tests/support.py)
- Criterios de aceptación: [docs/SPEC.md](../../../docs/SPEC.md) §3 · Estrategia: §5
