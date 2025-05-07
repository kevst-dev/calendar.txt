# Guía de Uso: `calendar.txt`

Este documento describe el formato y las convenciones utilizadas en el archivo `calendar.txt`, diseñado para una gestión de calendario simple y eficaz basada en texto plano.

## Filosofía

- **Texto Plano:** Fácil de leer, editar, buscar y procesar con herramientas estándar.
- **Simpleza:** Estructura mínima pero suficiente para organizar el tiempo.
- **Flexibilidad:** Adaptable a necesidades personales y fácil de extender.
- **Portabilidad:** Funciona en cualquier dispositivo con un editor de texto.
- **Automatización:** Un script ayuda a mantener el calendario ordenado, archivar el pasado y preparar el futuro.

## Archivos Utilizados

El sistema se compone principalmente de tres archivos:

1.  **`calendar.txt` (Archivo Principal):** Contiene los eventos y tareas para los días actuales y futuros. Es el archivo que consultarás y editarás con más frecuencia.

2.  **`calendar_archive.txt` (Archivo Histórico):** Almacena los bloques diarios de días que ya han pasado. El script mueve automáticamente los días pasados desde `calendar.txt` a este archivo para mantener el archivo principal manejable. Tiene exactamente el mismo formato que `calendar.txt`.

3.  **`recurring.txt` (Reglas Recurrentes):** Define eventos o tareas que se repiten anualmente, mensualmente o semanalmente. El script utiliza este archivo para añadir automáticamente estos eventos a los días correspondientes en `calendar.txt`.

## Estructura General

Los archivos `calendar.txt` y `calendar_archive.txt` comparten la misma estructura, organizada en bloques diarios. Cada bloque representa un día y contiene un encabezado seguido de una o más líneas de eventos o tareas.

```
<<Encabezado Diario>>
+ <<Línea de Evento/Tarea>>
+ <<Línea de Evento/Tarea>>

<<Encabezado Diario Siguiente>>
+ <<Línea de Evento/Tarea>>
```

Se recomienda separar los bloques diarios con una línea en blanco para mejorar la legibilidad.

## Formato del Encabezado Diario

Cada día comienza con una línea que sigue este formato:

```
+ YYYY-MM-DD nombre_dia [Ubicacion]
```

### Descripción del encabezado

- **`YYYY-MM-DD`**: Fecha en formato ISO 8601 (Año-Mes-Día). Esto asegura un orden cronológico correcto al ordenar el archivo.

- **`nombre_dia`**: Nombre del día de la semana en minúsculas (lunes, martes, etc.). Facilita la lectura humana.

- **`[Ubicacion]`**: Indicador opcional del tipo de jornada o ubicación principal del día. Se usan las siguientes abreviaturas (o las que definas):

  - `[V]`: Trabajo Virtual / Remoto.
  - `[P]`: Trabajo Presencial / En la oficina.
  - `[L]`: Día Libre / Personal / No laboral.
  - `[?]`: Ubicación por definir o flexible.
  - _Puedes omitirlo si no aplica o no quieres usarlo._

**Ejemplo:**

```
2025-04-22 martes [P]
+ ...
+ ...
+ ...

2025-04-26 sábado [L]
+ ...
+ ...
```

## Formato de Líneas de Evento/Tarea

Debajo del encabezado diario, cada línea representa una actividad específica para ese día:

- **`+`**: Indica que es un evento.
- **`HH:MM-HH:MM`**: (Opcional) Rango horario del evento en formato 24 horas.
  - Puedes usar solo hora de inicio: `+ HH:MM #tag ...`
  - Puedes omitir la hora si es un evento importante del día sin hora fija.
- **`#tag`**: (Opcional) Una etiqueta precedida por `#` para categorizar el evento (ver sección de Tags).
- **`Descripción del evento`**: Texto libre que describe la actividad.

**Ejemplos:**

```
+ 10:00-11:00 #w reunion teams: ejecución reporte ACL
+ 09:00 #p dar tutoría de programación
+ #h Llamar al fontanero
```

## Tags (Etiquetas)

Los tags son palabras clave precedidas por `#` que ayudan a categorizar y filtrar eventos o tareas. Puedes definir los que necesites.

**Tags Actuales:**

- `#w`: Trabajo (Work)
- `#h`: Hogar (Home)
- `#p`: Programación / Proyectos Personales

**Uso:**

- Permiten identificar rápidamente el contexto de una actividad.
- Facilitan la búsqueda y el filtrado (por ejemplo, usando `grep '#w'` para ver solo eventos de trabajo).

## Ejemplo Completo de un Bloque Diario

```
2025-04-23 miércoles [P]
+ #h Recordar sacar la basura orgánica
+ 09:00-09:30 #w reunion teams: avances cumplimiento de normas
+ 10:00-12:00 #w reunion teams: Descubre tu propósito
+ 12:00-01:00 #w preparar el almuerzo y comer
+ #p Investigar sobre librería X para proyecto Y
```

