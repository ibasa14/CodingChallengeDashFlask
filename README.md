# CodingChallengeDashFlask

Challenge de creación de un dashboard haciendo uno de Flask + Dash

## Instalación (linux)

1. Generar virtual enviroment:

```
python -m venv env
```

2. Clonar repositorio:

```
git clone https://github.com/ibasa14/CodingChallengeDashFlask.git
```

3. Activar entorno e instalar dependencias.

```
source env/bin/activate
cd CodingChallengeDashFlask
python -m pip install -r requirements.txt
```

## Uso

1. Ejecutar el archivo app.py:

```
python app.py
```

2. Abrir el navegador en la direccion:
   http://127.0.0.1:5000/dash/

## Funcionalidades

Además de los ejercicios propuestos en el guíon, se ha añadido:

- Un cuarto gráfico que representa la distribución de las motos en los diferentes distritos de Madrid.
- La página es responsive, al modificar el tamaño de la ventana, los tamaños de los graficos y proporciones se ajustan.

![Alt text](/assets/imagen1.png?raw=true "Mapa")

![Alt text](/assets/Imagen2.png?raw=true "Histograma")

![Alt text](/assets/Imagen3.png?raw=true "Responsive")
