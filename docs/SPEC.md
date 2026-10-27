# Especificación — Proyecto 1: Feature Sprint con IA

**Materia:** Tópicos Especiales II — Prof. Regis Rivera
**Equipo:** Ana · Justin · Bethel
**Repositorio:** https://github.com/JustinBr88/Proyecto-T-picos
**App base:** https://github.com/thegrucoder/Hotel-Reservation-System ("Fancy Hotel")

> Lo que se evalúa es el **proceso**: cómo se usó la IA, cómo se validó, qué se corrigió y qué se rechazó. No cuánto código generó.

---

## 1. Estado actual de la app base (análisis previo)

| Aspecto | Realidad del código | Impacto |
|---|---|---|
| Backend | Python **2** + Flask + flask_restful (`fancyhotel/serve.py`, `api.py`) | No corre en Python 3 (`print x`). Hay que migrar. |
| Frontend | **AngularJS 1.4** + Bootstrap 3 + **Eonasdan bootstrap-datetimepicker** (el archivo se llama `bootstrap-datepicker.js`, pero es otra librería) | No es "JS sin framework" como dice la tabla del enunciado. |
| Base de datos | MySQL; el esquema se crea en `MysqlManager.init_db()` | Credenciales `root/password` hardcodeadas. |
| Datos | No hay seed (`#fill db with existing data here` vacío) | Sin habitaciones la búsqueda nunca devuelve resultados. |
| Tests | Ninguno | Hay que montar pytest desde cero. |
| Roles | El login decide el rol por la 1ª letra del usuario (`C` cliente / `M` manager), `username CHAR(5)` | Frágil, pero fuera de alcance salvo que sobre tiempo. |
| Seguridad | Contraseñas y CVV en texto plano | Se aborda en el Caso 4. |

### Bugs conocidos detectados al leer el código

Las rutas indicadas son las de la app original; entre paréntesis, dónde quedó el código después del Caso 0.

| ID | Ubicación | Descripción | Estado |
|---|---|---|---|
| BUG-1 | `db/mysqldb.py` → `search_rooms`, `is_room_free` (hoy `fancyhotel/db/rooms.py`) | La condición de ocupado (`checkin >= X AND checkout <= Y`) sólo detecta reservas **contenidas** en el rango buscado; no detecta solapamientos parciales → doble reserva. De 4 formas de solapamiento sólo detectaba una (la búsqueda que envuelve a la reserva). | Resuelto en Caso 2 (además, crear una reserva ahora valida disponibilidad) |
| BUG-2 | `api.py` → `ReservationResource.put` (hoy `fancyhotel/api/reservations.py`) | `PUT /api/reservation/<id>` usa `deltaDays` sin definirlo (`NameError`) y llama a `update_reservation` con argumentos equivocados. El frontend **no** lo usa (llama a `PUT /api/reservation` con el id en el cuerpo), así que no afectaba a la UI. | Resuelto en Caso 0 |
| BUG-3 | `db/mysqldb.py` → `user_exists` (hoy `fancyhotel/db/users.py`) | Consulta `FROM customer` en minúscula; en MySQL sobre Linux (Docker) los nombres de tabla distinguen mayúsculas. | Resuelto en Caso 0 |
| BUG-4 | Todos los recursos con `reqparse` | Con Flask 3, flask-restful responde **415** a los GET porque intenta leer un cuerpo JSON; y `type=list` convierte cada habitación (un dict) en la lista de sus claves. | Resuelto en Caso 0 |
| BUG-5 | `db/mysqldb.py` → `cancel_reservation` | Mezcla de tab y espacio en la indentación: `TabError` en Python 3. | Resuelto en Caso 0 |
| BUG-6 | `static/js/controllers.js` → `searchAvailability` (línea ~481) | Lee `successData.data['rooms']`, pero `$resource` entrega la respuesta directa (`successData.rooms`): `TypeError` en consola y la pantalla "Actualizar reserva" muestra costo 0. El backend guarda bien el costo. | Pendiente (bug del original) |

---

## 2. Alcance

### Dentro
- Caso 0 (habilitador técnico) + 5 historias de usuario (3 obligatorias, 2 propias).
- Pruebas automatizadas por historia.
- AI Development Log y evidencias exigidas por el enunciado.

