"""
ReservaPanel - Panel de gestión de reservas con diseño moderno
"""
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime, date
from src.domain.reserva import TipoReserva
from src.ui_gui.huespedes_dialog import HuespedesDialog


class ReservaPanel:
    """Panel para gestionar reservas con CustomTkinter"""
    
    def __init__(self, parent, reserva_service, consulta_service):
        self.parent = parent
        self.reserva_service = reserva_service
        self.consulta_service = consulta_service
        self.huespedes_lista = []  # Lista de huéspedes para la reserva
        
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
        self._load_reservas()
    
    def _create_form(self):
        """Crea el formulario de reservas"""
        # Frame del formulario con scroll
        form_container = ctk.CTkScrollableFrame(self.main_container, corner_radius=15)
        form_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Título
        title = ctk.CTkLabel(
            form_container,
            text="📅 Nueva Reserva",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20), padx=20)
        
        # ID Reserva (solo para actualizar/eliminar)
        id_label = ctk.CTkLabel(form_container, text="ID Reserva:", font=ctk.CTkFont(size=13))
        id_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.id_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="Auto (solo para actualizar)",
            height=35,
            state="readonly",
            font=ctk.CTkFont(size=12)
        )
        self.id_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Cliente
        cliente_label = ctk.CTkLabel(form_container, text="Cliente (DNI):", font=ctk.CTkFont(size=13))
        cliente_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.cliente_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="DNI del cliente",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.cliente_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Hotel
        hotel_label = ctk.CTkLabel(form_container, text="Hotel:", font=ctk.CTkFont(size=13))
        hotel_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.hotel_combobox = ctk.CTkComboBox(
            form_container,
            values=self._get_hoteles(),
            height=35,
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        self.hotel_combobox.pack(fill="x", padx=30, pady=(0, 10))
        
        # Botón Volver a Seleccionar Hotel
        self.btn_cambiar_hotel = ctk.CTkButton(
            form_container,
            text="🔄 Volver a Seleccionar Hotel",
            command=self._volver_hotel,
            height=30,
            font=ctk.CTkFont(size=11),
            fg_color="#6B4423",
            hover_color="#4A2E16"
        )
        self.btn_cambiar_hotel.pack(fill="x", padx=30, pady=(0, 15))
        
        # Tipo Habitación
        tipo_hab_label = ctk.CTkLabel(form_container, text="Tipo Habitación:", font=ctk.CTkFont(size=13))
        tipo_hab_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.tipo_hab_combobox = ctk.CTkComboBox(
            form_container,
            values=self._get_tipos_habitacion(),
            height=35,
            font=ctk.CTkFont(size=12),
            state="readonly",
            command=lambda _: self._calcular_precio_total()  # Recalcular al cambiar
        )
        self.tipo_hab_combobox.pack(fill="x", padx=30, pady=(0, 15))
        
        # Régimen
        regimen_label = ctk.CTkLabel(form_container, text="Régimen:", font=ctk.CTkFont(size=13))
        regimen_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.regimen_combobox = ctk.CTkComboBox(
            form_container,
            values=self._get_regimenes(),
            height=35,
            font=ctk.CTkFont(size=12),
            state="readonly",
            command=lambda _: self._calcular_precio_total()  # Recalcular al cambiar
        )
        self.regimen_combobox.pack(fill="x", padx=30, pady=(0, 15))
        
        # Fecha Salida
        fecha_salida_label = ctk.CTkLabel(
            form_container, 
            text="Fecha Salida (YYYY-MM-DD):", 
            font=ctk.CTkFont(size=13)
        )
        fecha_salida_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.fecha_salida_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="2025-01-20",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.fecha_salida_entry.pack(fill="x", padx=30, pady=(0, 15))
        
        # Bind para recalcular cuando cambie la fecha
        self.fecha_salida_entry.bind("<KeyRelease>", lambda e: self._calcular_precio_total())
        
        # INFO: Fecha de entrada automática
        info_fecha = ctk.CTkLabel(
            form_container,
            text="ℹ️ Fecha entrada: HOY (automática)",
            font=ctk.CTkFont(size=11),
            text_color=("#5DADE2", "#3498DB")
        )
        info_fecha.pack(anchor="w", padx=30, pady=(0, 15))
        
        # Precio Total (calculado)
        precio_label = ctk.CTkLabel(
            form_container, 
            text="💰 Precio Total Estimado:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        precio_label.pack(anchor="w", padx=30, pady=(10, 0))
        
        self.precio_total_label = ctk.CTkLabel(
            form_container,
            text="0.00 €",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#27AE60", "#2ECC71")
        )
        self.precio_total_label.pack(anchor="w", padx=30, pady=(0, 15))
        
        # Tipo Reserva
        tipo_label = ctk.CTkLabel(form_container, text="Tipo Reserva:", font=ctk.CTkFont(size=13))
        tipo_label.pack(anchor="w", padx=30, pady=(5, 0))
        
        self.tipo_combobox = ctk.CTkComboBox(
            form_container,
            values=["AGENCIA", "PARTICULAR"],
            height=35,
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        self.tipo_combobox.set("PARTICULAR")
        self.tipo_combobox.pack(fill="x", padx=30, pady=(0, 20))
        
        # Botón Gestionar Huéspedes
        self.btn_huespedes = ctk.CTkButton(
            form_container,
            text="👥 Gestionar Huéspedes",
            command=self._gestionar_huespedes,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#2B5B84",
            hover_color="#1E3F5A"
        )
        self.btn_huespedes.pack(fill="x", padx=30, pady=(0, 15))
        
        # Botones
        button_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        self.btn_crear = ctk.CTkButton(
            button_frame,
            text="➕ Crear Reserva",
            command=self._crear_reserva,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E")
        )
        self.btn_crear.pack(fill="x", pady=5)
        
        self.btn_actualizar = ctk.CTkButton(
            button_frame,
            text="✏️ Actualizar",
            command=self._actualizar_reserva,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#1F618D", "#154360"),
            hover_color=("#2874A6", "#1B5A7E")
        )
        self.btn_actualizar.pack(fill="x", pady=5)
        
        self.btn_eliminar = ctk.CTkButton(
            button_frame,
            text="🗑️ Eliminar",
            command=self._eliminar_reserva,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#A93226", "#7B1F1F"),
            hover_color=("#C0392B", "#922B21")
        )
        self.btn_eliminar.pack(fill="x", pady=5)
        
        self.btn_checkin = ctk.CTkButton(
            button_frame,
            text="✅ Check-In",
            command=self._checkin,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#148F77", "#0E6655"),
            hover_color=("#16A085", "#117A65")
        )
        self.btn_checkin.pack(fill="x", pady=5)
        
        self.btn_checkout = ctk.CTkButton(
            button_frame,
            text="🚪 Check-Out",
            command=self._checkout,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#D68910", "#9C640C"),
            hover_color=("#F39C12", "#CA6F1E")
        )
        self.btn_checkout.pack(fill="x", pady=5)
        
        self.btn_limpiar = ctk.CTkButton(
            button_frame,
            text="🔄 Limpiar",
            command=self._limpiar_formulario,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#5D6D7E", "#34495E"),
            hover_color=("#707B7C", "#566573")
        )
        self.btn_limpiar.pack(fill="x", pady=5)
    
    def _create_table(self):
        """Crea la tabla de reservas"""
        # Frame de la tabla
        table_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        table_frame.grid(row=0, column=1, sticky="nsew")
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Header con título y botón
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="📋 Lista de Reservas",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        btn_refresh = ctk.CTkButton(
            header_frame,
            text="🔄 Actualizar",
            command=self._load_reservas,
            width=120,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E")
        )
        btn_refresh.grid(row=0, column=1, sticky="e", padx=10)
        
        # Scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            table_frame,
            fg_color=("gray90", "gray15")
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Headers
        headers = ["ID", "Cliente", "Hotel", "Entrada", "Salida", "Tipo"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.scrollable_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=("#2B7A78", "#14443F"),
                corner_radius=5
            )
            label.grid(row=0, column=col, sticky="ew", padx=5, pady=5)
    
    def _load_reservas(self):
        """Carga todas las reservas"""
        # Limpiar tabla
        for widget in self.scrollable_frame.winfo_children()[6:]:
            widget.destroy()
        
        try:
            reservas = self.reserva_service.listar_reservas()
            
            for idx, reserva in enumerate(reservas, start=1):
                row = idx
                bg_color = ("gray85", "gray20") if row % 2 == 0 else ("white", "gray25")
                
                # ID
                id_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                id_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
                id_label = ctk.CTkLabel(
                    id_frame,
                    text=str(getattr(reserva, 'id_reserva', 'N/A')),
                    font=ctk.CTkFont(size=12),
                    anchor="center"
                )
                id_label.pack(fill="x", padx=10, pady=8)
                
                # Cliente (DNI)
                cliente_dni = "N/A"
                if hasattr(reserva, 'cliente_paga') and reserva.cliente_paga:
                    cliente_dni = reserva.cliente_paga.dni
                elif hasattr(reserva, 'id_cliente'):
                    cliente_dni = str(reserva.id_cliente)
                    
                cliente_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                cliente_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                cliente_label = ctk.CTkLabel(
                    cliente_frame,
                    text=cliente_dni,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                cliente_label.pack(fill="x", padx=10, pady=8)
                
                # Hotel
                hotel_nombre = "N/A"
                if hasattr(reserva, 'precio_regimen') and reserva.precio_regimen and hasattr(reserva.precio_regimen, 'hotel'):
                    hotel_nombre = reserva.precio_regimen.hotel.nombre
                elif hasattr(reserva, 'id_hotel'):
                    hotel_nombre = f"Hotel #{reserva.id_hotel}"
                    
                hotel_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                hotel_frame.grid(row=row, column=2, sticky="ew", padx=5, pady=2)
                hotel_label = ctk.CTkLabel(
                    hotel_frame,
                    text=hotel_nombre,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                hotel_label.pack(fill="x", padx=10, pady=8)
                
                # Fecha Entrada
                entrada_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                entrada_frame.grid(row=row, column=3, sticky="ew", padx=5, pady=2)
                entrada_label = ctk.CTkLabel(
                    entrada_frame,
                    text=reserva.fecha_entrada.strftime("%Y-%m-%d") if reserva.fecha_entrada else "N/A",
                    font=ctk.CTkFont(size=12),
                    anchor="center"
                )
                entrada_label.pack(fill="x", padx=10, pady=8)
                
                # Fecha Salida
                salida_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                salida_frame.grid(row=row, column=4, sticky="ew", padx=5, pady=2)
                salida_label = ctk.CTkLabel(
                    salida_frame,
                    text=reserva.fecha_salida.strftime("%Y-%m-%d") if reserva.fecha_salida else "N/A",
                    font=ctk.CTkFont(size=12),
                    anchor="center"
                )
                salida_label.pack(fill="x", padx=10, pady=8)
                
                # Tipo
                tipo_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
                tipo_frame.grid(row=row, column=5, sticky="ew", padx=5, pady=2)
                tipo_label = ctk.CTkLabel(
                    tipo_frame,
                    text=reserva.tipo.name if reserva.tipo else "N/A",
                    font=ctk.CTkFont(size=12),
                    anchor="center"
                )
                tipo_label.pack(fill="x", padx=10, pady=8)
                
                # Hacer clickeable
                for frame in [id_frame, cliente_frame, hotel_frame, entrada_frame, salida_frame, tipo_frame]:
                    frame.bind("<Button-1>", lambda e, r=reserva: self._select_reserva(r))
                    for child in frame.winfo_children():
                        child.bind("<Button-1>", lambda e, r=reserva: self._select_reserva(r))
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar reservas: {str(e)}")
    
    def _select_reserva(self, reserva):
        """Selecciona una reserva y carga sus datos"""
        self.id_entry.configure(state="normal")
        self.id_entry.delete(0, "end")
        self.id_entry.insert(0, str(getattr(reserva, 'id_reserva', '')))
        self.id_entry.configure(state="readonly")
        
        # Cliente DNI
        if hasattr(reserva, 'cliente_paga') and reserva.cliente_paga:
            self.cliente_entry.delete(0, "end")
            self.cliente_entry.insert(0, reserva.cliente_paga.dni)
        
        # Fecha Salida
        if reserva.fecha_salida:
            self.fecha_salida_entry.delete(0, "end")
            self.fecha_salida_entry.insert(0, reserva.fecha_salida.strftime("%Y-%m-%d"))
        
        # Tipo
        if reserva.tipo:
            self.tipo_combobox.set(reserva.tipo.name)
    
    def _calcular_precio_total(self):
        """Calcula el precio total estimado de la reserva"""
        try:
            # Obtener datos necesarios
            hotel_str = self.hotel_combobox.get()
            tipo_hab_str = self.tipo_hab_combobox.get()
            regimen_str = self.regimen_combobox.get()
            fecha_salida_str = self.fecha_salida_entry.get().strip()
            
            # Si falta algún dato, mostrar 0.00
            if not all([hotel_str, tipo_hab_str, regimen_str, fecha_salida_str]):
                self.precio_total_label.configure(text="0.00 €")
                return
            
            # Parsear fecha de salida
            try:
                fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
            except:
                self.precio_total_label.configure(text="Fecha inválida")
                return
            
            # Fecha de entrada es HOY
            fecha_entrada = date.today()
            
            # Validar que la fecha de salida sea posterior a hoy
            if fecha_salida <= fecha_entrada:
                self.precio_total_label.configure(text="Fecha salida debe ser posterior")
                return
            
            # Calcular número de noches
            noches = (fecha_salida - fecha_entrada).days
            
            # Obtener precio del régimen desde la API
            # Formato: "ID - CODIGO"
            nombre_hotel = hotel_str.split(" - ")[1]
            codigo_regimen = regimen_str.split(" - ")[1]
            
            # Buscar el precio del régimen para este hotel
            response = self.reserva_service._repository._api.get(
                f"precios-regimen?hotel={nombre_hotel}&regimen={codigo_regimen}"
            )
            
            if response and response.success and response.data:
                # Asumir que retorna un array de precios
                precios = response.data if isinstance(response.data, list) else [response.data]
                if precios and len(precios) > 0 and precios[0]:
                    # Verificar que el primer elemento no sea None
                    precio_item = precios[0]
                    if isinstance(precio_item, dict) and 'precio' in precio_item:
                        precio_por_noche = float(precio_item.get('precio', 0))
                        precio_total = precio_por_noche * noches
                        
                        self.precio_total_label.configure(
                            text=f"{precio_total:.2f} € ({noches} noche{'s' if noches > 1 else ''} × {precio_por_noche:.2f}€)"
                        )
                        return
            
            # Si no se pudo obtener el precio, mostrar mensaje
            self.precio_total_label.configure(text="No disponible")
            
        except Exception as e:
            print(f"Error al calcular precio: {e}")
            import traceback
            traceback.print_exc()
            self.precio_total_label.configure(text="0.00 €")
    
    def _get_hoteles(self):
        """Obtiene lista de hoteles"""
        try:
            hoteles = self.consulta_service.obtener_hoteles()
            return [f"{h.id_hotel} - {h.nombre}" for h in hoteles]
        except:
            return []
    
    def _get_tipos_habitacion(self):
        """Obtiene tipos de habitación"""
        try:
            tipos = self.consulta_service.obtener_tipos_habitacion()
            return [f"{t.id_tipo_habitacion} - {t.tipo}" for t in tipos]
        except:
            return []
    
    def _get_regimenes(self):
        """Obtiene regímenes"""
        try:
            regimenes = self.consulta_service.obtener_regimenes()
            return [f"{r.id_regimen} - {r.codigo}" for r in regimenes]
        except:
            return []
    
    def _gestionar_huespedes(self):
        """Abre el diálogo para gestionar huéspedes de la reserva"""
        try:
            # Obtener tipo de habitación seleccionado
            tipo_hab_str = self.tipo_hab_combobox.get()
            if not tipo_hab_str:
                messagebox.showwarning("Advertencia", "Primero selecciona un tipo de habitación")
                return
            
            # Extraer nombre del tipo de habitación y calcular capacidad
            nombre_tipo = tipo_hab_str.split(" - ")[1]
            capacidades = {
                "Individual": 1,
                "Doble": 2,
                "Suite Junior": 4
            }
            capacidad = capacidades.get(nombre_tipo, 2)  # Default 2 si no se encuentra
            
            # Abrir diálogo
            dialog = HuespedesDialog(self.parent, capacidad, nombre_tipo)
            dialog.wait_window()
            
            # Guardar resultado si no fue cancelado
            if dialog.result is not None:
                self.huespedes_lista = dialog.result
                messagebox.showinfo(
                    "Huéspedes Actualizados",
                    f"Se han configurado {len(self.huespedes_lista)} huésped(es) además del cliente titular"
                )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al gestionar huéspedes: {str(e)}")
    
    def _volver_hotel(self):
        """Resetea la selección de hotel y limpia el formulario"""
        self._limpiar_formulario()
        self.huespedes_lista = []
        messagebox.showinfo("Reseteo", "Formulario reiniciado. Puedes seleccionar un nuevo hotel")
    
    def _crear_reserva(self):
        """Crea una nueva reserva y hace check-in automáticamente"""
        try:
            dni = self.cliente_entry.get().strip()
            hotel_str = self.hotel_combobox.get()
            tipo_hab_str = self.tipo_hab_combobox.get()
            regimen_str = self.regimen_combobox.get()
            fecha_salida_str = self.fecha_salida_entry.get().strip()
            tipo_str = self.tipo_combobox.get()
            
            if not all([dni, hotel_str, tipo_hab_str, regimen_str, fecha_salida_str]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                return
            
            # Validar que el cliente existe (asumiendo que debe existir antes)
            # Si no existe, el backend lo creará
            
            # Extraer nombres de hotel, tipo habitación y régimen
            nombre_hotel = hotel_str.split(" - ")[1]
            nombre_tipo_hab = tipo_hab_str.split(" - ")[1]
            codigo_regimen = regimen_str.split(" - ")[1]
            
            # Fecha de entrada es HOY (fecha actual local)
            fecha_entrada = date.today()
            
            # Parsear fecha de salida
            fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
            
            # Validar fechas
            if fecha_salida <= fecha_entrada:
                messagebox.showerror("Error", "La fecha de salida debe ser posterior a hoy")
                return
            
            # Construir objeto clientePaga (el que crea la reserva)
            # Nota: El backend buscará o creará el cliente
            cliente_paga = {
                "DNI": dni,
                "nombre": "Cliente",  # Placeholder - el backend debería tener estos datos
                "apellidos": "Titular",
                "correoElectronico": f"{dni}@example.com"  # Placeholder
            }
            
            # Preparar tipo de reserva
            tipo_reserva = "AGENCIA" if tipo_str == "AGENCIA" else "PARTICULAR"
            
            # Preparar payload para crear reserva
            payload = {
                "fechaEntrada": fecha_entrada.isoformat() + "T00:00:00",  # Local time con T00:00:00
                "fechaSalida": fecha_salida.isoformat() + "T00:00:00",
                "tipo": tipo_reserva,
                "clientePaga": cliente_paga,
                "hotel": nombre_hotel,
                "tipoHabitacion": nombre_tipo_hab,
                "regimen": codigo_regimen,
                "huespedes": self.huespedes_lista  # Incluir huéspedes gestionados
            }
            
            # Crear la reserva
            response = self.reserva_service._repository._api.post("reservas", payload)
            
            if not response.success:
                messagebox.showerror("Error", f"Error al crear reserva: {response.error}")
                return
            
            reserva_creada = response.data
            id_reserva = reserva_creada.get("idReserva")
            
            if not id_reserva:
                messagebox.showerror("Error", "No se pudo obtener el ID de la reserva creada")
                return
            
            # Preguntar número de habitación para check-in
            numero_habitacion = simpledialog.askstring(
                "Check-in",
                f"Reserva creada exitosamente (ID: {id_reserva})\n\n"
                f"Ingrese el número de habitación para hacer check-in automático:"
            )
            
            if not numero_habitacion:
                messagebox.showinfo(
                    "Reserva Creada",
                    f"Reserva creada correctamente (ID: {id_reserva})\n"
                    "Check-in no realizado (puede hacerlo manualmente después)"
                )
                self._limpiar_formulario()
                self.huespedes_lista = []
                self._load_reservas()
                return
            
            # Hacer check-in automáticamente
            checkin_payload = {
                "numeroHabitacion": numero_habitacion,
                "huespedes": self.huespedes_lista  # Incluir huéspedes en el check-in
            }
            
            checkin_response = self.reserva_service._repository._api.post(
                f"reservas/{id_reserva}/checkin",
                checkin_payload
            )
            
            if not checkin_response.success:
                messagebox.showwarning(
                    "Advertencia",
                    f"Reserva creada correctamente (ID: {id_reserva})\n\n"
                    f"Error al hacer check-in: {checkin_response.error}\n\n"
                    "Puede realizar el check-in manualmente"
                )
            else:
                messagebox.showinfo(
                    "Éxito",
                    f"✅ Reserva creada (ID: {id_reserva})\n"
                    f"✅ Check-in realizado\n"
                    f"✅ Habitación: {numero_habitacion}\n"
                    f"✅ Huéspedes: {len(self.huespedes_lista)} + 1 (titular)"
                )
            
            # Limpiar formulario y recargar
            self._limpiar_formulario()
            self.huespedes_lista = []
            self._load_reservas()
            
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de fecha inválido: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva: {str(e)}")
    
    def _actualizar_reserva(self):
        """Actualiza una reserva"""
        try:
            id_str = self.id_entry.get().strip()
            if not id_str:
                messagebox.showwarning("Advertencia", "Debe seleccionar una reserva")
                return
            
            id_reserva = int(id_str)
            dni = self.cliente_entry.get().strip()
            hotel_str = self.hotel_combobox.get()
            tipo_hab_str = self.tipo_hab_combobox.get()
            regimen_str = self.regimen_combobox.get()
            fecha_salida_str = self.fecha_salida_entry.get().strip()
            tipo_str = self.tipo_combobox.get()
            
            if not all([dni, hotel_str, tipo_hab_str, regimen_str, fecha_salida_str]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                return
            
            # Extraer IDs
            id_hotel = int(hotel_str.split(" - ")[0])
            id_tipo_hab = int(tipo_hab_str.split(" - ")[0])
            id_regimen = int(regimen_str.split(" - ")[0])
            
            # Fecha de entrada es HOY (fecha actual)
            fecha_entrada = date.today()
            # Parsear fecha de salida
            fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
            
            tipo_reserva = TipoReserva.AGENCIA if tipo_str == "AGENCIA" else TipoReserva.PARTICULAR
            
            self.reserva_service.actualizar_reserva(
                id_reserva, dni, id_hotel, id_tipo_hab, id_regimen,
                fecha_entrada, fecha_salida, tipo_reserva
            )
            
            messagebox.showinfo("Éxito", "Reserva actualizada correctamente")
            self._limpiar_formulario()
            self._load_reservas()
            
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato inválido: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar reserva: {str(e)}")
    
    def _eliminar_reserva(self):
        """Elimina una reserva"""
        try:
            id_str = self.id_entry.get().strip()
            if not id_str:
                messagebox.showwarning("Advertencia", "Debe seleccionar una reserva")
                return
            
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la reserva #{id_str}?"):
                self.reserva_service.eliminar_reserva(int(id_str))
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
                self._limpiar_formulario()
                self._load_reservas()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar reserva: {str(e)}")
    
    def _checkin(self):
        """Realiza check-in con gestión de huéspedes"""
        try:
            id_str = self.id_entry.get().strip()
            if not id_str:
                messagebox.showwarning("Advertencia", "Debe seleccionar una reserva")
                return
            
            id_reserva = int(id_str)
            
            # Obtener información de la reserva desde el backend
            response = self.reserva_service._repository._api.get(f"reservas/{id_reserva}")
            
            if not response.success:
                messagebox.showerror("Error", f"No se pudo obtener la reserva: {response.error}")
                return
            
            reserva_data = response.data
            
            # Extraer tipo de habitación de las pernoctaciones
            pernoctaciones = reserva_data.get("pernoctaciones", [])
            if not pernoctaciones:
                messagebox.showerror("Error", "La reserva no tiene pernoctaciones asociadas")
                return
            
            tipo_habitacion = pernoctaciones[0].get("tipoHabitacion", {})
            categoria = tipo_habitacion.get("categoria", "Desconocido")
            
            # Calcular capacidad según tipo de habitación
            capacidades = {
                "Individual": 1,
                "Doble": 2,
                "Suite Junior": 4
            }
            capacidad = capacidades.get(categoria, 2)  # Default 2 si no se encuentra
            
            # Pedir número de habitación
            numero_habitacion = simpledialog.askstring(
                "Check-in - Número de Habitación",
                f"Reserva #{id_reserva}\n"
                f"Tipo: {categoria}\n\n"
                f"Ingrese el número de habitación:"
            )
            
            if not numero_habitacion:
                messagebox.showinfo("Cancelado", "Check-in cancelado")
                return
            
            # Abrir diálogo de huéspedes
            dialog = HuespedesDialog(self.parent, capacidad, categoria)
            dialog.wait_window()
            
            # Si el usuario canceló, no continuar
            if dialog.result is None:
                messagebox.showinfo("Cancelado", "Check-in cancelado - no se registraron huéspedes")
                return
            
            huespedes_lista = dialog.result
            
            # Hacer check-in con número de habitación y huéspedes
            checkin_payload = {
                "numeroHabitacion": numero_habitacion,
                "huespedes": huespedes_lista
            }
            
            checkin_response = self.reserva_service._repository._api.post(
                f"reservas/{id_reserva}/checkin",
                checkin_payload
            )
            
            if not checkin_response.success:
                messagebox.showerror(
                    "Error",
                    f"Error al hacer check-in: {checkin_response.error}"
                )
                return
            
            messagebox.showinfo(
                "Éxito",
                f"✅ Check-in realizado correctamente\n"
                f"📍 Habitación: {numero_habitacion}\n"
                f"👥 Huéspedes registrados: {len(huespedes_lista)} + 1 (titular)\n"
                f"🏨 Tipo: {categoria}"
            )
            
            self._limpiar_formulario()
            self._load_reservas()
            
        except ValueError as ve:
            messagebox.showerror("Error", f"ID de reserva inválido: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en check-in: {str(e)}")
    
    def _checkout(self):
        """Realiza check-out"""
        try:
            id_str = self.id_entry.get().strip()
            if not id_str:
                messagebox.showwarning("Advertencia", "Debe seleccionar una reserva")
                return
            
            self.reserva_service.checkout(int(id_str))
            messagebox.showinfo("Éxito", "Check-out realizado correctamente")
            self._load_reservas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en check-out: {str(e)}")
    
    def _limpiar_formulario(self):
        """Limpia el formulario"""
        self.id_entry.configure(state="normal")
        self.id_entry.delete(0, "end")
        self.id_entry.configure(state="readonly")
        self.cliente_entry.delete(0, "end")
        self.fecha_salida_entry.delete(0, "end")
        self.tipo_combobox.set("PARTICULAR")
        self.huespedes_lista = []  # Limpiar lista de huéspedes
        self.precio_total_label.configure(text="0.00 €")  # Resetear precio

