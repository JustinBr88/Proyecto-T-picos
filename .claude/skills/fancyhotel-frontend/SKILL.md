---
name: fancyhotel-frontend
description: >
  Convenciones del frontend de Fancy Hotel (AngularJS 1.4, Bootstrap 3, Eonasdan
  bootstrap-datetimepicker, sin build): factories, controladores, rutas y vistas.
  Trigger: al modificar fancyhotel/static/ (controllers.js, views/*.html, libs) o
  templates/index.html, o al agregar pantallas, calendarios o gráficos.
license: Apache-2.0
metadata:
  author: equipo-fancyhotel
  version: "1.0"
---

## Cuándo usarla

- Agregar una pantalla, un formulario o una llamada a la API desde el navegador.
- Trabajar con el selector de fechas (Caso 2) o con gráficos (Caso 3).

## Cómo está armado

| Pieza | Dónde | Qué es |
|---|---|---|
| Página principal | `fancyhotel/templates/index.html` | Carga AngularJS, Bootstrap, jQuery, moment y el datetimepicker por `<script>`. **No hay npm ni build.** |
| Factories | `static/js/controllers.js` (arriba, módulo `resourceModule`) | Un `$resource` por dominio: `authFactory`, `reservationFactory`, `paymentFactory`, `reviewFactory`, `reportFactory`. |
| Controladores | `static/js/controllers.js` (módulo `FancyHotelApp`) | Uno por área: `reservationController` atiende buscar, reservar, actualizar y cancelar. |
| Rutas | `.config($routeProvider)` al final de `controllers.js` | `#/ruta` → vista + controlador. |
| Vistas | `static/views/*.html` | Plantillas que se cargan en `<div ng-view>`. |
| Sesión | `$rootScope.currentUser` / `$rootScope.userType` | Sólo en memoria: se pierde al recargar. El rol sale de la 1ª letra del usuario (`C` o `M`). |

## Reglas críticas

| Regla | Por qué |
|---|---|
| El selector de fechas es **Eonasdan bootstrap-datetimepicker** aunque el archivo se llame `bootstrap-datepicker.js`. API: `$(el).datetimepicker({...})`, `$(el).data("DateTimePicker")`, eventos `dp.change` / `dp.update`. Para deshabilitar días: opción `disabledDates`. **No existe `beforeShowDay`.** | Error ya cometido por la IA (ver AI_LOG): no asumir la librería por el nombre del archivo. |
| Toda llamada HTTP pasa por una acción de una factory (`$resource`), nunca `$http` o `$.ajax` sueltos. | Mantiene todas las URLs de la API en un solo lugar. |
| En GET/DELETE los parámetros viajan en la query string; en POST/PUT, en el cuerpo JSON. | El backend declara `location="args"` o `"json"` por argumento. |
| Una acción que devuelve una lista lleva `isArray: true`. | Si no, `$resource` falla al parsear. |
| Las fechas viajan como texto `YYYY-MM-DD`. | Es el formato que parsea el backend. |
| Librerías nuevas: por CDN con versión exacta (p. ej. Chart.js para el Caso 3) en `index.html`, o copiadas a `static/libs/`. | No hay bundler. |
| Mostrar sólo los últimos 4 dígitos de una tarjeta. | CA1.4 y Caso 4. |
| No migrar a otro framework ni rediseñar: fuera de alcance (SPEC §2). | Tiempo del proyecto. |

## Agregar una pantalla (receta)

1. Vista en `static/views/miPantalla.html`.
2. Si llama a la API: acción nueva en la factory del dominio.
3. Controlador nuevo (o reutilizar el del área) en `controllers.js`.
4. Ruta en `.config($routeProvider)`.
5. Enlace desde `selectionPage.html` (portal) si corresponde.
6. Caso de prueba manual para QA en el PR (no hay tests automáticos de UI).

## Ejemplos

```javascript
// Factory: nueva acción
resourceModule.factory('reservationFactory', function($resource){
    return $resource('/api', {}, {
        // ...acciones existentes...
        GetAvailability: { method: 'GET', url: '/api/availability' }
    })
})

// Controlador: llamada y uso del resultado
reservationFactory.GetAvailability({ location: $scope.location, month: '2026-11' })
    .$promise.then(function(data){
        var fullDays = data.days.filter(function(d){ return d.status === 'lleno'; })
                                .map(function(d){ return moment(d.date); });
        $('#startDatePicker').data('DateTimePicker').disabledDates(fullDays);
    });
```

## Comandos

```bash
python run.py   # http://localhost:5000 — recargar el navegador tras cambiar JS/HTML
```

## Recursos

- Controladores, factories y rutas: [fancyhotel/static/js/controllers.js](../../../fancyhotel/static/js/controllers.js)
- Criterios de UI por caso: [docs/SPEC.md](../../../docs/SPEC.md) (CA2.5–CA2.7, CA3.3)