### Fuera
- Rediseño visual completo o migración del front a otro framework.
- Rehacer el sistema de roles/autenticación (más allá de lo que pide el Caso 4).
- Despliegue en la nube.

---

## 3. Casos e historias de usuario

| Caso | Historia | Dev | Reviewer | QA |
|---|---|---|---|---|
| 0 | Puesta en marcha técnica | Todo el equipo | — | — |
| 1 | Reserva con datos de pago guardados | Ana | Justin | Bethel |
| 2 | Calendario dinámico de disponibilidad | Justin | Bethel | Ana |
| 3 | Gráficos de previsión de demanda | Bethel | Ana | Justin |
| 4 | Seguridad de credenciales | Ana | Bethel | Justin |
| 5 | Gestión de habitaciones (admin) | Bethel | Justin | Ana |

Los criterios de aceptación usan el formato *Dado / Cuando / Entonces*. Cada criterio debe tener al menos un test automatizado o, si no es automatizable (UI), un caso de prueba manual documentado por QA.

---

### Caso 0 — Puesta en marcha técnica (habilitador)

> Como equipo de desarrollo, queremos la app base funcionando en Python 3 con datos de prueba y pytest, para poder desarrollar y probar las historias sobre una base estable.

**Criterios de aceptación**
- **CA0.1** Dado un clon limpio, cuando se siguen los pasos del README, entonces la app arranca en `localhost:5000` con Python 3.12.
- **CA0.2** La conexión a MySQL se configura con variables de entorno (archivo `.env` opcional, fuera del repo). Los únicos valores en el código son los por defecto del contenedor local de desarrollo.
- **CA0.3** Existe un script de seed que crea: managers, clientes, habitaciones en al menos 2 locaciones y **un histórico de reservas de 12–18 meses** (lo necesita el Caso 3).
- **CA0.4** `pytest` corre y pasa con al menos un test de humo (la app levanta y `/api/searchRoom` responde).
- **CA0.5** Los tests usan una base separada (`Fancy_Hotel_test`) y nunca tocan la de desarrollo.
- **CA0.6** Flujo actual verificado manualmente tras la migración: registro, login, búsqueda, reserva, cancelación y reportes.

---

### Caso 1 — Reserva con datos de pago guardados

> Como usuario recurrente, quiero reservar directamente usando mis datos guardados, para no tener que rellenar el formulario de pago en cada compra.

**Contexto en el código:** ya existen la tabla `Credit_Card`, `/api/payment` (GET/POST/DELETE) y `payment.html`. Hoy el usuario elige una tarjeta en cada reserva.

**Criterios de aceptación**
- **CA1.1** Dado un cliente con una o más tarjetas guardadas, cuando marca una como predeterminada, entonces queda persistida como tal (sólo una por usuario).
- **CA1.2** Dado un cliente con tarjeta predeterminada, cuando confirma una reserva, entonces la tarjeta viene preseleccionada y puede reservar sin abrir el formulario de pago.
- **CA1.3** Dado un cliente sin tarjetas, cuando intenta reservar, entonces se le ofrece agregar una (y opcionalmente guardarla como predeterminada).
- **CA1.4** La interfaz sólo muestra los últimos 4 dígitos de la tarjeta.
- **CA1.5** No se puede usar una tarjeta vencida; el sistema lo indica.
- **CA1.6** Un usuario no puede usar ni ver tarjetas de otro usuario.

**Dependencia:** coordinar con el Caso 4 (eliminación del CVV). El Caso 1 **no debe depender** del CVV almacenado.

---

### Caso 2 — Calendario dinámico de disponibilidad

> Como cliente, quiero ver un calendario dinámico con los días disponibles y ocupados, para elegir mi fecha rápidamente sin intentos fallidos.

