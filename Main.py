'''

Este es un software modular, con aplicacion en negocios pequeños y medianos,utiliza una base de datos y es un sistema monousuario.
El objetivo de este software es el de proveer de un sistema liviano y facil de usar para usuarios con poca experiencia o sin necesidad de sistemas complejos.
El funcionamiento se basa en modulos reemplazables de acuerdo con las necesidades del usuario/local.
El sistema tiene un control de licencia que controla si el usuario tiene el sistema activado cada vez que ingresa al mismo.

- Lo primero que se ve al iniciar el sistema es la pantalla de bienvenida modulo <welcome()>
    · En ella existe la posibilidad del ingreso mediante contraseña o directo
    · Allí también hay una sección de notificaciones que avisan del estado de la licencia

- Una vez pasada la pantalla de bienvenida ingresamos directamente al modulo de atencion al cliente modulo <atencion()>
    · En este modulo se realizan las actividades del negocio pertinentes al sistema


'''

from BackEnd import *
from Resources import *
from Static import *
from Logs import autolog
from tkinter import ttk
from tkcalendar import Calendar
from babel.numbers import *

'''

Se importan funciones y objetos desde otros archivos para emprolijar el codigo en el main

- En backend estan el conjunto de funciones correspondientes con el funcionamiento del sistema.
    · Calculos y logica 
    · Formateo de datos
    · Interaccion con la base de datos
    
- En resources se encuentran los objetos y constantes con los que trabaja el sistema
    · Direcciones de archivos y directorios
    · Codigos de colores para la interfaz
    · Constantes para las dimensiones y caracteristicas de objetos de la interfaz
    · Objetos para crear widgets de tkinter
    · Objetos propios del funcionamiento del sistema
        ·· Objetos correspondientes a una venta, compra, gasto, etc.
        
- En Logs funciona la escritura de mensajes informativos o de excepciones del sistema a un archivo de reportes

'''

root = tk.Tk()


