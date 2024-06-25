from tkinter import ttk
from tkinter import *
import sys
sys.path.append('C:/Users/Administrator/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/LocalCache/local-packages/python311/site-packages')
from fpdf import FPDF
import mysql.connector
import tkinter.messagebox as messagebox

class Login:
    db_config = {
        'user': 'root',
        'password': '1234',
        'host': 'localhost',
        'database': 'consultorio'
    }

    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.configure(bg='#EDEAE0')

        frame = LabelFrame(self.root, text='Login', bg='#98DDDE', fg='#007F7F', font=('Verdana', 14, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky=N+S+E+W)

        Label(frame, text='Usuario: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.username = Entry(frame, font=('Verdana', 12))
        self.username.grid(row=1, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Contraseña: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=2, column=0, pady=5, padx=5, sticky=W)
        self.password = Entry(frame, show='*', font=('Verdana', 12))
        self.password.grid(row=2, column=1, pady=5, padx=5, sticky=E+W)

        ttk.Button(frame, text='Iniciar Sesión', command=self.check_login).grid(row=3, columnspan=2, sticky=W+E, pady=10)

        self.message = Label(text='', fg='red', bg='#EDEAE0', font=('Verdana', 10, 'italic'))
        self.message.grid(row=4, column=0, columnspan=2, sticky=W+E)

    def run_query(self, query, parameters=()):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def check_login(self):
        query = 'SELECT * FROM users WHERE name = %s AND password = %s'
        parameters = (self.username.get(), self.password.get())
        result = self.run_query(query, parameters)
        user = result[0] if result else None
        if user:
            self.root.destroy()
            main(user[3])  # Pasar el rol del usuario a la función principal
        else:
            self.message['text'] = 'Usuario o contraseña incorrecta'

class Appointment:
    db_config = {
        'user': 'root',
        'password': '1234',
        'host': 'localhost',
        'database': 'consultorio',
    }

    def __init__(self, window, user_role):
        self.wind = window
        self.user_role = user_role
        self.wind.title('Nohelia Bracho Consultorio')
        self.wind.configure(bg='#EDEAE0')

        for i in range(4):
            Grid.columnconfigure(self.wind, i, weight=1)
        for i in range(8):
            Grid.rowconfigure(self.wind, i, weight=1)

        self.create_table()

        frame = LabelFrame(self.wind, text='Registrar nueva Cita', bg='#98DDDE', fg='#007F7F', font=('Verdana', 14, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky=N+S+E+W)

        Label(frame, text='Nombre: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.name = Entry(frame, font=('Verdana', 12))
        self.name.focus()
        self.name.grid(row=1, column=1, pady=5, padx=5, sticky=E+W)

        # Validaciones
        vcmd_name = (self.wind.register(self.validate_name), '%P')
        vcmd_appointment = (self.wind.register(self.validate_appointment), '%P')
        vcmd_hora = (self.wind.register(self.validate_hora), '%P')

        Label(frame, text='Fecha: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=2, column=0, pady=5, padx=5, sticky=W)
        # self.appointment = Entry(frame, font=('Verdana', 12), validate='key', validatecommand=vcmd_appointment)
        # self.appointment.grid(row=2, column=1, pady=5, padx=5, sticky=E+W)
        self.dia = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.dia['values'] = [str(i) for i in range(1, 32)]
        self.dia.grid(row=2, column=1, pady=5, padx=5, sticky=E+W)
        self.dia.current(0)  # Selecciona el primer día por defecto

        self.mes = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.mes['values'] = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.mes.grid(row=2, column=2, pady=5, padx=5, sticky=E+W)
        self.mes.current(0)  # Selecciona el primer mes por defecto

        self.ano = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.ano['values'] = [str(i) for i in range(2023, 2033)]
        self.ano.grid(row=2, column=3, pady=5, padx=5, sticky=E+W)
        self.ano.current(0)  # Selecciona el primer año por defecto
        

        Label(frame, text='Hora: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=3, column=0, pady=5, padx=5, sticky=W)
        self.hora = Entry(frame, font=('Verdana', 12), validate='key', validatecommand=vcmd_hora)
        self.hora.grid(row=3, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Tratamiento: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=4, column=0, pady=5, padx=5, sticky=W)
        self.tratamiento = Entry(frame, font=('Verdana', 12), validate='key', validatecommand=vcmd_name)
        self.tratamiento.grid(row=4, column=1, pady=5, padx=5, sticky=E+W)

        # Combobox para seleccionar médico
        Label(frame, text='Médico: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=5, column=0, pady=5, padx=5, sticky=W)
        self.medico = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.medico['values'] = ['DRa Nohelia Bracho', 'DR Armando Mendoza']
        self.medico.grid(row=5, column=1, pady=5, padx=5, sticky=E+W)
        self.medico.current(0)  # Selecciona por defecto "Armando Mendoza"

        self.save_button = ttk.Button(frame, text='Guardar Cita', command=self.add_appointment)
        self.save_button.grid(row=6, columnspan=2, sticky=W + E, pady=10)

        self.message = Label(text='', fg='red', bg='#EDEAE0', font=('Verdana', 10, 'italic'))
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        self.tree = ttk.Treeview(height=10, columns=('cita', 'hora', 'tratamiento', 'medico'))
        self.tree.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky=N+S+E+W)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('cita', text='Cita', anchor=CENTER)
        self.tree.heading('hora', text='Hora', anchor=CENTER)
        self.tree.heading('tratamiento', text='Tratamiento', anchor=CENTER)
        self.tree.heading('medico', text='Medico', anchor=CENTER)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#98DDDE", font=('Verdana', 12, 'bold'))

        self.delete_button = ttk.Button(text='ELIMINAR', command=self.delete_appointment)
        self.delete_button.grid(row=5, column=0, sticky=W + E, padx=10, pady=5)

        self.edit_button = ttk.Button(text='EDITAR', command=self.edit_appointment)
        self.edit_button.grid(row=5, column=1, sticky=W + E, padx=10, pady=5)

        self.export_all_button = ttk.Button(text='Exportar Todo a PDF', command=self.export_all_to_pdf)
        self.export_all_button.grid(row=6, column=0, sticky=W + E, padx=10, pady=5)

        self.export_selected_button = ttk.Button(text='Exportar Seleccionados a PDF', command=self.export_selected_to_pdf)
        self.export_selected_button.grid(row=6, column=1, sticky=W + E, padx=10, pady=5)

        self.client_button = ttk.Button(text='Agregar Cliente', command=self.edit_clients)
        self.client_button.grid(row=7, column=0, sticky=W + E, padx=10, pady=5)

        self.medico_button = ttk.Button(text='Agregar medico', command=self.view_medico)
        self.medico_button.grid(row=7, column=1, sticky=W + E, padx=10, pady=5)


        self.get_appointments()
        

        if self.user_role == 2:
            self.delete_button.grid_remove()
            self.export_all_button.grid_remove()
            self.export_selected_button.grid_remove()


    def validate_name(self, new_value):
        return new_value.isalpha() or new_value == ""

    def validate_appointment(self, new_value):
        return all(c.isdigit() or c in ";/?:." for c in new_value) or new_value == ""

    def validate_hora(self, new_value):
        return all(c.isdigit() or c in ";/?:.ampAMP" for c in new_value) or new_value == ""


    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS appointment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cita VARCHAR(100) NOT NULL,
            hora VARCHAR(50) NOT NULL,
            tratamiento VARCHAR(100) NOT NULL
        )
        '''
        self.run_query(query)

    def run_query(self, query, parameters=()):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def get_appointments(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM appointment_view ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[4], row[5]))

    def get_pacientes(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM pacientes ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def get_medicos(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM medicos ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            print(row)
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))           

    def validation(self):
        return len(self.name.get()) != 0 and len(self.dia.get()) != 0 and len(self.mes.get()) != 0 and len(self.ano.get()) != 0 and len(self.hora.get()) != 0

    def add_appointment(self):
        if self.validation():
            print(self.medico.get())
            medico_index = self.medico.current()
            medico_id = medico_index + 1
            query = 'INSERT INTO appointment (name, appointment, hora, tratamiento, medico_id) VALUES (%s, %s, %s, %s, %s)'
            parameters = (self.name.get(), self.dia.get()+self.mes.get()+self.ano.get(), self.hora.get(), self.tratamiento.get(), medico_id)
            self.run_query(query, parameters)
            self.message['text'] = 'Cita {} añadida satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.dia.delete(0, END)
            self.mes.delete(0, END)
            self.ano.delete(0, END)
            self.hora.delete(0, END)
            self.tratamiento.delete(0, END)
            self.medico.delete(0, END)
        else:
            self.message['text'] = 'Nombre, cita y hora son requeridos'
        self.get_appointments()

    def add_paciente(self):
            query = 'INSERT INTO pacientes (name, apellido, cedula, telefono) VALUES (%s, %s, %s, %s)'
            parameters = (self.name.get(), self.apellido.get(),self.cedula.get(), self.telefono.get())
            self.run_query(query, parameters)
            self.message['text'] = 'paciente {} añadido satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.apellido.delete(0, END)
            self.cedula.delete(0, END)
            self.telefono.delete(0, END)
            self.get_pacientes()
    
    def add_medico(self):
            query = 'INSERT INTO medicos (name, apellido, telefono) VALUES (%s, %s, %s)'
            parameters = (self.name_medico.get(), self.apellido_medico.get(), self.telefono_medico.get())
            self.run_query(query, parameters)
            self.message['text'] = 'medico {} añadido satisfactoriamente'.format(self.name_medico.get())
            self.name_medico.delete(0, END)
            self.apellido_medico.delete(0, END)
            self.telefono_medico.delete(0, END)
            self.get_medicos()
    
    def delete_appointment(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                self.message['text'] = 'Por favor selecciona una cita'
                return

            confirmation = messagebox.askyesno('Confirmación', '¿Estás seguro que deseas eliminar esta cita?')
            if confirmation:
                self.message['text'] = ''
                name = self.tree.item(selected_item)['text']
                query = 'DELETE FROM appointment WHERE name = %s'
                self.run_query(query, (name,))
                self.message['text'] = 'Cita {} eliminada satisfactoriamente'.format(name)
                self.get_appointments()
        except Exception as e:
            print(e)
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona una cita'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM appointment WHERE name = %s'
        self.run_query(query, (name,))
        self.message['text'] = 'Cita {} eliminada satisfactoriamente'.format(name)
        self.get_appointments()

    def edit_appointment(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona una cita'
            return
        
        name = self.tree.item(self.tree.selection())['text']
        old_cita = self.tree.item(self.tree.selection())['values'][0]
        old_hora = self.tree.item(self.tree.selection())['values'][1]
        old_tratamiento = self.tree.item(self.tree.selection())['values'][2]
        # Validaciones
        vcmd_name = (self.wind.register(self.validate_name), '%P')
        vcmd_appointment = (self.wind.register(self.validate_appointment), '%P')
        vcmd_hora = (self.wind.register(self.validate_hora), '%P')
        
        self.edit_wind = Toplevel()
        self.edit_wind.title('Editar Cita')

        for i in range(4):
            Grid.columnconfigure(self.edit_wind, i, weight=1)
        for i in range(9):  # Ajuste del número de filas para que el botón 'Actualizar' sea visible
            Grid.rowconfigure(self.edit_wind, i, weight=1)

        frame = LabelFrame(self.edit_wind, text='Editar Cita', bg='#98DDDE', fg='#007F7F', font=('Verdana', 14, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky=N+S+E+W)

        Label(frame, text='Nombre antiguo: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=0, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=StringVar(self.edit_wind, value=name), state='readonly', font=('Verdana', 12)).grid(row=0, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Fecha antigua: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=1, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=StringVar(self.edit_wind, value=old_cita), state='readonly', font=('Verdana', 12)).grid(row=1, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Hora antigua: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=2, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=StringVar(self.edit_wind, value=old_hora), state='readonly', font=('Verdana', 12)).grid(row=2, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Tratamiento antiguo: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=3, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=StringVar(self.edit_wind, value=old_tratamiento), state='readonly', font=('Verdana', 12)).grid(row=3, column=1, pady=5, padx=5, sticky=E+W)

        # self.new_cita = StringVar(self.edit_wind, value=old_cita)
        Label(frame, text='Nueva Fecha: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=4, column=0, pady=5, padx=5, sticky=W)
        # Entry(frame, textvariable=self.new_cita, font=('Verdana', 12), validate='key', validatecommand=vcmd_appointment).grid(row=4, column=1, pady=5, padx=5, sticky=E+W)
        
        self.dia = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.dia['values'] = [str(i) for i in range(1, 32)]
        self.dia.grid(row=4, column=1, pady=5, padx=5, sticky=E+W)
        self.dia.current(0)  # Selecciona el primer día por defecto

        self.mes = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.mes['values'] = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.mes.grid(row=4, column=2, pady=5, padx=5, sticky=E+W)
        self.mes.current(0)  # Selecciona el primer mes por defecto

        self.ano = ttk.Combobox(frame, font=('Verdana', 12), state='readonly')
        self.ano['values'] = [str(i) for i in range(2023, 2033)]
        self.ano.grid(row=4, column=3, pady=5, padx=5, sticky=E+W)
        self.ano.current(0)  # Selecciona el primer año por defecto

        self.new_hora = StringVar(self.edit_wind, value=old_hora)
        Label(frame, text='Nueva Hora: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=5, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=self.new_hora, font=('Verdana', 12), validate='key', validatecommand=vcmd_hora).grid(row=5, column=1, pady=5, padx=5, sticky=E+W)

        self.new_tratamiento = StringVar(self.edit_wind, value=old_tratamiento)
        Label(frame, text='Nuevo Tratamiento: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=6, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=self.new_tratamiento, font=('Verdana', 12), validate='key', validatecommand=vcmd_name).grid(row=6, column=1, pady=5, padx=5, sticky=E+W)

        self.new_name = StringVar(self.edit_wind, value=name)
        Label(frame, text='Nuevo Nombre: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=7, column=0, pady=5, padx=5, sticky=W)
        Entry(frame, textvariable=self.new_name, font=('Verdana', 12)).grid(row=7, column=1, pady=5, padx=5, sticky=E+W)

        ttk.Button(frame, text='Actualizar', command=lambda: self.update_appointments(name, self.dia.get()+self.mes.get()+self.ano.get(), self.new_hora.get(), self.new_tratamiento.get(), self.new_name.get(),old_cita,old_hora,old_tratamiento)).grid(row=8, columnspan=2, sticky=W + E, pady=10)

    def edit_clients(self):
        self.client_wind = Toplevel()
        self.client_wind.title('Editar Cita')
        for i in range(4):
            Grid.columnconfigure(self.client_wind, i, weight=1)
        for i in range(9):  # Ajuste del número de filas para que el botón 'Actualizar' sea visible
            Grid.rowconfigure(self.client_wind, i, weight=1)

        frame = LabelFrame(self.client_wind, text='Editar Cita', bg='#98DDDE', fg='#007F7F', font=('Verdana', 14, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky=N+S+E+W)
        Label(frame, text='Nombre: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.name = Entry(frame, font=('Verdana', 12))
        self.name.focus()
        self.name.grid(row=1, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Apellido: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=2, column=0, pady=5, padx=5, sticky=W)
        self.apellido = Entry(frame, font=('Verdana', 12))
        self.apellido.focus()
        self.apellido.grid(row=2, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='cedula: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=3, column=0, pady=5, padx=5, sticky=W)
        self.cedula = Entry(frame, font=('Verdana', 12))
        self.cedula.focus()
        self.cedula.grid(row=3, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='telefono: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=4, column=0, pady=5, padx=5, sticky=W)
        self.telefono = Entry(frame, font=('Verdana', 12))
        self.telefono.focus()
        self.telefono.grid(row=4, column=1, pady=5, padx=5, sticky=E+W)

        self.tree = ttk.Treeview(height=10, columns=('cita', 'hora', 'tratamiento', 'medico'))
        self.tree.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky=N+S+E+W)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('cita', text='Cita', anchor=CENTER)
        self.tree.heading('hora', text='Hora', anchor=CENTER)
        self.tree.heading('tratamiento', text='Tratamiento', anchor=CENTER)
        self.tree.heading('medico', text='Medico', anchor=CENTER)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#98DDDE", font=('Verdana', 12, 'bold'))

        self.save_button = ttk.Button(frame, text='Guardar Paciente', command=self.add_paciente)
        self.save_button.grid(row=6, columnspan=2, sticky=W + E, pady=10)
        self.get_appointments()

    def view_medico(self):
        self.medico_wind = Toplevel()
        self.medico_wind.title('Agregar Medico')
        for i in range(4):
            Grid.columnconfigure(self.medico_wind, i, weight=1)
        for i in range(9):  # Ajuste del número de filas para que el botón 'Actualizar' sea visible
            Grid.rowconfigure(self.medico_wind, i, weight=1)

        frame = LabelFrame(self.medico_wind, text='Editar Cita', bg='#98DDDE', fg='#007F7F', font=('Verdana', 14, 'bold'))
        frame.grid(row=0, column=0, columnspan=4, pady=20, padx=20, sticky=N+S+E+W)
        Label(frame, text='Nombre: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.name_medico = Entry(frame, font=('Verdana', 12))
        self.name_medico.focus()
        self.name_medico.grid(row=1, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Apellido: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=2, column=0, pady=5, padx=5, sticky=W)
        self.apellido_medico = Entry(frame, font=('Verdana', 12))
        self.apellido_medico.grid(row=2, column=1, pady=5, padx=5, sticky=E+W)

        Label(frame, text='Telefono: ', bg='#98DDDE', fg='#007F7F', font=('Verdana', 12)).grid(row=3, column=0, pady=5, padx=5, sticky=W)
        self.telefono_medico = Entry(frame, font=('Verdana', 12))
        self.telefono_medico.grid(row=3, column=1, pady=5, padx=5, sticky=E+W)

        # No duplicamos self.tree
        medico_tree = ttk.Treeview(height=10, columns=('cita', 'hora', 'tratamiento', 'medico'))
        medico_tree.grid(row=5, column=0, columnspan=4, pady=10, padx=20, sticky=N+S+E+W)
        medico_tree.heading('#0', text='Nombre', anchor=CENTER)
        medico_tree.heading('cita', text='Cita', anchor=CENTER)
        medico_tree.heading('hora', text='Hora', anchor=CENTER)
        medico_tree.heading('tratamiento', text='Tratamiento', anchor=CENTER)
        medico_tree.heading('medico', text='Medico', anchor=CENTER)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#98DDDE", font=('Verdana', 12, 'bold'))

        self.save_button = ttk.Button(frame, text='Guardar Medico', command=self.add_medico)
        self.save_button.grid(row=4, columnspan=2, sticky=W + E, pady=10)
        self.get_appointments()

        def update_appointments(self, name, new_cita, new_hora, new_tratamiento, new_name,old_cita, old_hora, old_tratamiento):        
            query = '''
            UPDATE appointment SET appointment = %s, hora = %s, tratamiento = %s, name = %s
            WHERE name = %s AND appointment = %s AND hora = %s AND tratamiento = %s
            '''
            parameters = (new_cita, new_hora, new_tratamiento, new_name, name, old_cita, old_hora, old_tratamiento)
            self.run_query(query, parameters)
            self.edit_wind.destroy()
            self.message['text'] = 'Cita de {} actualizada satisfactoriamente'.format(name)
            self.get_appointments()

    def export_all_to_pdf(self):
        query = 'SELECT name, appointment, hora, tratamiento, medico FROM appointment_view ORDER BY name DESC'
        db_rows = self.run_query(query)
        self.export_to_pdf(db_rows,'Citas')

    def export_selected_to_pdf(self):
        selected_items = self.tree.selection()
        if not selected_items:
            self.message['text'] = 'Por favor selecciona al menos una cita para exportar'
            return
        selected_appointments = []
        for item in selected_items:
            name = self.tree.item(item)['text']
            cita = self.tree.item(item)['values'][0]
            hora = self.tree.item(item)['values'][1]
            tratamiento = self.tree.item(item)['values'][2]
            medico = self.tree.item(item)['values'][3]
            selected_appointments.append((name, cita, hora, tratamiento, medico))
        self.export_to_pdf(selected_appointments,'Cita')

    def export_to_pdf(self, appointments,title):
       pdf = FPDF()
       pdf.add_page()
       pdf.set_font('Arial', size=12)
        
       for appointment in appointments:
            if len(appointment) < 5:
                self.message['text'] = 'Error: Se esperaba una tupla con al menos 4 elementos.'
                return
            
            # Omite el primer elemento (ID)
            name, cita, hora, tratamiento, medico = appointment
            pdf.cell(200, 10, txt=f"Nombre: {name}, Cita: {cita}, Hora: {hora}, Tratamiento: {tratamiento}, Medico: {medico}", ln=True)
        
       pdf.output(title+'.pdf')
       self.message['text'] = 'Citas exportadas a PDF satisfactoriamente'


def main(user_role):
    window = Tk()
    application = Appointment(window, user_role)
    window.mainloop()

if __name__ == '__main__':
    root = Tk()
    Login(root)
    root.mainloop()