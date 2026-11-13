# Portal de Servicios

Aplicación web para la evaluación parcial de Desarrollo de Aplicaciones Web. Incluye siete páginas con navegación común, tres calculadoras con Flask y formularios `POST`, páginas informativas y un carrusel Bootstrap.

## Requisitos

- Python 3.10 o posterior
- `pip`
- Navegador web moderno

## Preparación y ejecución

Desde la carpeta del proyecto, crea el entorno virtual:

```powershell
py -m venv .venv
```

Actívalo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En Windows CMD, activa el mismo entorno con:

```bat
.venv\Scripts\activate.bat
```

Instala las dependencias registradas:

```powershell
python -m pip install -r requirements.txt
```

Inicia la aplicación:

```powershell
python app.py
```

Abre <http://127.0.0.1:5000> en el navegador mientras la aplicación esté ejecutándose. Bootstrap se carga desde su CDN, por lo que la interfaz requiere conexión a Internet.

## Páginas

- **Inicio:** presentación y carrusel de tres imágenes.
- **Compra:** subtotal y descuento del 10 % cuando el subtotal supera $1,000.
- **Salario:** hasta 40 horas normales; cada hora adicional se paga al doble.
- **Temperatura:** conversión de Celsius a Fahrenheit y Kelvin.
- **Empresa:** presentación, misión y visión de Nexo, una empresa ficticia.
- **Servicios:** tres opciones presentadas en tarjetas Bootstrap.
- **Contacto:** correo, teléfono, ubicación y horario de atención ficticios.

## Pruebas

Con el entorno activado, ejecuta:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas verifican las siete rutas, los casos de compra con y sin descuento, el salario con y sin horas extra, la conversión de 25 °C y el manejo de datos inválidos.

## Evidencias y explicación

Las evidencias disponibles están en [`examen/evidencias/`](examen/evidencias/). La explicación técnica, el diagrama y la interpretación de resultados están en [`examen/explicacion.md`](examen/explicacion.md). Para completar la entrega hacen falta capturas legibles de todas las páginas y de los casos de cálculo solicitados.
