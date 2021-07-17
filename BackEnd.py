# Data base management functions

import sqlite3
from Resources import *
from Logs import autolog

conn = sqlite3.connect(dataBaseFile)  # File name and path in resources
c = conn.cursor()


# Verificacion de existencia de tablas
# Devuelve TRUE si todas las tablas existen (modificar parametros segun tablas en uso)


def tablesExist(tabla_1, tabla_2):
    with conn:
        c.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name="{tabla_1}"''')
        cond_1 = c.fetchall()
        c.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name="{tabla_2}"''')
        cond_2 = c.fetchall()
        if cond_1 and cond_2:
            return True
        else:
            return False

# Creacion de tablas (modificar a necesidad)
def initDB():
    DBcreation()

def DBcreation():
    if not tablesExist("cubiertas", "ventas"):
        with conn:
            table = 'cubiertas'
            try:
                c.execute(f'''CREATE TABLE {table} (
                id integer,
                nombre text,
                costo real,
                precio real,
                cantidad integer,
                proveedor text,
                fechaCompra text)''')
                autolog(f'Tabla {table} creada')
            except Exception as exc:
                autolog(f'No se pudo crear la tabla {table}', exc)
            table = 'ventas'
            try:
                c.execute(f'''CREATE TABLE {table} (
                id integer,
                codigoProducto integer,
                cantidad integer,
                cliente text,
                observaciones text,
                saldo real,
                fechaCompra text)''')
                autolog(f'Tabla {table} creada')
            except Exception as exc:
                autolog(f'No se pudo crear la tabla {table}', exc)



# Funciones genéricas

def sqGenericSelect(table, fetchCol=None, searchCol=None, refValue=None):
    '''
     Funcion select generica (no excluye filas repetidas)
    :param table: tabla que se recupera. Si solo se provee este parametro la funcion devuelte la tabla completa.
    :param fetchCol: columna que devuelve. Si provista, la funcion devuelve solo la columna requerida aqui.
    :param searchCol: columna en la que se busca. Si provista, la funcion busca en esta columna, el valor pasado en refValue.
    :param refValue: valor de referencia. Dato con el se comparan los datos de la columna pasada en searchCol. Si provisto,
    la funcion solo devuelve las filas que en los que el valor de "searchCol" sea igual a "refValue".
    :return:
    '''
    try:
        with conn:
            if not fetchCol: fetchCol = '*'
            if searchCol:
                c.execute(f'SELECT {fetchCol} FROM {table} WHERE {searchCol} = ?', (refValue,))
            else:
                c.execute(f'SELECT {fetchCol} FROM {table} ')
            x = c.fetchall()
            return x
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


def sqGenericSelectDate(table, period, refDate, fetchCol=None):
    '''
    Funcion select para fechas en formato 'DD-MM-YYYY' (no excluye filas repetidas)
    table: tabla de la que se recupera la informacion.
    period: acepta los valores 'd', 'm', 'y' para seleccionar el retorno del dia mes o año, respectivamente.
    refDate: fecha completa actual
    refValue: fecha de referencia con la que se compara.
    fetchCol: columna que devuelve. Si provista, la funcion devuelve solo la columna requerida aqui.
    '''
    try:
        start, length, _date = calcPeriod(period, refDate)
        with conn:
            if not fetchCol: fetchCol = '*'
            c.execute(f"SELECT {fetchCol} FROM {table} WHERE substr(fecha, {start}, {length}) = ?", (_date,))
            return c.fetchall()
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


# Dado el parametro "per" se devuelven los valores para dividir la fecha en el periodo correspondiente
def calcPeriod(per, date):
    valid = ['d', 'm', 'y']
    start = 0
    length = 0
    if per not in valid:
        raise ValueError("calcPeriod: periodo debe ser uno ser uno de %s" % valid)
    if per == 'd':
        start = 1
        length = 10
    elif per == 'm':
        start = 4
        length = 7
    elif per == 'y':
        start = 7
        length = 4
    subDate = date[(start - 1):(length + start - 1)]
    return start, length, subDate