**Criterios de aceptación**
- **CA2.1** (BUG-1) Dada una reserva del día 10 al 15, cuando se busca del 12 al 20, entonces esa habitación **no** aparece como libre. Se cubre el solapamiento en ambos extremos, la contención total y el rango que envuelve a la reserva.
- **CA2.2** Check-out y check-in el mismo día no se consideran solapamiento (la noche del check-out queda libre).
- **CA2.3** Las reservas canceladas no ocupan días.
- **CA2.4** Existe `GET /api/availability?location=&month=YYYY-MM` que devuelve el estado de cada día del mes: `lleno` (ninguna habitación libre), `parcial` (quedan pocas: **30 % o menos** libres) o `libre` (el resto), junto con la cantidad de habitaciones libres. *Cambio respecto de la versión inicial ("parcial" = alguna ocupada): ver AI_LOG, decisión humana #8.*
- **CA2.5** Dado que el cliente elige una locación, cuando abre el selector de fechas, entonces los días `lleno` aparecen deshabilitados (opción `disabledDates` de bootstrap-datetimepicker) y los `parcial` se distinguen visualmente (la librería no lo trae: hay que marcarlos con CSS sobre el widget, por ejemplo en el evento `dp.update`).
- **CA2.6** Las fechas pasadas no se pueden seleccionar.
- **CA2.7** Al cambiar de mes o de locación, el calendario se actualiza sin recargar la página.

**Nota de diseño:** extraer la regla de solapamiento a una función pura (`overlaps(a_in, a_out, b_in, b_out)`) testeable sin base de datos, y usar la condición correcta en SQL: `res.checkin_date < :checkOut AND res.checkout_date > :checkIn`.

---

### Caso 3 — Gráficos de previsión de demanda

> Como administrador del sistema, quiero ver gráficos de previsión de la demanda basados en el histórico, para ajustar los precios y el inventario de forma inteligente.

**Contexto en el código:** ya existen los reportes `reservation_report`, `room_report` y `revenue_report` (rutas `/api/reports/*`, código en `fancyhotel/db/reports.py`). Ojo: están fijos a agosto y septiembre.

**Criterios de aceptación**
- **CA3.1** Existe `GET /api/reports/forecast?location=&type=` que devuelve una serie mensual histórica (noches reservadas u ocupación %) y una previsión de los próximos 3 meses.
- **CA3.2** El método de previsión es simple y explicable (p. ej. media móvil o regresión lineal con estacionalidad mensual) y está documentado en el código y en el AI Log.
- **CA3.3** El gráfico (Chart.js) diferencia visualmente lo histórico de lo previsto y se puede filtrar por locación y tipo de habitación.
- **CA3.4** Con menos de 3 meses de histórico, el sistema indica "datos insuficientes" en lugar de inventar una previsión.
- **CA3.5** Sólo los managers acceden a la vista y al endpoint.
- **CA3.6** El cálculo de la previsión es una función pura con tests sobre datos conocidos (p. ej. una serie constante debe prever el mismo valor).

**Dependencia:** necesita el histórico del seed (CA0.3).

---

### Caso 4 — Seguridad de credenciales (historia propia)

> Como cliente, quiero que mi contraseña se guarde cifrada y que el sistema nunca almacene el CVV de mi tarjeta, para que mis datos estén protegidos si la base de datos se filtra.

**Criterios de aceptación**
- **CA4.1** Las contraseñas nuevas se guardan con hash (bcrypt o equivalente); la columna nunca contiene el texto plano.
- **CA4.2** El login valida contra el hash; las credenciales incorrectas siguen devolviendo 401.
- **CA4.3** Existe un script de migración que hashea las contraseñas existentes del seed.
- **CA4.4** El CVV se pide en el formulario pero **no se persiste** (se elimina la columna `cvv` o deja de usarse).
- **CA4.5** La columna `password` admite la longitud del hash (hoy es `VARCHAR(16)`).
- **CA4.6** Los tests verifican que tras registrar un usuario el valor guardado no es igual a la contraseña.

**Dependencia:** se desarrolla después de mergear el Caso 1 (ambos tocan `Credit_Card`).

---

### Caso 5 — Gestión de habitaciones por el administrador (historia propia)

> Como administrador, quiero crear habitaciones y modificar su precio desde un panel, para ajustar el inventario sin tocar la base de datos.

**Criterios de aceptación**
- **CA5.1** Un manager puede listar las habitaciones por locación.
- **CA5.2** Un manager puede crear una habitación (locación, número, tipo, costo, capacidad, precio de cama extra) con validación de campos.
- **CA5.3** No se puede crear una habitación duplicada (misma locación + número).
- **CA5.4** Un manager puede modificar el costo y el precio de cama extra; el cambio **no altera** el `total_cost` de las reservas ya hechas.
- **CA5.5** Los clientes no pueden acceder al panel ni a los endpoints (403).
- **CA5.6** Desde la vista de previsión (Caso 3) hay un acceso directo al panel para ajustar el precio de esa locación/tipo.