def init():
    inicio = tk.Canvas(root, height=mainY, width=mainX, background=bgColor_1, highlightthickness=0)
    inicio.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)

    inicio.grid_columnconfigure(1, weight=1)
    inicio.grid_columnconfigure(2, weight=1)
    inicio.grid_rowconfigure(1, weight=1)

    sec1 = tk.Canvas(inicio, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
    sec1.grid(row=0, column=0, columnspan=2, sticky='nswe', padx=padx, pady=pady)
    sec1.grid_columnconfigure(1, weight=1)

    sec2 = tk.Canvas(inicio, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
    sec2.grid(row=0, column=2, sticky='nswe', padx=padx, pady=pady)
    sec2.grid_columnconfigure(0, weight=1)

    sec3 = tk.Canvas(inicio, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
    sec3.grid(row=1, column=0,columnspan=3, sticky='nswe', padx=padx, pady=pady)
    sec3.grid_columnconfigure(0, weight=1)
    sec3.grid_columnconfigure(1, weight=1)
    sec3.grid_columnconfigure(2, weight=1)
    sec3.grid_rowconfigure(0,weight=1)
    sec3.grid_rowconfigure(1,weight=1)
    sec3.grid_rowconfigure(2,weight=1)

    # Widget functions

    def updNotif(msg):
        notPanel.insert(0, msg)

    def updateAll():
        ventasInsertAll()
        cubInsertAll()
        _capital = 0
        _cubs = sqGenericSelect('cubiertas')
        _saldoTotal = 0
        _ventas = sqGenericSelect('ventas')
        for item in _cubs:
            _stock = item[4]
            if _stock > 0:
                _costo = item[2]
                _capital += (_costo * _stock)
        for item in _ventas:
            _saldo = item[5]
            if _saldo > 0:
                _saldoTotal += _saldo
        capitalVar.set(f'${"%.2f" % _capital}')
        deudaVar.set(f'{"%.2f" % _saldoTotal}')

    def compraBind(event=None):
        compra = tk.Tk()
        wTitle = 'Carga una compra'
        compra.title(wTitle)
        compra.configure(bg=bgColor_1)
        compra.geometry('%dx%d' % (windX, windY))
        compra.grid_columnconfigure(0, weight=1)
        compra.grid_rowconfigure(1, weight=1)

        sec1 = tk.Canvas(compra, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
        sec1.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
        sec1.grid_columnconfigure(0, weight=1)
        sec1.grid_columnconfigure(1, weight=1)

        sec2 = tk.Canvas(compra, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
        sec2.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)
        sec2.grid_columnconfigure(0, weight=1)
        sec2.grid_columnconfigure(1, weight=1)

        fecha = date

        def fieldsOk(cub, cost, prec, cant, prov):
            try:
                if cub != cubText and cost != costoText and prec != precText and cant != cantText and prov != provText:
                    cost = float(cost)
                    prec = float(prec)
                    cant = int(cant)
                    return True
                else:
                    popUp("Campos incorrectos", "Falta rellenar campos", "Aceptar", fontPrimary,
                          fontSecondary, bgColor_2,
                          fColor_1)
                    print("Rellenar")
            except Exception as e:
                popUp("Campos incorrectos", "Ingrese datos correctos para el producto", "Aceptar", fontPrimary,
                      fontSecondary, bgColor_2,
                      fColor_1)
                print("Campos incorrectos")
                return False

        def confBind(event=None):
            nombre = cubEntry.get()
            costo = costoEntry.get()
            precio = precEntry.get()
            cantidad = cantEntry.get()
            proveedor = provEntry.get()
            fecha = fechaVar.get()
            if fieldsOk(nombre, costo, precio, cantidad, proveedor):
                costo = float(costo)
                precio = float(precio)
                cantidad = int(cantidad)
                cubierta = producto(nombre, costo, precio, cantidad, proveedor, fecha)
                cubierta.cargarNuevo()
                cubInsertAll()
                updNotif(f"Se ingresó la compra de {cantidad} {nombre}")
                compra.destroy()

        def calendarBind(event=None):
            calendario = tk.Tk()
            wTitle = 'Elija una fecha'
            calendario.title(wTitle)
            calendario.configure(bg=bgColor_1)

            global fecha

            def listoBind(event=None):
                fecha = cal.get_date()
                fechaVar.set(fecha)
                calendario.destroy()

            try:
                cal = Calendar(calendario, font=fontSecondary, selectmode='day', locale='es_es', date_pattern="dd/mm/yyyy",
                               background=bgColor_2, foreground=fColor_1, bordercolor=bgColor_2,
                               headersbackground=bgColor_1,
                               headersforeground=fColor_1, normalbackground=bgColor_2, normalforeground=fColor_1)
                cal.grid(row=0, column=0)
            except Exception as e:
                autolog("Error en calendario", e)

            buttonStatic(calendario, 1, 0, 1, 1, "Listo", fontSecondary, bttBgColor_1, fColor_1, 1, bttWidth_1,
                         listoBind)

            calendario.mainloop()

        fechaVar = tk.StringVar(compra)
        fechaVar.set(fecha)

        labelStatic(sec1, 0, 0, "Cubierta", fontSecondary, bgColor_2, fColor_1, "we", "w")
        labelStatic(sec1, 1, 0, "Costo", fontSecondary, bgColor_2, fColor_1, "we", "w")
        labelStatic(sec1, 2, 0, "Precio", fontSecondary, bgColor_2, fColor_1, "we", "w")
        labelStatic(sec1, 3, 0, "Cantidad", fontSecondary, bgColor_2, fColor_1, "we", "w")
        labelStatic(sec1, 4, 0, "Proveedor", fontSecondary, bgColor_2, fColor_1, "we", "w")
        labelStatic(sec1, 5, 0, "Fecha", fontSecondary, bgColor_2, fColor_1, "we", "w")

        cubText = ""
        costoText = ""
        precText = ""
        cantText = ""
        provText = ""

        cubEntry = entry(sec1, 0, 1, 1, 1, cubText, bgColor_3, fColor_1, defaultFg, entryWidth,
                         None, "we")
        costoEntry = entry(sec1, 1, 1, 1, 1, costoText, bgColor_3, fColor_1, defaultFg,
                           entryWidth, None, "we")
        precEntry = entry(sec1, 2, 1, 1, 1, precText, bgColor_3, fColor_1, defaultFg,
                          entryWidth, None, "we")
        cantEntry = entry(sec1, 3, 1, 1, 1, cantText, bgColor_3, fColor_1, defaultFg,
                          entryWidth, None, "we")
        provEntry = entry(sec1, 4, 1, 1, 1, provText, bgColor_3, fColor_1, defaultFg,
                          entryWidth, None, "we")
        buttonDinamic(sec1, 5, 1, 1, 1, fechaVar, fontSecondary, bttBgColor_1, fColor_1, 1, bttWidth_1, calendarBind)

        buttonStatic(sec2, 6, 0, 2, 2, "Confirmar", fontPrimary, bttBgColor_1, fColor_1, 1, bttWidth_1, confBind,
                     "we")

        compra.mainloop()

    # Insercion de todos los productos en la tabla
    def ventasInsertAll():
        if ventasList.get_children():
            ventasList.delete(*ventasList.get_children())
        productos = sqGenericSelect('ventas')
        for item in productos:
            ventasInsertOne(item)

    # Insercion de un solo producto en la tabla
    def ventasInsertOne(item):
        id = item[0]
        cod = item[1]
        fecha = item[6]
        cliente = item[3]
        nom = sqGenericSelectOne("cubiertas", "nombre", "id", cod)
        cant = int(item[2])
        precio = float(sqGenericSelectOne("cubiertas", "precio", "id", cod)[0])
        total = float(precio * cant)
        saldo = float(item[5])
        if saldo > 0:
            ventasList.insert("", tk.END,
                              values=(id, fecha, cliente, nom, cant, f'${"%.2f" % total}', f'${"%.2f" % saldo}'))

    # Insercion de todos los productos en la tabla
    def cubInsertAll():
        if cubiertas.get_children():
            cubiertas.delete(*cubiertas.get_children())
        productos = sqGenericSelect('cubiertas')
        for item in productos:
            cubInsertOne(item)

    # Insercion de un solo producto en la tabla
    def cubInsertOne(item):
        id = item[0]
        cub = f'{item[1]}'
        costo = f'${"%.2f" % item[2]}'
        precio = f'${"%.2f" % item[3]}'
        stock = item[4]
        proveedor = f'{item[5]}'
        fecha = f'{item[6]}'
        if stock > 0:
            cubiertas.insert("", tk.END, values=(id, cub, costo, precio, stock, proveedor, fecha))

    def inventarioDoubleClickBind(event=None):
        if cubiertas.selection():
            inventario = tk.Tk()
            wTitle = 'Acciones con una cubierta'
            inventario.title(wTitle)
            inventario.configure(bg=bgColor_1)
            inventario.geometry('%dx%d' % (windX, windY))
            inventario.grid_columnconfigure(0, weight=1)
            inventario.grid_rowconfigure(0, weight=1)
            inventario.grid_rowconfigure(1, weight=1)

            sec1 = tk.Canvas(inventario, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
            sec1.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
            sec1.grid_columnconfigure(0, weight=1)
            sec1.grid_columnconfigure(1, weight=1)

            sec2 = tk.Canvas(inventario, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
            sec2.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)
            sec2.grid_columnconfigure(0, weight=1)
            sec2.grid_columnconfigure(1, weight=1)

            _producto = None

            for item in cubiertas.selection():
                _codigo = cubiertas.item(item)['values'][0]
                _producto = sqGenericSelect('cubiertas', None, 'id', _codigo)[0]

            def fieldsOk(cantidad):
                try:
                    cantidad = int(cantidad)
                    if cantidad >= 0:
                        return True
                    else:
                        popUp("Campos incorrectos", "El valor debe ser mayor a cero", "Aceptar", fontPrimary,
                              fontSecondary, bgColor_2,
                              fColor_1)
                        updNotif("Se ingresó un valor incorrecto")
                except Exception as e:
                    popUp("Campos incorrectos", "Ingrese datos correctos para el producto", "Aceptar", fontPrimary,
                          fontSecondary, bgColor_2,
                          fColor_1)
                    updNotif("Se ingresó un valor incorrecto")
                    return False

            def eliminarBind(event=None):
                popUp_select("Precaucion", "Está por eliminar un producto", "Volver", "Continuar", fontPrimary,
                             fontSecondary, bttBgColor_1, fColor_1, delete)

            def delete(event=None):
                sqDeleteRow('cubiertas', 'id', _codigo)
                updNotif(f"Se eliminó {_producto[1]} del inventario")
                updateAll()
                inventario.destroy()

            def venderBind(event=None):
                cantidad = cantEntry.get()
                if fieldsOk(cantidad):
                    cantidad = int(cantidad)
                    if cantidad <= _producto[4]:
                        _venta = venta(_producto[0], cantidad, cliEntry.get(), obsEntry.get())
                        _venta.cargarNueva()
                        sqUpdateOne('cubiertas', 'cantidad', (_producto[4] - cantidad), 'id', _producto[0])
                        updNotif(f"Se registró la venta de {cantidad} {_producto[1]}")
                        inventario.destroy()
                        updateAll()
                    else:
                        popUp("Stock insuficiente", "Ingresó una cantidad mayor al stock existente", "Continuar",
                              fontPrimary, fontSecondary, bttBgColor_1, fColor_1)

            def loadValues(prod):
                cubText.set(prod[1])
                costoText.set(prod[2])
                precText.set(prod[3])
                cantText.set(prod[4])
                provText.set(prod[5])
                fechaText.set(prod[6])

            cubText = tk.StringVar(sec1)
            costoText = tk.StringVar(sec1)
            precText = tk.StringVar(sec1)
            cantText = tk.StringVar(sec1)
            provText = tk.StringVar(sec1)
            fechaText = tk.StringVar(sec1)

            labelStatic(sec1, 0, 0, 'Cubierta:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 0, 1, 'Stock:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 1, 0, 'Costo:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 1, 1, 'Precio:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 2, 0, 'Proveedor:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 2, 1, 'Compra:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelDinamic(sec1, 0, 0, 1, cubText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 0, 1, 1, cantText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 1, 0, 1, costoText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 1, 1, 1, precText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 2, 0, 1, provText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 2, 1, 1, fechaText, fontSecondary, bgColor_2, fColor_1, 'e')

            labelStatic(sec2, 3, 0, 'Cantidad:', fontPrimary, bgColor_2, fColor_2, 'we', 'w')
            cantEntry = entry(sec2, 3, 1, 1, 1, "", bgColor_3, fColor_1, defaultFg, entryWidth, None, 'we')
            labelStatic(sec2, 4, 0, 'Cliente:', fontPrimary, bgColor_2, fColor_2, 'we', 'w')
            cliEntry = entry(sec2, 4, 1, 1, 1, "", bgColor_3, fColor_1, defaultFg, entryWidth, None, 'we')
            labelStatic(sec2, 5, 0, 'Observaciones:', fontPrimary, bgColor_2, fColor_2, 'we', 'w')
            obsEntry = entry(sec2, 5, 1, 1, 1, "", bgColor_3, fColor_1, defaultFg, entryWidth, None, 'we')

            buttonStatic(sec2, 6, 0, 1, 1, "Eliminar", fontPrimary, notificationColor, fColor_2, 1, bttWidth_1,
                         eliminarBind)
            buttonStatic(sec2, 6, 1, 1, 1, "Vender", fontPrimary, bttBgColor_1, fColor_1, 1, bttWidth_1,
                         venderBind)

            loadValues(_producto)
            inventario.mainloop()

    def ventasDoubleClickBind(event=None):
        if ventasList.selection():
            venta = tk.Tk()
            wTitle = 'Acciones con una cubierta'
            venta.title(wTitle)
            venta.configure(bg=bgColor_1)
            venta.geometry('%dx%d' % (windX, windY))

            venta.grid_columnconfigure(0, weight=1)

            sec1 = tk.Canvas(venta, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
            sec1.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
            sec1.grid_columnconfigure(0, weight=1)
            sec1.grid_columnconfigure(1, weight=1)

            sec2 = tk.Canvas(venta, height=windX, width=windY, background=bgColor_2, highlightthickness=0)
            sec2.grid(row=1, column=0, sticky='nswe', padx=5, pady=5)
            sec2.grid_columnconfigure(0, weight=1)
            sec2.grid_columnconfigure(1, weight=1)
            sec2.grid_rowconfigure(0, weight=1)
            sec2.grid_rowconfigure(1, weight=1)
            sec2.grid_rowconfigure(2, weight=1)

            _producto = None
            _venta = None

            for item in ventasList.selection():
                _id = ventasList.item(item)['values'][0]
                _venta = sqGenericSelect('ventas', None, 'id', _id)[0]
                _codigo = _venta[1]
                _producto = sqGenericSelect('cubiertas', None, 'id', _codigo)[0]

            def fieldsOk(num):
                try:
                    cantidad = int(num)
                    if cantidad >= 0:
                        return True
                    else:
                        popUp("Campos incorrectos", "El valor debe ser mayor a cero", "Aceptar", fontPrimary,
                              fontSecondary, bgColor_2,
                              fColor_1)
                        print("Rellenar")
                except Exception as e:
                    popUp("Campos incorrectos", "Ingrese un importe correcto", "Aceptar", fontPrimary,
                          fontSecondary, bgColor_2,
                          fColor_1)
                    return False

            def confirmBind(event=None):
                sqDeleteRow('Ventas', 'id', _id)
                updNotif(f"El saldo de {_venta[3]} fue cancelado")
                updateAll()
                venta.destroy()

            def cancelarBind(event=None):
                cliente = _venta[3]
                popUp_select("Confirmar", f"Esta por cancelar el saldo de {cliente}", "Volver", "Confirmar",
                             fontSecondary, fontPrimary, bttBgColor_1, fColor_1, confirmBind)

            def pagoBind(event=None):
                saldo = float(_venta[5])
                pago = pagoEntry.get()
                if fieldsOk(pago):
                    pago = float(pago)
                    _ganancia = float(statics()['ganancia'])
                    _ganancia += pago
                    staticData['ganancia'] = _ganancia
                    write(staticFile,staticData)
                    nuevoSaldo = float(saldo - pago)
                    sqUpdateOne('ventas', 'saldo', nuevoSaldo, 'id', _id)
                    updNotif(f"Se registro un pago de {_venta[3]} por ${pago} ")
                    updNotif(f"Se actualizó la ganancia")
                    updateAll()
                    venta.destroy()

            def loadValues(venta, prod):
                precio = prod[3]
                cant = venta[2]
                total = precio * cant
                cliText.set(venta[3])
                fechaText.set(venta[6])
                cubText.set(prod[1])
                cantText.set(cant)
                totalText.set(total)
                saldoText.set(venta[5])
                obsText.set(f'"{venta[4]}"')

            cliText = tk.StringVar(venta)
            fechaText = tk.StringVar(venta)
            cubText = tk.StringVar(venta)
            cantText = tk.StringVar(venta)
            totalText = tk.StringVar(venta)
            saldoText = tk.StringVar(venta)
            obsText = tk.StringVar(venta)

            labelStatic(sec1, 0, 0, 'Cliente:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 0, 1, 'Fecha:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 1, 0, 'Cubierta:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 1, 1, 'Cantidad:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 2, 0, 'Total:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 2, 1, 'Saldo:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelStatic(sec1, 3, 0, 'Observaciones:', fontPrimary, bgColor_2, fColor_2, 'w')
            labelDinamic(sec1, 0, 0, 1, cliText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 0, 1, 1, fechaText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 1, 0, 1, cubText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 1, 1, 1, cantText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 2, 0, 1, totalText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 2, 1, 1, saldoText, fontSecondary, bgColor_2, fColor_1, 'e')
            labelDinamic(sec1, 4, 0, 2, obsText, fontSecondary, bgColor_2, fColor_1, 'we', 'w')

            labelStatic(sec2, 0, 0, 'Pago:', fontPrimary, bgColor_2, fColor_2, 'w')
            pagoEntry = entry(sec2, 0, 1, 1, 1, "", bgColor_3, fColor_1, defaultFg, entryWidth, None, "we")
            buttonStatic(sec2, 1, 0, 1, 1, "Cancelar saldo", fontPrimary, bttBgColor_1, fColor_1, 1, bttWidth_1,
                         cancelarBind)
            buttonStatic(sec2, 1, 1, 1, 1, "Registrar pago", fontPrimary, bttBgColor_1, fColor_1, 1, bttWidth_1,
                         pagoBind)

            loadValues(_venta, _producto)
            venta.mainloop()

    # Botones
    buttonStatic(sec1, 1, 0, 1, 1, "Compra", fontSecondary, bttBgColor_1, fColor_1, 1, None, compraBind, "nwe")

    # Seccion 1
    labelStatic(sec1, 0, 1, "Inventario", fontPrimary, bgColor_2, fColor_1, 'nswe')

    # Treeview
    cubiertas = ttk.Treeview(sec1, selectmode='browse')
    cubiertas.grid(column=1, row=1, rowspan=2, padx=5, pady=pady, sticky='nswe')
    cubiertas['columns'] = ('0', '1', '2', '3', '4', '5', '6')
    cubiertas['show'] = 'headings'

    # ScrollBar
    scrollBar = ttk.Scrollbar(sec1, orient='vertical', command=cubiertas.yview)
    scrollBar.grid(column=2, row=1, rowspan=2, padx=5, pady=pady, sticky='ns')
    cubiertas.configure(yscrollcommand=scrollBar.set)

    # Cabecera de cada columna
    cubiertas.heading('0', text='id')
    cubiertas.heading('1', text='Cubierta')
    cubiertas.heading('2', text='Costo')
    cubiertas.heading('3', text='Precio')
    cubiertas.heading('4', text='Stock')
    cubiertas.heading('5', text='Proveedor')
    cubiertas.heading('6', text='Adquisicion')

    # Configuracion del ancho normal y ancho minimo de las columnas
    cubiertas.column("0", stretch='no', width=0, anchor="center")
    cubiertas.column("1", minwidth=40, width=80, anchor="center")
    cubiertas.column("2", stretch='no', width=0, anchor="center")
    cubiertas.column("3", minwidth=40, width=60, anchor="center")
    cubiertas.column("4", minwidth=20, width=30, anchor="center")
    cubiertas.column("5", stretch='no', width=0, anchor="w")
    cubiertas.column("6", stretch='no', width=0, anchor="center")
    cubiertas.bind("<Double-1>", inventarioDoubleClickBind)

    # Seccion 2
    labelStatic(sec2, 0, 0, "Ventas", fontPrimary, bgColor_2, fColor_1, 'nswe')

    # Treeview
    ventasList = ttk.Treeview(sec2, selectmode='browse')
    ventasList.grid(column=0, row=1, rowspan=2, padx=5, pady=pady, sticky='nswe')
    ventasList['columns'] = ('0', '1', '2', '3', '4', '5', '6')
    ventasList['show'] = 'headings'

    # ScrollBar
    scrollBar = ttk.Scrollbar(sec2, orient='vertical', command=ventasList.yview)
    scrollBar.grid(column=1, row=1, rowspan=2, padx=5, pady=pady, sticky='ns')
    ventasList.configure(yscrollcommand=scrollBar.set)

    # Cabecera de cada columna
    ventasList.heading('0', text='*')
    ventasList.heading('1', text='Fecha')
    ventasList.heading('2', text='Cliente')
    ventasList.heading('3', text='Cubierta')
    ventasList.heading('4', text='Cantidad')
    ventasList.heading('5', text='Total')
    ventasList.heading('6', text='Saldo')

    # Configuracion del ancho normal y ancho minimo de las columnas
    ventasList.column("0", stretch='no', width=0, anchor="center")
    ventasList.column("1", minwidth=40, width=60, anchor="center")
    ventasList.column("2", minwidth=40, width=60, anchor="center")
    ventasList.column("3", minwidth=40, width=60, anchor="center")
    ventasList.column("4", minwidth=40, width=60, anchor="center")
    ventasList.column("5", minwidth=40, width=60, anchor="w")
    ventasList.column("6", minwidth=40, width=60, anchor="center")
    ventasList.bind("<Double-1>", ventasDoubleClickBind)

    # Seccion3
    capitalVar = tk.StringVar(sec3)
    capitalVar.set("$0")
    deudaVar = tk.StringVar(sec3)
    deudaVar.set("$0")
    gananciaVar = tk.StringVar(sec3)
    gananciaVar.set("$0")
    labelStatic(sec3, 0, 3, "Capital:", fontSecondary, bgColor_2, fColor_1, 'w')
    labelDinamic(sec3, 0, 4, 1, capitalVar, fontSecondary, bgColor_2, fColor_1, 'e')
    labelStatic(sec3, 1, 3, "Deuda:", fontSecondary, bgColor_2, fColor_1, 'w')
    labelDinamic(sec3, 1, 4, 1, deudaVar, fontSecondary, bgColor_2, fColor_1, 'e')
    labelStatic(sec3, 2, 3, "Ganancia:", fontSecondary, bgColor_2, fColor_1, 'w')
    labelDinamic(sec3, 2, 4, 1, gananciaVar, fontSecondary, bgColor_2, fColor_1, 'e')
    notPanel = listbox(sec3,0,0,3,1,fontSecondary,bgColor_3,fColor_2,'we')

    updateAll()
    inicio.mainloop()


'''
EJECUCION
'''

root.geometry('%dx%d' % (mainX, mainY))
root.title("KencoWare 3.0")
root.configure(background=bgColor_1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

autolog(" > Programa iniciado < ")
init()
root.mainloop()