def sqGenericSelectDistinct(table, fetchCol, searchCol=None, refValue=None):
    '''
    Funcion select generica (excluye filas repetidas)
    table: tabla que se recupera. Si solo se provee este parametro la funcion devuelte la tabla completa.
    fetchCol: columna que devuelve. Si provista, la funcion devuelve solo la columna requerida aqui.
    searchCol: columna en la que se busca. Si provista, la funcion busca en esta columna, el valor pasado en refValue.
    refValue: valor de referencia. Dato con el se comparan los datos de la columna pasada en searchCol. Si provisto, la funcion solo devuelve las filas que en los que el valor de "searchCol" sea igual a "refValue".
    '''
    try:
        with conn:
            if not fetchCol: fetchCol = '*'
            if searchCol:
                c.execute(f'SELECT DISTINCT {fetchCol} FROM {table} WHERE {searchCol} = {refValue}')
            else:
                c.execute(f'SELECT DISTINCT {fetchCol} FROM {table} ')
            return c.fetchall()
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


def sqGenericSelectDistinctOrdASC(table, orderCol, fetchCol, searchCol=None, refValue=None):
    '''
    Funcion select generica (excluye filas repetidas). Las filas devueltas estan ordenadas en orden alfabetico.
    table: tabla que se recupera. Si solo se provee este parametro la funcion devuelte la tabla completa.
    orderCol: en función a esta columna se ordenan los datos recuperados.
    fetchCol: columna que devuelve. Si provista, la funcion devuelve solo la columna requerida aqui.
    searchCol: columna en la que se busca. Si provista, la funcion busca en esta columna, el valor pasado en refValue.
    refValue: valor de referencia. Dato con el se comparan los datos de la columna pasada en searchCol. Si provisto, la funcion solo devuelve las filas que en los que el valor de "searchCol" sea igual a "refValue".
    '''
    try:
        with conn:
            if not fetchCol: fetchCol = '*'
            if searchCol and refValue >= 0:
                c.execute(
                    f'SELECT DISTINCT {fetchCol} FROM {table} WHERE {searchCol} = {refValue} ORDER BY {orderCol} ASC')
            else:
                c.execute(f'SELECT DISTINCT {fetchCol} FROM {table} ORDER BY {orderCol} ASC')
            return c.fetchall()
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


def sqGenericSelectOne(table, fetchCol, searchCol=None, refValue=None):
    '''
    Funcion select generica (devuelve solo una fila que concuerde con lo requerido)
    table: tabla que se recupera.
    fetchCol: columna que devuelve.
    searchCol: columna en la que se busca. Coordenada X de la busqueda
    refValue: valor de referencia. Dato con el se comparan los datos de la columna pasada en searchCol. Coordenada Y de la busqueda.
    '''
    try:
        with conn:
            if not fetchCol: fetchCol = '*'
            if searchCol and refValue >= 0:
                c.execute(f'SELECT {fetchCol} FROM {table} WHERE {searchCol} = {refValue}')
            else:
                c.execute(f'SELECT {fetchCol} FROM {table} ')
            return c.fetchone()
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


def lastID(table):
    '''
    Funcion select generica (devuelve solo una fila que concuerde con lo requerido)
    table: tabla que se recupera.
    fetchCol: columna que devuelve.
    searchCol: columna en la que se busca. Coordenada X de la busqueda
    refValue: valor de referencia. Dato con el se comparan los datos de la columna pasada en searchCol. Coordenada Y de la busqueda.
    '''
    try:
        with conn:
            c.execute(f'SELECT * FROM {table} WHERE ID = (SELECT MAX(ID)  FROM {table})')
            try:
                _id = c.fetchone()[0]
            except:
                _id = 0
            return _id
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


def sqGenericCount(table):
    '''
    Conteo de items de una tabla.
    table: Tabla en la que se cuenta
    '''
    try:
        with conn:
            c.execute(f'''SELECT COUNT(*) FROM {table}''')
            return c.fetchone()[0]
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