**Dependencia:** CA5.6 requiere el Caso 3 mergeado; el resto es independiente.

---

## 4. Requisitos no funcionales

- **RNF1** Python 3.12, dependencias fijadas en `requirements.txt`.
- **RNF2** Ninguna credencial o secreto en el repositorio.
- **RNF3** Consultas SQL siempre parametrizadas (ya es el patrón del código; se mantiene).
- **RNF4** Los cambios no rompen los flujos existentes (registro, login, búsqueda, reserva, actualización, cancelación, reseñas, reportes).

---

## 5. Reglas de trabajo

### Git
- Dos ramas permanentes, ambas protegidas (sólo se entra por Pull Request aprobado):
  - `develop`: integración. Las ramas de cada caso salen de `develop` y vuelven a `develop`.
  - `main`: versión estable y entregable. Sólo recibe un PR `develop → main` cuando lo integrado pasó la regresión (fin de cada fase y entrega final).
- Una rama por caso: `feature/caso-N-descripcion` (p. ej. `feature/caso-2-calendario`). Correcciones: `fix/descripcion`.
- Commits con Conventional Commits y referencia al issue: `feat(calendar): add availability endpoint (#3)`.
- Cada historia es un **issue** en GitHub con los criterios de aceptación como checklist y la etiqueta `caso-N`.

### Pull Requests
- Lo abre el Dev; lo aprueba el **Reviewer** del caso; el **QA** deja constancia de las pruebas en un comentario.
- Plantilla mínima: qué cambia, issue que cierra, cómo probar, evidencia de tests, uso de IA en este PR.
- No se mergea con tests en rojo.

### Definition of Done (por historia)
1. Todos los criterios de aceptación cumplidos.
2. Tests automatizados escritos y pasando.
3. Revisión de código aprobada por el Reviewer.
4. QA validó los criterios y documentó el resultado en el PR.
5. Entradas del AI Log registradas para ese caso.
6. Mergeado a `develop` y issue cerrado (GitHub sólo cierra solo los issues al mergear en `main`: cerrarlo a mano con referencia al PR).

### Estrategia de pruebas
- **Unitarias** (sin BD): lógica pura — solapamiento de fechas, previsión, hash de contraseñas, validaciones.
- **Integración**: endpoints con el cliente de pruebas de Flask contra `Fancy_Hotel_test`.
- **Manual (QA)**: flujos de UI con casos documentados en el PR.

---

## 6. Evidencia del uso de IA

Archivo `docs/AI_LOG.md`, completado **durante** el desarrollo, nunca reconstruido al final.

| Fecha | Caso | Quién | Actividad | Herramienta IA | Qué se solicitó | Resultado | Decisión humana | Evidencia (commit/PR) |
|---|---|---|---|---|---|---|---|---|

Además, tres secciones obligatorias (cubren las restricciones 8, 9 y 10):
- **Respuestas incorrectas de la IA**: qué propuso, por qué estaba mal, cómo se detectó.
- **Cambios rechazados**: qué se descartó y por qué.
- **Decisiones humanas**: decisiones de diseño tomadas por el equipo, con su justificación.

No hace falta registrar cada prompt; sólo los que afectaron significativamente al desarrollo.

---

## 7. Trazabilidad con las restricciones del enunciado

| # | Restricción | Dónde se cumple |
|---|---|---|
| 1 | Repositorio Git | `JustinBr88/Proyecto-T-picos` |
| 2 | Issues / historias | Un issue por caso (0–5) |
| 3 | Commits identificables | Conventional Commits + `#issue` |
| 4 | Uso de ramas | `feature/caso-N-*` |
| 5 | Pull Request | Un PR por caso, aprobado por el Reviewer |
| 6 | Pruebas automatizadas | pytest (unitarias + integración) |
| 7 | Evidencia de IA | `docs/AI_LOG.md` |
| 8 | Respuestas incorrectas | Sección en `AI_LOG.md` |
| 9 | Cambios rechazados | Sección en `AI_LOG.md` + comentarios de PR |
| 10 | Decisiones humanas | Sección en `AI_LOG.md` |
