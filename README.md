# Taller: Análisis de Datos con Power BI

## Herramientas utilizadas

### Python

Utilizaremos Python para leer y procesar los archivos de datos.

### Pandas

Utilizaremos la biblioteca Pandas para:

- Leer archivos CSV.
- Filtrar información.
- Agrupar datos.
- Calcular métricas sencillas como promedio, máximo y mínimo.
- Preparar los datos que utilizaremos en Power BI.

### Tkinter

La aplicación incluye una interfaz gráfica sencilla que permite seleccionar archivos, edificios y métricas para realizar consultas sobre los datos.

### Power BI

Utilizaremos Power BI Desktop para convertir los datos procesados en un dashboard interactivo mediante gráficos, tarjetas y filtros.

---

Los archivos contienen información de consumo energético.

Cada registro incluye:

| Campo | Descripción |
|---|---|
| Fecha | Día en que se registró el consumo |
| Edificio | Edificio al que pertenece el registro |
| Consumo_kWh | Consumo de energía registrado |
| Temperatura | Temperatura registrada |
| Personas | Cantidad de personas registradas |



---

## Estructura del proyecto

```text
taller-powerbi-energy-dashboard/
│
├── datos/
│   ├── prueba_1.csv
│   ├── prueba_2.csv
│   └── prueba_3.csv
│
├── src/
│   └── app.py
│
├── resultados/
│
├── powerbi/
│   └── EnergyDashboard.pbix
│
├── requirements.txt
└── README.md
```

### `datos/`

Contiene los archivos CSV utilizados como información de entrada.

### `src/`

Contiene el código fuente de la aplicación.

### `resultados/`

Contiene los archivos generados por el programa. Aquí se crea el archivo que posteriormente se importa a Power BI.

### `powerbi/`

Contiene el archivo del dashboard de Power BI.

### `requirements.txt`

Contiene las bibliotecas de Python necesarias para ejecutar el proyecto.

---

La aplicación permite:

1. Seleccionar un archivo CSV.
2. Seleccionar un edificio.
3. Seleccionar una métrica.
4. Analizar los datos.
5. Generar los datos que utilizaremos en Power BI.

---

## Conceptos que utilizaremos

Durante el taller trabajaremos principalmente con:

- Datos y datasets.
- Archivos CSV.
- Filtrado de datos.
- Agrupación de datos.
- Promedio, máximo y mínimo.
- Visualizaciones.
- Dashboards.
- Filtros y segmentadores.
- Integración entre Python/Pandas y Power BI.

---

## Evidencia

Cada estudiante deberá entregar:

- El código fuente modificado.
- Un video corto mostrando la aplicación y el dashboard modificados.

Los archivos deberán subirse a la carpeta de Drive indicada durante el taller.



