El la carpeta raiz gestor proyectos, ejectuar el comando pytest

luego estos comandos, es para configurar la ruta absoluta:
set PYTHONPATH=%cd%
pytest

Si se quiere correr la aplicacion, correr el siguiente comando:
uvicorn app.main:app --reload

Comando para correr los test:

pytest app/tests