## Formato `recurring.txt`

Este archivo define los eventos recurrentes usando secciones y reglas específicas.

### Estructura del Archivo

El archivo se divide en secciones usando encabezados especiales:

- **`@anual`**: Para eventos que ocurren una vez al año en una fecha específica.
- **`@mensual`**: Para eventos que ocurren mensualmente en un día específico del mes.
- **`@semanal`**: Para eventos que ocurren semanalmente en un día específico de la semana.

> Las líneas que no estén bajo una de estas secciones, las líneas vacías o las que comiencen con `#` (comentarios) serán ignoradas.

### Sintaxis de las Reglas

Dentro de cada sección, las reglas siguen un formato similar al de las líneas de evento:

- **Regla Anual (`@anual`):**

  ```
  MM-DD [HH:MM[-HH:MM]] [#tag] Descripción
  ```

  - `MM-DD`: Mes y día (con ceros iniciales, ej. `07-11`).
  - Resto: Opcional Hora(s), Tag y Descripción, igual que una línea de evento normal.

- **Regla Mensual (`@mensual`):**

  ```
  DD [HH:MM[-HH:MM]] [#tag] Descripción
  ```

  - `DD`: Día del mes (1-31, sin cero inicial necesario para días < 10, ej. `1` o `15`).
  - Resto: Opcional Hora(s), Tag y Descripción.

- **Regla Semanal (`@semanal`):**
  ```
  nombre_dia [HH:MM[-HH:MM]] [#tag] Descripción
  ```
  - `nombre_dia`: Nombre completo del día en minúsculas (lunes, martes, miércoles, jueves, viernes, sábado, domingo).
  - Resto: Opcional Hora(s), Tag y Descripción.

### Ejemplo de `recurring.txt`

```
# Cumpleaños y aniversarios
@anual
07-11 13:00-14:00 #h cumpleaños primo Juan
12-25 #f Navidad (sin hora)

# Tareas mensuales
@mensual
01 09:00 #h Pagar alquiler
15 #p Revisión mensual proyecto X

# Tareas semanales
@semanal
lunes 08:00 #w Scrum diario
miércoles #h Sacar basura
viernes 19:00-21:00 #p Noche de estudio
```

## Funcionamiento del Script (`calendar_parser.py`)

El script `calendar_parser.py` automatiza el mantenimiento de estos archivos. Al ejecutarlo:

1.  **Lee los Archivos:** Carga el contenido de `calendar.txt`, `calendar_archive.txt` y, si existe, `recurring.txt`.
2.  **Archiva Días Pasados:** Revisa `calendar.txt` y mueve todos los bloques diarios cuya fecha sea _anterior_ a la fecha de referencia (por defecto, hoy) al archivo `calendar_archive.txt`.
3.  **Genera Plantillas Futuras:** Asegura que existan bloques diarios vacíos en `calendar.txt` para un número determinado de días hacia el futuro (por defecto, 20 días) a partir de la fecha de referencia. Si faltan días, crea sus encabezados.
4.  **Aplica Eventos Recurrentes:** Si se proporcionó `recurring.txt`:
    - Genera todos los eventos recurrentes (anuales, mensuales, semanales) que caen dentro del rango de días futuros definidos en el paso anterior.
    - Para cada día en ese rango, añade los eventos recurrentes generados a la lista de eventos del día correspondiente en `calendar.txt`.
    - **Importante:** El script verifica si un evento _idéntico_ (misma hora, tag y descripción) ya existe en ese día antes de añadirlo, para evitar duplicados.
5.  **Guarda Cambios:** Sobrescribe los archivos `calendar.txt` y `calendar_archive.txt` con el contenido actualizado y ordenado.

### Ejecución del Script

Se ejecuta desde la línea de comandos usando `uv run` (o `python`) y especificando las rutas de los archivos:

```bash
uv run calendar_parser.py \
  --main-file /ruta/a/tu/calendar.txt \
  --archive-file /ruta/a/tu/calendar_archive.txt \
  --recurring-file /ruta/a/tu/recurring.txt
```

## Consejos Adicionales

- **Consistencia:** Sé consistente con el formato para facilitar la lectura y posible procesamiento automático futuro.
- **Herramientas:** Usa `grep`, `awk`, `sed` o scripts simples (Python, Bash) para buscar, filtrar o generar resúmenes de tu calendario.
- **Integración:** Puedes vincular esto con tu `todo.txt` añadiendo tareas específicas que surjan de eventos del calendario.
- **Revisión:** Revisa tu `calendar.txt` regularmente (diaria o semanalmente) como parte de tu rutina de planificación.
- **Automatización**: Ejecuta el script `calendar_parser.py` regularmente (ej. diariamente usando cron en Linux/macOS o el Programador de Tareas en Windows) para mantener tu calendario al día automáticamente.
- **Backup:** Al ser un archivo de texto, es fácil de respaldar usando Git, Dropbox, etc.
