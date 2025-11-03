"""
ClientePanel - Panel de gestión de clientes actualizado según modelo de dominio
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import date


class ClientePanel:
    """Panel para gestionar clientes con CustomTkinter"""
    
    def __init__(self, parent, cliente_service):
        self.parent = parent
        self.cliente_service = cliente_service
        self.selected_cliente_id = None
        
        # Configurar parent
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        
        self._create_form()
        self._create_table()
        self._load_clientes()
    
    def _create_form(self):
        """Crea el formulario de clientes"""
        # Frame del formulario
        form_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Título
        title = ctk.CTkLabel(
            form_frame,
            text=" Datos del Cliente",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(20, 30), padx=20)
        
        # DNI
        dni_label = ctk.CTkLabel(form_frame, text="DNI:", font=ctk.CTkFont(size=13))
        dni_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.dni_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: 12345678A",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.dni_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Nombre
        nombre_label = ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=13))
        nombre_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.nombre_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: Juan",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.nombre_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Apellidos
        apellidos_label = ctk.CTkLabel(form_frame, text="Apellidos:", font=ctk.CTkFont(size=13))
        apellidos_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.apellidos_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: Pérez García",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.apellidos_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Email
        email_label = ctk.CTkLabel(form_frame, text="Correo Electrónico:", font=ctk.CTkFont(size=13))
        email_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="ejemplo@email.com",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.email_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Fecha de Nacimiento
        fecha_label = ctk.CTkLabel(form_frame, text="Fecha Nacimiento:", font=ctk.CTkFont(size=13))
        fecha_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.fecha_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="YYYY-MM-DD",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.fecha_entry.pack(fill="x", padx=30, pady=(0, 20))
        
        # Botones
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        self.btn_crear = ctk.CTkButton(
            button_frame,
            text=" Crear Cliente",
            command=self._crear_cliente,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E")
        )
        self.btn_crear.pack(fill="x", pady=5)
        
        self.btn_actualizar = ctk.CTkButton(
            button_frame,
            text=" Actualizar",
            command=self._actualizar_cliente,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#1F618D", "#154360"),
            hover_color=("#2874A6", "#1B5A7E")
        )
        self.btn_actualizar.pack(fill="x", pady=5)
        
        self.btn_eliminar = ctk.CTkButton(
            button_frame,
            text=" Eliminar",
            command=self._eliminar_cliente,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#A93226", "#7B1F1F"),
            hover_color=("#C0392B", "#922B21")
        )
        self.btn_eliminar.pack(fill="x", pady=5)
        
        self.btn_limpiar = ctk.CTkButton(
            button_frame,
            text=" Limpiar",
            command=self._limpiar_formulario,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#5D6D7E", "#34495E"),
            hover_color=("#707B7C", "#566573")
        )
        self.btn_limpiar.pack(fill="x", pady=5)
    
    def _create_table(self):
        """Crea la tabla de clientes"""
        # Frame de la tabla
        table_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        table_frame.grid(row=0, column=1, sticky="nsew")
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text=" Lista de Clientes",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(side="left")
        
        # Frame scrollable para la tabla
        self.scrollable_frame = ctk.CTkScrollableFrame(
            table_frame,
            corner_radius=10
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Headers
        headers = ["DNI", "Nombre", "Apellidos", "Email"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.scrollable_frame,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=("#2B7A78", "#14443F"),
                corner_radius=5,
                height=35
            )
            label.grid(row=0, column=col, sticky="ew", padx=5, pady=5)
    
    def _load_clientes(self):
        """Carga todos los clientes en la tabla"""
        # Limpiar tabla (mantener headers)
        for widget in self.scrollable_frame.winfo_children()[4:]:
            widget.destroy()
        
        try:
            clientes = self.cliente_service.listar_clientes()
            
            for idx, cliente in enumerate(clientes, start=1):
                row = idx
                # Alternar colores
                bg_color = ("gray85", "gray20") if row % 2 == 0 else ("white", "gray25")
                
                # DNI
                dni_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                dni_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
                dni_label = ctk.CTkLabel(
                    dni_frame,
                    text=cliente.dni,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                dni_label.pack(fill="x", padx=10, pady=8)
                
                # Nombre
                nombre_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                nombre_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                nombre_label = ctk.CTkLabel(
                    nombre_frame,
                    text=cliente.nombre,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                nombre_label.pack(fill="x", padx=10, pady=8)
                
                # Apellidos
                apellidos_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                apellidos_frame.grid(row=row, column=2, sticky="ew", padx=5, pady=2)
                apellidos_label = ctk.CTkLabel(
                    apellidos_frame,
                    text=cliente.apellidos,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                apellidos_label.pack(fill="x", padx=10, pady=8)
                
                # Email
                email_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                email_frame.grid(row=row, column=3, sticky="ew", padx=5, pady=2)
                email_label = ctk.CTkLabel(
                    email_frame,
                    text=cliente.correo_electronico,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                email_label.pack(fill="x", padx=10, pady=8)
                
                # Hacer clickeable
                for frame in [dni_frame, nombre_frame, apellidos_frame, email_frame]:
                    frame.bind("<Button-1>", lambda e, c=cliente: self._select_cliente(c))
                    for child in frame.winfo_children():
                        child.bind("<Button-1>", lambda e, c=cliente: self._select_cliente(c))
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
    
    def _select_cliente(self, cliente):
        """Selecciona un cliente y carga sus datos en el formulario"""
        self.selected_cliente_id = cliente.id_cliente
        
        self.dni_entry.delete(0, "end")
        self.dni_entry.insert(0, cliente.dni)
        
        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, cliente.nombre)
        
        self.apellidos_entry.delete(0, "end")
        self.apellidos_entry.insert(0, cliente.apellidos)
        
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, cliente.correo_electronico)
        
        if cliente.fecha_nacimiento:
            self.fecha_entry.delete(0, "end")
            self.fecha_entry.insert(0, cliente.fecha_nacimiento.strftime("%Y-%m-%d"))
    
    def _crear_cliente(self):
        """Crea un nuevo cliente"""
        try:
            nombre = self.nombre_entry.get().strip()
            apellidos = self.apellidos_entry.get().strip()
            email = self.email_entry.get().strip()
            dni = self.dni_entry.get().strip()
            fecha_nac = self.fecha_entry.get().strip()
            
            if not all([nombre, apellidos, email, dni, fecha_nac]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                return
            
            self.cliente_service.crear_cliente(
                nombre=nombre,
                apellidos=apellidos,
                correo=email,
                dni=dni,
                fecha_nacimiento=fecha_nac
            )
            messagebox.showinfo("Éxito", "Cliente creado correctamente")
            self._limpiar_formulario()
            self._load_clientes()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear cliente: {str(e)}")
    
    def _actualizar_cliente(self):
        """Actualiza un cliente existente"""
        try:
            if not self.selected_cliente_id:
                messagebox.showwarning("Advertencia", "Debe seleccionar un cliente")
                return
            
            nombre = self.nombre_entry.get().strip()
            apellidos = self.apellidos_entry.get().strip()
            email = self.email_entry.get().strip()
            fecha_nac = self.fecha_entry.get().strip()
            
            if not all([nombre, apellidos, email]):
                messagebox.showwarning("Advertencia", "Nombre, apellidos y email son obligatorios")
                return
            
            self.cliente_service.actualizar_cliente(
                id_cliente=self.selected_cliente_id,
                nombre=nombre,
                apellidos=apellidos,
                correo=email,
                fecha_nacimiento=fecha_nac if fecha_nac else None
            )
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self._limpiar_formulario()
            self._load_clientes()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")
    
    def _eliminar_cliente(self):
        """Elimina un cliente"""
        try:
            if not self.selected_cliente_id:
                messagebox.showwarning("Advertencia", "Debe seleccionar un cliente")
                return
            
            nombre = self.nombre_entry.get().strip()
            
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cliente {nombre}?"):
                self.cliente_service.eliminar_cliente(self.selected_cliente_id)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self._limpiar_formulario()
                self._load_clientes()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
    
    def _limpiar_formulario(self):
        """Limpia el formulario"""
        self.selected_cliente_id = None
        self.dni_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.apellidos_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")
