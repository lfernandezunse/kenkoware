'''Global style and classes'''

# This is a customized library for the making of my projects and I made it to my requirements and no one else's.
# Esta es una libreria personalizada para la creacion de mis proyectos y la hice solo acorde a mis necesidades.
# Here lies the neccesary variable definitions for the consistency of a visual style using the Tkinter library.
# This file (in his original state) cant be executed as a main program.
# Add, delete and modify as needed.

# import everything here
import os, pathlib, datetime, re
import tkinter as tk

if __name__ != '__main__':

    # Gestion de archivos
    folderName = 'bin'
    folderPath = pathlib.Path(f'./{folderName}')
    dataBaseFileName = 'dataBase'
    reportsFileName = 'reports'
    dataBaseFile = f'{folderPath}/{dataBaseFileName}'
    reportsFile = f'{folderPath}/{reportsFileName}'

    # Creacion de carpeta de archivos
    try:
        os.mkdir(f'{folderPath}')
    except Exception as e:
        print()

    # Informacion sobre versión y nombre de software
    software_title = 'PineWare'

    # Variables
    date_time = datetime.datetime.today().strftime('%d/%m/%Y - %H:%M')
    date = datetime.datetime.today().strftime('%d/%m/%Y')

    # Configuraciones globales
    bgColor_1 = '#2d546b'
    bgColor_2 = '#366480'
    bgColor_3 = '#2a3c47'
    title = ('century gothic regular', 24)
    fontPrimary = ('century gothic regular', 12)
    fontSecondary = ('century gothic regular', 10)
    fColor_1 = '#a6b6bf'
    fColor_2 = '#62727a'
    notificationColor = '#ffffff'
    mainX = 900
    mainY = 400

    # Configuraciones de botones
    bttWidth_1 = 15
    bttBgColor_1 = '#254457'
    padx = 5
    pady = 5

    # Configuracion de "entry"
    entryWidth = 30
    defaultFg = '#ffffff'

    # Configuracion de ventanas emergentes
    windX = 500
    windY = 250


    ### Clases de tkinter

    # Botón con texto estático
    class buttonStatic(tk.Button):
        def __init__(self, parent, row, col, rowspan, columnspan, text, font, bg, fg, bd, width=None, function=None,
                     sticky=None):
            super().__init__(parent, text=text, font=(font), bg=bg, fg=fg, bd=bd, width=width, command=function)
            self.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)


    # Botón con texto dinámico
    class buttonDinamic(tk.Button):
        def __init__(self, parent, row, col, rowspan, columnspan, textVar, font, bg, fg, bd, width=None, function=None,
                     sticky=None):
            super().__init__(parent, textvariable=textVar, font=(font), bg=bg, fg=fg, bd=bd, width=width,
                             command=function)
            self.grid(row=row, column=col, rowspan=rowspan, padx=padx, pady=pady, sticky=sticky)


    # Label con texto estático
    class labelStatic(tk.Label):
        def __init__(self, parent, row, col, text, font, bg, fg, sticky=None, anchor=None):
            super().__init__(parent, text=text, font=(font), bg=bg, fg=fg, anchor=anchor)
            self.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)


    # Label con texto dinámico
    class labelDinamic(tk.Label):
        def __init__(self, parent, row, col, columnspan, textVar, font, bg, fg, sticky=None, anchor=None):
            super().__init__(parent, textvariable=textVar, font=font, bg=bg, fg=fg, anchor=anchor)
            self.grid(row=row, column=col, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)


    # Entry con efecto de focus, se borra el texto cuando se utiliza entry
    class entry(tk.Entry):
        def __init__(self, parent, row, column, rowspan, columnspan, texto, bg, activeFg, defaultFg, width,
                     justify=None, sticky=None, func=None):
            super().__init__(parent, bg=bg, justify=justify, width=width, fg=defaultFg)
            self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=padx,
                      pady=pady)
            self.insert(0, texto)
            self.bind('<FocusIn>', lambda x: self.focusIn(activeFg))
            self.bind('<FocusOut>', lambda x: self.focusOut(defaultFg, texto))
            self.bind('<Return>', lambda x: self.enter(func, defaultFg, texto))

        # Se borra el texto default
        def focusIn(self, fg):
            self.config(fg=fg)

        # Se inserta nuevamente el texto default
        def focusOut(self, fg, text):
            try:
                if not self.get():
                    self.insert(0, text)
                    self.config(fg=fg)
            except:
                return

        # Funcion vinculada con la tecla enter mientras se usa entry
        def enter(self, func, fg, text):
            value = self.get()
            if func:
                func(value)
            self.focusOut(defaultFg, text)
            return value


    # Entry para contraseñas
    class passwordEntry(tk.Entry):
        def __init__(self, parent, row, column, rowspan, columnspan, texto, bg, activeFg, defaultFg, width,
                     justify=None, sticky=None, func=None):
            super().__init__(parent, show="*", bg=bg, justify=justify, width=width, fg=defaultFg)
            self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=10,
                      pady=pady)
            self.insert(0, texto)
            self.bind('<FocusIn>', lambda x: self.focusIn(activeFg))
            self.bind('<FocusOut>', lambda x: self.focusOut(defaultFg, texto))
            self.bind('<Return>', lambda x: self.enter(func, defaultFg, texto))

        # Se borra el texto default
        def focusIn(self, fg):
            self.delete(0, 'end')
            self.config(fg=fg)

        # Se inserta nuevamente el texto default
        def focusOut(self, fg, text):
            try:
                if not self.get():
                    self.insert(0, text)
                    self.config(fg=fg)
            except:
                return

        # Funcion vinculada con la tecla enter mientras se usa entry
        def enter(self, func, fg, text):
            value = self.get()
            if func:
                func(value)
            self.focusOut(defaultFg, text)
            return value


    # Listbox
    class listbox(tk.Listbox):
        def __init__(self, parent, row, col, rowspan, columnspan, font, bg, fg, sticky=None, function=None):
            super().__init__(parent, font=font, bg=bg, fg=fg)
            if function:
                self.bind('<<ListboxSelect>>', lambda x: click())
            self.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, padx=20, pady=pady, sticky=sticky)

            def click(event=None):
                try:
                    ind = self.curselection()[0]
                    if function:
                        function(ind)
                except:
                    return
                return


    # OptionMenu
    class optMenu(tk.OptionMenu):
        def __init__(self, parent, row, col, textVar, itemList, font, bg, fg, sticky, function=None):
            def click(event=None):
                if function:
                    var = "".join(re.split("[^a-zA-Z]*", variable.get()))
                    function(var)
                return

            variable = tk.StringVar(parent)
            variable.set(textVar)
            super().__init__(parent, variable, *itemList, command=click)
            self.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
            self.configure(bg=bg, activebackground=bg, font=font, fg=fg)
            self["menu"].configure(bg=bg, activebackground=bg, fg=fg)


    # Ventana emergente con texto y dos botones (uno vinculado a una funcion)
    class popUp_select(tk.Tk):
        def __init__(self, title, message, btText1, btText2, font, btFont, bg, fg, function=None):
            super().__init__()
            self.title(title)
            self.geometry('400x150')
            self.configure(bg=bg)
            self.columnconfigure(0, weight=1)

            def accept(event=None):
                self.destroy()

            def cont(event=None):
                try:
                    if function:
                        self.destroy()
                        function()
                except Exception as e:
                    print(e)
                    return

            label = labelStatic(self, 0, 0, message, font, bg, fg, 'we')
            btAccept = buttonStatic(self, 1, 0, 1, 1, btText1, btFont, bg, fg, 1, None, accept)
            btContinue = buttonStatic(self, 2, 0, 1, 1, btText2, btFont, bg, fg, 1, None, cont)
            btContinue.bind()

            self.mainloop()


    # Ventana emergente con texto y un boton
    class popUp(tk.Tk):
        def __init__(self, title, message, btText1, font, btFont, bg, fg, function=None):
            super().__init__()
            self.title(title)
            self.geometry('350x75')
            self.configure(bg=bgColor_1)
            self.columnconfigure(0, weight=1)

            def accept(event=None):
                self.destroy()

            labelStatic(self, 0, 0, message, font, bgColor_1, fg, 'we')
            buttonStatic(self, 1, 0, 1, 1, btText1, btFont, bg, fg, 1, None, accept)

            self.mainloop()


    # Slider
    class slider(tk.Scale):
        def __init__(self, parent, row, column, rowspan, columnspan, start, end, orient, bg, fg, length=None, interval=None,
                     sticky=None, func=None):
            super().__init__(parent, from_=start, to=end, orient=orient, length=length, bg=bg, fg=fg, bd=0, highlightthickness=0,
                             resolution=interval, command=func)
            self.grid(row=row,column=column,rowspan=rowspan, columnspan=columnspan,sticky=sticky, padx=padx, pady=pady)


    ### Clases especificas (borrar innecesarias)

    class auxObj:
        def __init__(self, value):
            self.value = value
            return
