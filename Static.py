"""
En este archivo se gestionan los datos permanentes de funcionamiento del
programa, es decir, aquellos que no deben ser borrados al cerrarse el software.
"""

from Resources import staticFile
from Logs import autolog
import json

staticData = {
    'ganancia' : "0"
}

def write (file, data):
    try:
        with open (file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        autolog("No se pudo escribir el archivo static", e)

def statics():
    try:
        with open(staticFile, "r") as f:
            return json.load(f)
    except Exception as e:
        autolog("No se pudo recuperar el archivo static", e)