def sqUpdateOne(table, column, newValue, refColumn, refValue):
    '''
    Funcion con la que se modifica un valor especifico de la base de datos.
    table: Tabla en la que se realiza la modificacion.
    column: Columna en la que se realiza la modificacion.
    newValue: Nuevo valor que se inserta.
    refColumn: Columna en la que se busca un valor de referencia. Coordenada X del cambio
    refValue: Valor que se busca en la columna de referencia (refColumn). Coordenada Y del cambio
    '''
    try:
        with conn:
            c.execute(f'''UPDATE {table} SET {column} = "{newValue}" WHERE {refColumn} = {refValue}''')
    except Exception as exc:
        autolog(f'Problema en la tabla {table}', exc)


# Eliminacion de una fila en la base de datos
def sqDeleteRow(table, refColumn, refValue):
    try:
        with conn:
            c.execute(f'''DELETE FROM {table} WHERE {refColumn} = {refValue}''')
    except Exception as exc:
        autolog(f'No se pudo eliminar una fila en la tabla {table}', exc)


def modifValue(column, id, prevValue, newValue):
    '''
    Modificacion de un producto del inventario: si el nuevo valor es igual al previo no se realiza la modificacion.
    column: columna en la que se realizará la modificacion, es decir, el atributo del producto que se quiere modificar.
    id: codigo del producto a modificar.
    prevValue: valor previo, el que ya tiene el producto antes de realizar la modificacion
    newValue: nuevo valor a insertar en el lugar de "prevValue"
    '''
    if newValue != prevValue:
        idCol = 'id'
        invCol = 'inventario'
        sqUpdateOne(invCol, column, newValue, idCol, id)
        return True
    else:
        return False


# Clases para el funcionamiento del sistema
class producto:
    def __init__(self, nombre, costo, precio, cantidad, proveedor, fechaCompra):
        self.table = "cubiertas"
        self.id = 0
        if sqGenericCount(self.table) > 0:
            self.id = int(lastID(self.table)) + 1
        self.nombre = nombre
        self.costo = costo
        self.precio = precio
        self.cantidad = cantidad
        self.proveedor = proveedor
        self.fechaCompra = fechaCompra

    # Alta de un producto a la base de datos

    def cargarNuevo(self):
        try:
            with conn:
                c.execute(
                    f'''
                    INSERT INTO {self.table} 
                    VALUES (:id, :nombre, :costo, :precio, :cantidad,
                    :proveedor, :fechaCompra)''',
                    {'id': self.id,
                     'nombre': self.nombre,
                     'costo': self.costo,
                     'precio': self.precio,
                     'cantidad': self.cantidad,
                     'proveedor': self.proveedor,
                     'fechaCompra':self.fechaCompra})
        except Exception as exc:
            autolog(f'No se pudo cargar la tabla {self.table}', exc)

class venta:
    def __init__(self, codigoProducto, cantidad, cliente, obs):
        self.table = "ventas"
        self.id = 0
        if sqGenericCount(self.table) > 0:
            self.id = int(lastID(self.table)) + 1
        self.codigoProducto = codigoProducto
        self.cantidad = cantidad
        precio = sqGenericSelectOne("cubiertas","precio",'id', codigoProducto)[0]
        self.saldo = float(precio*cantidad)
        self.cliente = cliente
        self.obs = obs
        self.fecha = date

    def cargarNueva(self):
        try:
            with conn:
                c.execute(f'''INSERT INTO {self.table} VALUES 
                (:id, :codigoProducto, :cantidad, :cliente,:observaciones, :saldo, :fechaCompra)''',
                          {'id': self.id,
                           'codigoProducto': self.codigoProducto,
                           'cantidad': self.cantidad,
                           'cliente': self.cliente,
                           'observaciones': self.obs,
                           'saldo': self.saldo,
                           'fechaCompra': self.fecha})
            autolog(f"Venta {id} cargada correctamente - {date_time}")
        except Exception as exc:
            autolog(f'No se pudo cargar la tabla {self.table}', exc)



'''
EJECUCION
'''
initDB()