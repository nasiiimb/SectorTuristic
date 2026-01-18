"""
MainWindow - Ventana principal del PMS con menú de opciones
"""
import tkinter
import customtkinter as ctk
from tkinter import messagebox, Toplevel
from datetime import datetime, timedelta, date
from tkcalendar import Calendar


class MainWindow:
    """Ventana principal de la aplicación PMS"""
    
    def __init__(self, root, cliente_service, reserva_service, consulta_service, api_client):
        self.root = root
        self.cliente_service = cliente_service
        self.reserva_service = reserva_service
        self.consulta_service = consulta_service
        self.api_client = api_client
        
        # Hotel seleccionado (se establecerá al inicio)
        self.hotel_seleccionado = None
        self.hoteles_disponibles = []
        
        # Configuración de la ventana
        self.root.title("PMS - Property Management System")
        self.root.geometry("1400x900")  # Tamaño óptimo para visualización
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Mostrar selector de hotel primero
        self._mostrar_selector_hotel()
    
    def _mostrar_selector_hotel(self):
        """Muestra el selector de hotel al inicio"""
        # Limpiar el frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Frame centrado para el selector
        selector_frame = ctk.CTkFrame(self.main_frame)
        selector_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = ctk.CTkLabel(
            selector_frame,
            text="Seleccione el Hotel",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=(20, 30), padx=40)
        
        # Cargar hoteles desde la API
        try:
            self.hoteles_disponibles = self.consulta_service.obtener_hoteles()
            
            if not self.hoteles_disponibles:
                messagebox.showerror("Error", "No se encontraron hoteles disponibles")
                return
            
            # Crear opciones para el dropdown
            opciones_hoteles = [
                f"{h.nombre} - {h.ubicacion}" 
                for h in self.hoteles_disponibles
            ]
            
            # Dropdown de hoteles
            label_hotel = ctk.CTkLabel(
                selector_frame,
                text="Hotel:",
                font=ctk.CTkFont(size=14)
            )
            label_hotel.pack(pady=(10, 5), padx=40)
            
            self.dropdown_hotel = ctk.CTkOptionMenu(
                selector_frame,
                values=opciones_hoteles,
                width=300
            )
            self.dropdown_hotel.pack(pady=(0, 20), padx=40)
            
            # Botón confirmar
            btn_confirmar = ctk.CTkButton(
                selector_frame,
                text="Confirmar",
                command=self._confirmar_hotel,
                width=200,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            btn_confirmar.pack(pady=(10, 20), padx=40)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar hoteles: {str(e)}")
    
    def _confirmar_hotel(self):
        """Confirma la selección del hotel y carga el menú principal"""
        # Obtener el hotel seleccionado
        seleccion = self.dropdown_hotel.get()
        
        # Buscar el hotel en la lista
        for hotel in self.hoteles_disponibles:
            if f"{hotel.nombre} - {hotel.ubicacion}" == seleccion:
                self.hotel_seleccionado = hotel
                break
        
        if not self.hotel_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un hotel")
            return
        
        # Actualizar el título de la ventana
        self.root.title(f"PMS - {self.hotel_seleccionado.nombre}")
        
        # Limpiar el frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Crear el menú y mostrar la interfaz principal
        self._crear_menu()
        
        # Frame de contenido
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar pantalla de bienvenida
        self._mostrar_bienvenida()
    
    def _crear_menu(self):
        """Crea el menú lateral"""
        menu_frame = ctk.CTkFrame(self.main_frame, width=280, corner_radius=0)
        menu_frame.pack(side="left", fill="y", padx=0, pady=0)
        menu_frame.pack_propagate(False)
        
        # Título del menú con icono
        titulo = ctk.CTkLabel(
            menu_frame,
            text="🏨 MENÚ PMS",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        titulo.pack(pady=(35, 60))
        
        # Botones del menú
        btn_buscar_reservas = ctk.CTkButton(
            menu_frame,
            text="🔍 Buscar Reservas",
            command=self._mostrar_buscar_reservas,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            corner_radius=10,
            anchor="w",
            image=None
        )
        btn_buscar_reservas.pack(fill="x", padx=25, pady=12)
        
        btn_buscar_contratos = ctk.CTkButton(
            menu_frame,
            text="📋 Buscar Contratos",
            command=self._mostrar_buscar_contratos,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            corner_radius=10,
            anchor="w"
        )
        btn_buscar_contratos.pack(fill="x", padx=25, pady=12)
        
        btn_crear_reserva = ctk.CTkButton(
            menu_frame,
            text="➕ Crear Reserva",
            command=self._mostrar_crear_reserva,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            corner_radius=10,
            anchor="w"
        )
        btn_crear_reserva.pack(fill="x", padx=25, pady=12)
        
        # Separador
        separador = ctk.CTkFrame(menu_frame, height=2, fg_color=("#3D9970", "#2A7A5E"))
        separador.pack(fill="x", padx=30, pady=40)
        
        # Botón cambiar hotel
        btn_cambiar_hotel = ctk.CTkButton(
            menu_frame,
            text="🏨 Cambiar Hotel",
            command=self._cambiar_hotel,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#F39C12", "#D68910"),
            hover_color=("#F4A624", "#E5A01F"),
            corner_radius=10,
            anchor="w"
        )
        btn_cambiar_hotel.pack(fill="x", padx=25, pady=12)
        
        # Botón de salir
        btn_salir = ctk.CTkButton(
            menu_frame,
            text="🚪 Salir",
            command=self.root.quit,
            height=55,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#A93226", "#7B1F1F"),
            hover_color=("#C0392B", "#922B21"),
            corner_radius=10,
            anchor="w"
        )
        btn_salir.pack(side="bottom", fill="x", padx=25, pady=25)
    
    def _limpiar_contenido(self):
        """Limpia el frame de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _cambiar_hotel(self):
        """Permite cambiar de hotel"""
        # Mostrar diálogo de confirmación
        respuesta = messagebox.askyesno(
            "Cambiar Hotel",
            f"¿Está seguro que desea cambiar de hotel?\n\n"
            f"Hotel actual: {self.hotel_seleccionado.nombre if self.hotel_seleccionado else 'Ninguno'}\n\n"
            f"Se perderá cualquier información no guardada."
        )
        
        if respuesta:
            # Reiniciar la selección de hotel
            self._mostrar_selector_hotel()
    
    def _mostrar_bienvenida(self):
        """Muestra la pantalla de bienvenida"""
        self._limpiar_contenido()
        
        # Mensaje principal
        mensaje_principal = f"🏨 Bienvenido al PMS\n\n"
        if self.hotel_seleccionado:
            mensaje_principal += f"Hotel: {self.hotel_seleccionado.nombre}\n"
            mensaje_principal += f"Ubicación: {self.hotel_seleccionado.ubicacion}\n\n"
        mensaje_principal += "Seleccione una opción del menú"
        
        bienvenida = ctk.CTkLabel(
            self.content_frame,
            text=mensaje_principal,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        bienvenida.pack(expand=True)
    
    def _mostrar_buscar_reservas(self):
        """Muestra el panel de búsqueda de reservas"""
        self._limpiar_contenido()
        
        # Título con estilo mejorado
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="🔍 Buscar Reservas",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        titulo.pack(pady=(10, 30))
        
        # Formulario de búsqueda con mejor estilo
        search_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        search_frame.pack(fill="x", pady=20, padx=20)
        
        # Campo Nombre
        label_nombre = ctk.CTkLabel(search_frame, text="Nombre Cliente:", font=ctk.CTkFont(size=15, weight="bold"))
        label_nombre.pack(side="left", padx=15, pady=15)
        
        self.entry_nombre_cliente = ctk.CTkEntry(
            search_frame, 
            width=220, 
            height=40,
            placeholder_text="Ej: Juan",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.entry_nombre_cliente.pack(side="left", padx=10, pady=15)
        
        # Campo Apellido
        label_apellido = ctk.CTkLabel(search_frame, text="Apellido:", font=ctk.CTkFont(size=15, weight="bold"))
        label_apellido.pack(side="left", padx=15, pady=15)
        
        self.entry_apellido_cliente = ctk.CTkEntry(
            search_frame, 
            width=220, 
            height=40,
            placeholder_text="Ej: García",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.entry_apellido_cliente.pack(side="left", padx=10, pady=15)
        
        # Botón Buscar
        btn_buscar = ctk.CTkButton(
            search_frame,
            text="🔍 Buscar",
            command=self._buscar_reservas_por_cliente,
            width=140,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            corner_radius=10
        )
        btn_buscar.pack(side="left", padx=15, pady=15)
        
        # Botón Listar Todas
        btn_listar_todas = ctk.CTkButton(
            search_frame,
            text="📋 Listar Todas",
            command=self._listar_todas_reservas,
            width=140,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#1F618D", "#154360"),
            hover_color=("#2874A6", "#1A5276"),
            corner_radius=10
        )
        btn_listar_todas.pack(side="left", padx=10, pady=15)
        
        # Frame para resultados
        self.reservas_result_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.reservas_result_frame.pack(fill="both", expand=True, pady=20)
    
    def _buscar_reservas_por_cliente(self):
        """Busca reservas por nombre y/o apellido del cliente"""
        try:
            nombre = self.entry_nombre_cliente.get().strip()
            apellido = self.entry_apellido_cliente.get().strip()
            
            if not nombre and not apellido:
                messagebox.showwarning("Advertencia", "Debe ingresar al menos un nombre o apellido")
                return
            
            # Construir query params
            params = []
            if nombre:
                params.append(f"nombre={nombre}")
            if apellido:
                params.append(f"apellido={apellido}")
            # FILTRAR POR HOTEL SELECCIONADO
            if self.hotel_seleccionado:
                params.append(f"hotel={self.hotel_seleccionado.id_hotel}")
            
            query_string = "&".join(params)
            
            print(f"[BUSCAR] Buscando reservas ACTIVAS en hotel {self.hotel_seleccionado.nombre}: {query_string}")
            
            # Llamar al endpoint de búsqueda de reservas ACTIVAS
            response = self.api_client.get(f"reservas/buscar/cliente/activas?{query_string}")
            
            if not response.success:
                messagebox.showinfo("Info", "No se encontraron reservas con esos criterios")
                return
            
            # Extraer reservas de la respuesta
            reservas_data = response.data.get('reservas', [])
            
            if not reservas_data:
                messagebox.showinfo("Info", f"No se encontraron reservas para: {nombre} {apellido}")
                # Limpiar resultados
                for widget in self.reservas_result_frame.winfo_children():
                    widget.destroy()
                label = ctk.CTkLabel(
                    self.reservas_result_frame,
                    text=f"No se encontraron reservas para: {nombre} {apellido}",
                    font=ctk.CTkFont(size=14)
                )
                label.pack(pady=20)
                return
            
            print(f"[INFO] Se encontraron {len(reservas_data)} reservas")
            
            # Convertir a objetos Reserva y mostrar
            from src.domain.reserva import Reserva
            reservas = []
            for data in reservas_data:
                # Usar el método from_dict de la clase Reserva
                reserva = Reserva.from_dict(data)
                # Agregar datos adicionales para el display
                reserva._contrato_data = data.get('contrato')
                reserva._cliente_data = data.get('clientePaga')
                reserva._precio_regimen_data = data.get('precioRegimen')
                reservas.append(reserva)
            
            self._mostrar_lista_reservas(reservas)
            
        except Exception as e:
            print(f"[ERROR] Error al buscar reservas: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al buscar reservas: {str(e)}")
    
    def _listar_todas_reservas(self):
        """Lista todas las reservas ACTIVAS del hotel seleccionado"""
        try:
            # FILTRAR POR HOTEL SELECCIONADO
            query = ""
            if self.hotel_seleccionado:
                query = f"?hotel={self.hotel_seleccionado.id_hotel}"
            
            # Obtener datos completos de la API - Solo ACTIVAS
            response = self.api_client.get(f"reservas/activas{query}")
            if not response.success:
                raise Exception(response.error)
            
            reservas_data = response.data
            
            print(f"[INFO] Listando reservas ACTIVAS del hotel: {self.hotel_seleccionado.nombre}")
            print(f"[INFO] Se encontraron {len(reservas_data)} reservas activas")
            
            # Convertir a objetos Reserva
            from src.domain.reserva import Reserva
            reservas = []
            for data in reservas_data:
                reserva = Reserva.from_dict(data)
                # Agregar datos adicionales para el display
                reserva._contrato_data = data.get('contrato')
                reserva._cliente_data = data.get('clientePaga')
                reserva._precio_regimen_data = data.get('precioRegimen')
                reservas.append(reserva)
            
            self._mostrar_lista_reservas(reservas)
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar reservas: {str(e)}")
    
    def _mostrar_lista_reservas(self, reservas):
        """Muestra una lista de reservas"""
        # Limpiar resultados
        for widget in self.reservas_result_frame.winfo_children():
            widget.destroy()
        
        if not reservas:
            label = ctk.CTkLabel(
                self.reservas_result_frame,
                text="No se encontraron reservas",
                font=ctk.CTkFont(size=14)
            )
            label.pack(pady=20)
            return
        
        # Headers con anchos proporcionados
        header_frame = ctk.CTkFrame(self.reservas_result_frame, fg_color=("#2B7A78", "#14443F"), corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        # Configurar grid para que se expanda
        header_frame.grid_columnconfigure(0, weight=2)  # Cliente
        header_frame.grid_columnconfigure(1, weight=2)  # Hotel
        header_frame.grid_columnconfigure(2, weight=1)  # Entrada
        header_frame.grid_columnconfigure(3, weight=1)  # Salida
        header_frame.grid_columnconfigure(4, weight=1)  # Tipo
        header_frame.grid_columnconfigure(5, weight=1)  # Acción
        
        headers = ["Cliente", "Hotel", "Entrada", "Salida", "Tipo", "Acción"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="center"
            )
            label.grid(row=0, column=col, padx=8, pady=15, sticky="ew")
        
        # Datos con filas alternadas
        for idx, reserva in enumerate(reservas):
            # Color alternado para mejor legibilidad
            bg_color = ("#2B2B2B", "#1E1E1E") if idx % 2 == 0 else ("#252525", "#252525")
            
            row_frame = ctk.CTkFrame(self.reservas_result_frame, fg_color=bg_color, corner_radius=5)
            row_frame.pack(fill="x", pady=3, padx=10)
            
            # Configurar grid igual que header
            row_frame.grid_columnconfigure(0, weight=2)
            row_frame.grid_columnconfigure(1, weight=2)
            row_frame.grid_columnconfigure(2, weight=1)
            row_frame.grid_columnconfigure(3, weight=1)
            row_frame.grid_columnconfigure(4, weight=1)
            row_frame.grid_columnconfigure(5, weight=1)
            
            # Cliente (nombre completo)
            cliente_text = "N/A"
            if hasattr(reserva, '_cliente_data') and reserva._cliente_data:
                cliente_text = f"{reserva._cliente_data.get('nombre', '')} {reserva._cliente_data.get('apellidos', '')}"
            elif reserva.cliente_paga:
                cliente_text = f"{reserva.cliente_paga.nombre} {reserva.cliente_paga.apellidos}"
            elif reserva.id_cliente:
                cliente_text = f"ID: {reserva.id_cliente}"
            
            ctk.CTkLabel(
                row_frame,
                text=cliente_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            ).grid(row=0, column=0, padx=12, pady=12, sticky="ew")
            
            # Hotel (nombre)
            hotel_text = "N/A"
            if hasattr(reserva, '_precio_regimen_data') and reserva._precio_regimen_data:
                hotel_data = reserva._precio_regimen_data.get('hotel', {})
                hotel_text = hotel_data.get('nombre', 'N/A')
            elif reserva.precio_regimen and reserva.precio_regimen.hotel:
                hotel_text = reserva.precio_regimen.hotel.nombre
            elif reserva.id_hotel:
                hotel_text = f"ID: {reserva.id_hotel}"
            
            ctk.CTkLabel(
                row_frame,
                text=hotel_text,
                font=ctk.CTkFont(size=13),
                anchor="w"
            ).grid(row=0, column=1, padx=12, pady=12, sticky="ew")
            
            # Fechas
            ctk.CTkLabel(
                row_frame,
                text=str(reserva.fecha_entrada),
                font=ctk.CTkFont(size=13),
                anchor="center"
            ).grid(row=0, column=2, padx=8, pady=12, sticky="ew")
            
            ctk.CTkLabel(
                row_frame,
                text=str(reserva.fecha_salida),
                font=ctk.CTkFont(size=13),
                anchor="center"
            ).grid(row=0, column=3, padx=8, pady=12, sticky="ew")
            
            # Tipo de reserva
            tipo_text = reserva.tipo.value if hasattr(reserva.tipo, 'value') else str(reserva.tipo)
            ctk.CTkLabel(
                row_frame,
                text=tipo_text,
                font=ctk.CTkFont(size=13),
                anchor="center"
            ).grid(row=0, column=4, padx=8, pady=12, sticky="ew")
            
            # Botón
            btn_ver = ctk.CTkButton(
                row_frame,
                text="👁️ Ver",
                command=lambda r=reserva: self._mostrar_detalle_reserva(r),
                fg_color=("#1F618D", "#154360"),
                hover_color=("#2E86C1", "#1A5490"),
                font=ctk.CTkFont(size=13, weight="bold"),
                height=38
            )
            btn_ver.grid(row=0, column=5, padx=10, pady=10, sticky="ew")
    
    def _mostrar_detalle_reserva(self, reserva):
        """Muestra el detalle de una reserva con opción de check-in"""
        # Limpiar resultados
        for widget in self.reservas_result_frame.winfo_children():
            widget.destroy()
        
        # Obtener datos completos de la reserva desde la API
        try:
            response = self.api_client.get(f"reservas/{reserva.id_reserva}")
            if response.success:
                from src.domain.reserva import Reserva
                reserva = Reserva.from_dict(response.data)
                reserva._contrato_data = response.data.get('contrato')
                reserva._cliente_data = response.data.get('clientePaga')
                reserva._precio_regimen_data = response.data.get('precioRegimen')
                reserva._raw_data = response.data  # Guardar datos completos incluyendo pernoctaciones
        except Exception as e:
            print(f"[WARNING] No se pudieron obtener datos completos de la reserva: {e}")
            import traceback
            traceback.print_exc()
        
        # Frame de detalle con estilo mejorado
        detalle_frame = ctk.CTkFrame(self.reservas_result_frame, corner_radius=15)
        detalle_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título con mejor estilo
        titulo = ctk.CTkLabel(
            detalle_frame,
            text=f"📄 Detalle de Reserva #{reserva.id_reserva}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        titulo.pack(pady=25)
        
        # Información de la reserva con mejor estilo
        info_frame = ctk.CTkFrame(detalle_frame, corner_radius=12)
        info_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Cliente
        cliente_nombre = "N/A"
        if reserva.cliente_paga:
            cliente_nombre = f"{reserva.cliente_paga.nombre} {reserva.cliente_paga.apellidos}"
        elif reserva.id_cliente:
            cliente_nombre = f"ID: {reserva.id_cliente}"
        
        # Hotel
        hotel_nombre = "N/A"
        if reserva.precio_regimen and reserva.precio_regimen.hotel:
            hotel_nombre = reserva.precio_regimen.hotel.nombre
        elif reserva.id_hotel:
            hotel_nombre = f"ID: {reserva.id_hotel}"
        
        # Régimen
        regimen_info = "N/A"
        if reserva.precio_regimen and reserva.precio_regimen.regimen:
            regimen_info = f"{reserva.precio_regimen.regimen.codigo} - {reserva.precio_regimen.precio}€"
        elif reserva.id_regimen:
            regimen_info = f"ID: {reserva.id_regimen}"
        
        # Tipo de Habitación
        tipo_habitacion_info = "N/A"
        
        # 1. Intentar obtener desde pernoctaciones directas de la reserva (_raw_data)
        if hasattr(reserva, '_raw_data') and reserva._raw_data:
            pernoctaciones = reserva._raw_data.get('pernoctaciones', [])
            if pernoctaciones and len(pernoctaciones) > 0:
                tipo_hab = pernoctaciones[0].get('tipoHabitacion', {})
                if tipo_hab:
                    tipo_habitacion_info = tipo_hab.get('categoria', 'N/A')
                    camas_ind = tipo_hab.get('camasIndividuales', 0)
                    camas_dobles = tipo_hab.get('camasDobles', 0)
                    if camas_ind or camas_dobles:
                        tipo_habitacion_info += f" ({camas_ind} ind, {camas_dobles} dob)"
        
        # 2. Si no hay pernoctaciones, intentar desde contrato (si tiene check-in)
        if tipo_habitacion_info == "N/A" and hasattr(reserva, '_contrato_data') and reserva._contrato_data:
            pernoctaciones_contrato = reserva._contrato_data.get('pernoctaciones', [])
            if pernoctaciones_contrato and len(pernoctaciones_contrato) > 0:
                tipo_hab = pernoctaciones_contrato[0].get('tipoHabitacion', {})
                if tipo_hab:
                    tipo_habitacion_info = tipo_hab.get('categoria', 'N/A')
                    camas_ind = tipo_hab.get('camasIndividuales', 0)
                    camas_dobles = tipo_hab.get('camasDobles', 0)
                    if camas_ind or camas_dobles:
                        tipo_habitacion_info += f" ({camas_ind} ind, {camas_dobles} dob)"
        
        # Tipo
        tipo_reserva = reserva.tipo.value if hasattr(reserva.tipo, 'value') else str(reserva.tipo)
        
        info = [
            ("ID Reserva:", reserva.id_reserva),
            ("Cliente:", cliente_nombre),
            ("Hotel:", hotel_nombre),
            ("Tipo Habitación:", tipo_habitacion_info),
            ("Fecha Entrada:", reserva.fecha_entrada),
            ("Fecha Salida:", reserva.fecha_salida),
            ("Noches:", reserva.numero_noches),
            ("Régimen:", regimen_info),
            ("Tipo:", tipo_reserva),
            ("Canal:", reserva.canal_reserva or "N/A"),
        ]
        
        # Verificar si ya tiene contrato (check-in realizado)
        # Prioridad: _contrato_data (API) > tiene_contrato (atributo) > contrato (objeto)
        tiene_contrato = False
        contrato_habitacion = None
        
        # 1. Verificar _contrato_data (datos frescos de la API)
        if hasattr(reserva, '_contrato_data') and reserva._contrato_data:
            tiene_contrato = True
            contrato_habitacion = reserva._contrato_data.get('numeroHabitacion')
        # 2. Verificar atributo tiene_contrato
        elif hasattr(reserva, 'tiene_contrato') and reserva.tiene_contrato:
            tiene_contrato = True
        # 3. Verificar objeto contrato
        elif hasattr(reserva, 'contrato') and reserva.contrato is not None:
            tiene_contrato = True
            if hasattr(reserva.contrato, 'numero_habitacion'):
                contrato_habitacion = reserva.contrato.numero_habitacion
        
        if tiene_contrato:
            contrato_info = "✅ SÍ - Check-in completado"
            if contrato_habitacion:
                contrato_info += f" (Hab. {contrato_habitacion})"
            info.append(("Check-in:", contrato_info))
        else:
            info.append(("Check-in:", "❌ Pendiente"))
        
        for idx, (campo, valor) in enumerate(info):
            # Alternar colores de fondo
            bg_color = ("#2B2B2B", "#1E1E1E") if idx % 2 == 0 else "transparent"
            frame = ctk.CTkFrame(info_frame, fg_color=bg_color, corner_radius=8)
            frame.pack(fill="x", pady=6, padx=15)
            
            ctk.CTkLabel(
                frame,
                text=campo,
                font=ctk.CTkFont(size=15, weight="bold"),
                width=220,
                anchor="w"
            ).pack(side="left", padx=15, pady=12)
            
            # Color especial para el estado del check-in
            text_color = None
            if campo == "Check-in:":
                # Verde si tiene check-in, rojo si está pendiente
                text_color = ("#27AE60", "#2ECC71") if tiene_contrato else ("#E74C3C", "#EC7063")
            
            label_valor = ctk.CTkLabel(
                frame,
                text=str(valor),
                font=ctk.CTkFont(size=15),
                anchor="w"
            )
            if text_color:
                label_valor.configure(text_color=text_color)
            label_valor.pack(side="left", padx=10, pady=12)
        
        # Botones de acción (Check-in o Cancelar)
        acciones_frame = ctk.CTkFrame(detalle_frame, fg_color="transparent")
        acciones_frame.pack(pady=35)
        
        if tiene_contrato:
            # Mostrar mensaje de que ya se hizo check-in
            mensaje_info = ctk.CTkLabel(
                acciones_frame,
                text="⚠️ Esta reserva ya tiene check-in realizado",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#E67E22", "#F39C12")
            )
            mensaje_info.pack(pady=20)
        else:
            # Frame para check-in con mejor estilo
            checkin_frame = ctk.CTkFrame(acciones_frame, fg_color="transparent")
            checkin_frame.pack(pady=12)
            
            # Obtener habitaciones disponibles del hotel
            habitaciones_disponibles = self._obtener_habitaciones_disponibles(reserva)
            
            # Mostrar formulario de check-in
            label_hab = ctk.CTkLabel(checkin_frame, text="Seleccionar Habitación:", font=ctk.CTkFont(size=15, weight="bold"))
            label_hab.pack(side="left", padx=12)
        
            if habitaciones_disponibles:
                # Crear opciones del dropdown con formato "Número - Tipo"
                opciones_habitaciones = {}
                for hab in habitaciones_disponibles:
                    numero = hab.get('numeroHabitacion', 'N/A')
                    tipo = hab.get('tipoHabitacion', {}).get('categoria', 'N/A')
                    texto = f"{numero} - {tipo}"
                    opciones_habitaciones[texto] = numero
                
                dropdown_hab = ctk.CTkOptionMenu(
                    checkin_frame,
                    values=list(opciones_habitaciones.keys()),
                    font=ctk.CTkFont(size=14),
                    width=250,
                    height=45
                )
                dropdown_hab.pack(side="left", padx=12)
                dropdown_hab.set(list(opciones_habitaciones.keys())[0])
                
                btn_checkin = ctk.CTkButton(
                    checkin_frame,
                    text="✓ Hacer Check-in",
                    command=lambda: self._mostrar_checkin_con_huespedes_inline(reserva, opciones_habitaciones[dropdown_hab.get()]),
                    font=ctk.CTkFont(size=15, weight="bold"),
                    fg_color=("#2B7A78", "#14443F"),
                    hover_color=("#3D9970", "#2A7A5E"),
                    width=220,
                    height=45,
                    corner_radius=10
                )
                btn_checkin.pack(side="left", padx=12)
            else:
                # No hay habitaciones disponibles
                label_no_hab = ctk.CTkLabel(
                    checkin_frame,
                    text="❌ No hay habitaciones disponibles",
                    font=ctk.CTkFont(size=14),
                    text_color=("#E74C3C", "#C0392B")
                )
                label_no_hab.pack(side="left", padx=12)
            
            # Frame para cancelar (separado visualmente)
            separador = ctk.CTkLabel(acciones_frame, text="— o —", font=ctk.CTkFont(size=14, weight="bold"))
            separador.pack(pady=12)
            
            cancelar_frame = ctk.CTkFrame(acciones_frame, fg_color="transparent")
            cancelar_frame.pack(pady=12)
            
            btn_cancelar = ctk.CTkButton(
                cancelar_frame,
                text="✖ Cancelar Reserva",
                command=lambda: self._cancelar_reserva(reserva),
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=("#E74C3C", "#C0392B"),
                hover_color=("#EC7063", "#CB4335"),
                width=220,
                height=45,
                corner_radius=10
            )
            btn_cancelar.pack(padx=12)
    
    def _mostrar_checkin_con_huespedes_inline(self, reserva, numero_hab):
        """Muestra el panel inline para gestionar huéspedes y hacer check-in"""
        try:
            if not numero_hab:
                messagebox.showwarning("Advertencia", "Debe ingresar el número de habitación")
                return
            
            # Obtener la reserva completa desde la API para asegurar tener todas las relaciones
            response = self.api_client.get(f"reservas/{reserva.id_reserva}")
            
            if not response.success:
                messagebox.showerror("Error", f"No se pudo obtener la reserva: {response.error}")
                return
            
            reserva_data = response.data
            
            # Verificar si ya tiene contrato
            if reserva_data.get("contrato"):
                messagebox.showwarning(
                    "Check-in ya realizado",
                    f"⚠️ Esta reserva ya tiene check-in realizado\n"
                    f"Habitación: {reserva_data['contrato'].get('numeroHabitacion', 'N/A')}\n"
                    f"No se puede hacer check-in nuevamente."
                )
                return
            
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
            
            # Limpiar contenido y mostrar panel inline
            self._limpiar_contenido()
            
            # Guardar datos en el objeto para usarlos en otros métodos
            self.checkin_data = {
                'reserva': reserva,
                'numero_hab': numero_hab,
                'capacidad': capacidad,
                'categoria': categoria,
                'huespedes': []
            }
            
            # ============= CONTENIDO =============
            content_scroll = ctk.CTkScrollableFrame(self.content_frame)
            content_scroll.pack(side="top", fill="both", expand=True, padx=20, pady=(20, 0))
            
            # Título
            title = ctk.CTkLabel(
                content_scroll,
                text=f"👥 Gestionar Huéspedes - Check-in",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title.pack(pady=(0, 10))
            
            # Información de capacidad
            info_frame = ctk.CTkFrame(content_scroll, corner_radius=10)
            info_frame.pack(fill="x", pady=(0, 15))
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=f"📍 Habitación: {categoria} (Número: {numero_hab})\n"
                     f"👤 Capacidad máxima: {capacidad} persona(s)\n"
                     f"ℹ️  El cliente que paga cuenta como 1 huésped",
                font=ctk.CTkFont(size=13),
                justify="left"
            )
            info_label.pack(padx=15, pady=15)
            
            # Frame del formulario
            form_frame = ctk.CTkFrame(content_scroll, corner_radius=10)
            form_frame.pack(fill="x", pady=(0, 15))
            
            # Nombre
            nombre_label = ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=13))
            nombre_label.pack(anchor="w", padx=20, pady=(10, 0))
            
            self.checkin_nombre_entry = ctk.CTkEntry(
                form_frame,
                placeholder_text="Nombre del huésped",
                height=32,
                font=ctk.CTkFont(size=12)
            )
            self.checkin_nombre_entry.pack(fill="x", padx=20, pady=(0, 8))
            
            # Apellidos
            apellidos_label = ctk.CTkLabel(form_frame, text="Apellidos:", font=ctk.CTkFont(size=13))
            apellidos_label.pack(anchor="w", padx=20, pady=(3, 0))
            
            self.checkin_apellidos_entry = ctk.CTkEntry(
                form_frame,
                placeholder_text="Apellidos del huésped",
                height=32,
                font=ctk.CTkFont(size=12)
            )
            self.checkin_apellidos_entry.pack(fill="x", padx=20, pady=(0, 8))
            
            # Email
            email_label = ctk.CTkLabel(form_frame, text="Correo Electrónico:", font=ctk.CTkFont(size=13))
            email_label.pack(anchor="w", padx=20, pady=(3, 0))
            
            self.checkin_email_entry = ctk.CTkEntry(
                form_frame,
                placeholder_text="email@ejemplo.com",
                height=32,
                font=ctk.CTkFont(size=12)
            )
            self.checkin_email_entry.pack(fill="x", padx=20, pady=(0, 8))
            
            # DNI
            dni_label = ctk.CTkLabel(form_frame, text="DNI:", font=ctk.CTkFont(size=13))
            dni_label.pack(anchor="w", padx=20, pady=(3, 0))
            
            self.checkin_dni_entry = ctk.CTkEntry(
                form_frame,
                placeholder_text="12345678A",
                height=32,
                font=ctk.CTkFont(size=12)
            )
            self.checkin_dni_entry.pack(fill="x", padx=20, pady=(0, 8))
            
            # Botón añadir
            btn_añadir = ctk.CTkButton(
                form_frame,
                text="➕ Añadir Huésped",
                command=self._anadir_huesped_checkin,
                height=40,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=("#2B7A78", "#14443F"),
                hover_color=("#3D9970", "#2A7A5E")
            )
            btn_añadir.pack(fill="x", padx=20, pady=(5, 15))
            
            # Lista de huéspedes
            lista_frame = ctk.CTkFrame(content_scroll, corner_radius=10)
            lista_frame.pack(fill="x", pady=(0, 15))
            
            lista_title = ctk.CTkLabel(
                lista_frame,
                text="📋 Huéspedes Añadidos (0) - Total: 1/{}".format(capacidad),
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lista_title.pack(pady=(10, 5))
            self.checkin_lista_title_label = lista_title
            
            # Scrollable frame para la lista
            self.checkin_lista_scroll = ctk.CTkScrollableFrame(lista_frame, height=150)
            self.checkin_lista_scroll.pack(fill="x", padx=10, pady=(0, 10))
            
            # Mostrar cliente que paga (info inicial)
            self._actualizar_lista_huespedes_checkin()
            
            # ============= BOTONES AL FINAL =============
            button_container = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=80)
            button_container.pack(side="bottom", fill="x", padx=20, pady=20)
            
            btn_volver = ctk.CTkButton(
                button_container,
                text="⬅️ Volver",
                command=lambda: self._mostrar_detalle_reserva(reserva),
                height=50,
                width=200,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=("#95A5A6", "#7F8C8D"),
                hover_color=("#7F8C8D", "#707B7C")
            )
            btn_volver.pack(side="left", padx=20, expand=True)
            
            btn_confirmar = ctk.CTkButton(
                button_container,
                text="✅ CONFIRMAR CHECK-IN",
                command=self._realizar_checkin_final,
                height=50,
                width=300,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=("#148F77", "#0E6655"),
                hover_color=("#16A085", "#117A65")
            )
            btn_confirmar.pack(side="right", padx=20, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar check-in: {str(e)}")
    
    def _obtener_habitaciones_disponibles(self, reserva):
        """Obtiene las habitaciones disponibles del hotel para el tipo de la reserva"""
        try:
            # Obtener el tipo de habitación de la reserva
            response = self.api_client.get(f"reservas/{reserva.id_reserva}")
            if not response.success:
                return []
            
            reserva_data = response.data
            pernoctaciones = reserva_data.get("pernoctaciones", [])
            if not pernoctaciones:
                return []
            
            tipo_habitacion = pernoctaciones[0].get("tipoHabitacion", {})
            categoria = tipo_habitacion.get("categoria", "")
            
            # Obtener habitaciones disponibles del hotel usando el WebService
            if not self.hotel_seleccionado:
                return []
            
            # Llamar al endpoint de habitaciones disponibles
            hab_response = self.api_client.get(
                f"habitaciones/disponibles/list?hotel={self.hotel_seleccionado.id_hotel}&tipoHabitacion={categoria}"
            )
            
            if not hab_response.success:
                print(f"❌ Error al obtener habitaciones disponibles: {hab_response.error}")
                return []
            
            habitaciones_disponibles = hab_response.data.get('habitaciones', [])
            
            return habitaciones_disponibles
            
        except Exception as e:
            print(f"Error al obtener habitaciones disponibles: {e}")
            return []
    
    def _cancelar_reserva(self, reserva):
        """Cancela una reserva sin check-in"""
        try:
            # Confirmar cancelación
            respuesta = messagebox.askyesno(
                "Confirmar Cancelación",
                f"¿Está seguro que desea cancelar la reserva?\n\n"
                f"Reserva #{reserva.id_reserva}\n"
                f"Cliente: {reserva.cliente_paga.nombre_completo if reserva.cliente_paga else 'N/A'}\n"
                f"Fechas: {reserva.fecha_entrada} a {reserva.fecha_salida}\n\n"
                f"Esta acción NO PUEDE deshacerse."
            )
            
            if not respuesta:
                return
            
            # Llamar a la API para cancelar
            response = self.api_client.patch(f"reservas/{reserva.id_reserva}/cancelar")
            
            if not response.success:
                error_msg = response.data.get('message', response.error) if response.data else response.error
                messagebox.showerror("Error", f"Error al cancelar reserva: {error_msg}")
                return
            
            messagebox.showinfo(
                "Éxito",
                f"✓ Reserva #{reserva.id_reserva} cancelada exitosamente\n\n"
                f"La reserva se ha marcado como cancelada y ya no aparecerá en las búsquedas activas."
            )
            
            # Volver a la búsqueda de reservas
            self._mostrar_buscar_reservas()
            
        except Exception as e:
            print(f"❌ Error al cancelar reserva: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error inesperado al cancelar: {str(e)}")
    
    def _hacer_checkin(self, id_reserva, numero_hab, monto):
        """Realiza el check-in de una reserva (método antiguo - mantener por compatibilidad)"""
        try:
            if not numero_hab or not monto:
                messagebox.showwarning("Advertencia", "Debe ingresar número de habitación y monto total")
                return
            
            numero_hab = int(numero_hab)
            monto = float(monto)
            
            contrato = self.reserva_service.hacer_checkin(id_reserva, numero_hab, monto)
            messagebox.showinfo("Éxito", f"Check-in realizado. Contrato ID: {contrato.id_contrato}")
            self._mostrar_buscar_reservas()
        except ValueError:
            messagebox.showerror("Error", "Número de habitación debe ser entero y monto un decimal")
        except Exception as e:
            messagebox.showerror("Error", f"Error al hacer check-in: {str(e)}")
    
    def _mostrar_buscar_contratos(self):
        """Muestra el panel de búsqueda de contratos"""
        self._limpiar_contenido()
        
        # Título con estilo mejorado
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="📋 Buscar Contratos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        titulo.pack(pady=(10, 30))
        
        # Buscar por Nombre/Apellido
        search_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        search_frame.pack(fill="x", pady=20, padx=20)
        
        label_nombre = ctk.CTkLabel(search_frame, text="Nombre Cliente:", font=ctk.CTkFont(size=15, weight="bold"))
        label_nombre.pack(side="left", padx=15, pady=15)
        
        self.entry_nombre_cliente_contrato = ctk.CTkEntry(
            search_frame, 
            width=220, 
            height=40,
            placeholder_text="Ej: Juan",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.entry_nombre_cliente_contrato.pack(side="left", padx=10, pady=15)
        
        label_apellido = ctk.CTkLabel(search_frame, text="Apellido:", font=ctk.CTkFont(size=15, weight="bold"))
        label_apellido.pack(side="left", padx=15, pady=15)
        
        self.entry_apellido_cliente_contrato = ctk.CTkEntry(
            search_frame, 
            width=220, 
            height=40,
            placeholder_text="Ej: García",
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        self.entry_apellido_cliente_contrato.pack(side="left", padx=10, pady=15)
        
        btn_buscar = ctk.CTkButton(
            search_frame,
            text="🔍 Buscar",
            command=self._buscar_contratos_por_cliente,
            width=140,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            corner_radius=10
        )
        btn_buscar.pack(side="left", padx=15, pady=15)
        
        btn_listar_todos = ctk.CTkButton(
            search_frame,
            text="📋 Listar Todos",
            command=self._listar_todos_contratos,
            width=140,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#1F618D", "#154360"),
            hover_color=("#2874A6", "#1A5276"),
            corner_radius=10
        )
        btn_listar_todos.pack(side="left", padx=10, pady=15)
        
        # Frame para resultados
        self.contratos_result_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.contratos_result_frame.pack(fill="both", expand=True, pady=20)
    
    def _buscar_contratos_por_cliente(self):
        """Busca contratos por nombre o apellido del cliente"""
        try:
            nombre = self.entry_nombre_cliente_contrato.get().strip()
            apellido = self.entry_apellido_cliente_contrato.get().strip()
            
            # Validar que al menos un campo tenga valor
            if not nombre and not apellido:
                messagebox.showwarning("Advertencia", "Debe ingresar al menos el nombre o apellido del cliente")
                return
            
            # Construir query string
            query_params = []
            if nombre:
                query_params.append(f"nombre={nombre}")
            if apellido:
                query_params.append(f"apellido={apellido}")
            # FILTRAR POR HOTEL SELECCIONADO
            if self.hotel_seleccionado:
                query_params.append(f"hotel={self.hotel_seleccionado.id_hotel}")
            
            query_string = "&".join(query_params)
            
            print(f"🔍 Buscando contratos en hotel {self.hotel_seleccionado.nombre}: {query_string}")
            
            # Llamar a la API
            response = self.api_client.get(f"contratos/buscar/cliente?{query_string}")
            
            if not response.success:
                messagebox.showerror("Error", f"Error al buscar contratos: {response.error}")
                return
            
            contratos_data = response.data.get('contratos', [])
            
            if not contratos_data:
                # Mostrar mensaje de no encontrado
                for widget in self.contratos_result_frame.winfo_children():
                    widget.destroy()
                label = ctk.CTkLabel(
                    self.contratos_result_frame,
                    text=f"No se encontraron contratos para: {nombre} {apellido}".strip(),
                    font=ctk.CTkFont(size=14)
                )
                label.pack(pady=20)
                return
            
            print(f"✅ Se encontraron {len(contratos_data)} contratos")
            
            # Convertir a objetos Contrato
            from src.domain.contrato import Contrato
            contratos = []
            for data in contratos_data:
                contrato = Contrato.from_dict(data)
                # Agregar datos adicionales para el display
                contrato._reserva_data = data.get('reserva')
                contrato._habitacion_data = data.get('habitacion')
                contratos.append(contrato)
            
            self._mostrar_lista_contratos(contratos)
            
        except Exception as e:
            print(f"❌ Error al buscar contratos: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al buscar contratos: {str(e)}")
    
    def _listar_todos_contratos(self):
        """Lista todos los contratos del hotel seleccionado"""
        try:
            # FILTRAR POR HOTEL SELECCIONADO
            query = ""
            if self.hotel_seleccionado:
                query = f"?hotel={self.hotel_seleccionado.id_hotel}"
            
            # Obtener datos completos de la API
            response = self.api_client.get(f"contratos{query}")
            if not response.success:
                raise Exception(response.error)
            
            contratos_data = response.data.get('contratos', [])
            
            print(f"📋 Listando todos los contratos del hotel: {self.hotel_seleccionado.nombre}")
            print(f"✅ Se encontraron {len(contratos_data)} contratos")
            
            # Convertir a objetos Contrato
            from src.domain.contrato import Contrato
            contratos = []
            for data in contratos_data:
                contrato = Contrato.from_dict(data)
                # Agregar datos adicionales para el display
                contrato._reserva_data = data.get('reserva')
                contrato._habitacion_data = data.get('habitacion')
                contratos.append(contrato)
            
            self._mostrar_lista_contratos(contratos)
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar contratos: {str(e)}")
    
    def _mostrar_lista_contratos(self, contratos):
        """Muestra una lista de contratos"""
        # Limpiar solo el frame de resultados (no todo el content_frame)
        for widget in self.contratos_result_frame.winfo_children():
            widget.destroy()
        
        if not contratos:
            label = ctk.CTkLabel(
                self.contratos_result_frame,
                text="No se encontraron contratos",
                font=ctk.CTkFont(size=14)
            )
            label.pack(pady=20)
            return
        
        # Headers con anchos proporcionados
        header_frame = ctk.CTkFrame(self.contratos_result_frame, fg_color=("#2B7A78", "#14443F"), corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        # Configurar grid con anchos mínimos para alineación perfecta
        header_frame.grid_columnconfigure(0, weight=3, minsize=180)  # Cliente
        header_frame.grid_columnconfigure(1, weight=1, minsize=100)  # Habitación
        header_frame.grid_columnconfigure(2, weight=2, minsize=150)  # Check-in
        header_frame.grid_columnconfigure(3, weight=2, minsize=150)  # Check-out
        header_frame.grid_columnconfigure(4, weight=1, minsize=100)  # Estado
        header_frame.grid_columnconfigure(5, weight=1, minsize=120)  # Servicios
        header_frame.grid_columnconfigure(6, weight=1, minsize=100)  # Acción
        
        headers = ["Cliente", "Habitación", "Check-in", "Check-out", "Estado", "Servicios", "Acción"]
        
        for col, header in enumerate(headers):
            # Anclar a la izquierda solo la columna Cliente, el resto al centro
            anchor_pos = "w" if col == 0 else "center"
            
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor=anchor_pos
            )
            label.grid(row=0, column=col, padx=5, pady=15, sticky="ew")
        
        # Datos
        for idx, contrato in enumerate(contratos):
            bg_color = ("#2B2B2B", "#1E1E1E") if idx % 2 == 0 else ("#252525", "#252525")
            
            row_frame = ctk.CTkFrame(self.contratos_result_frame, fg_color=bg_color, corner_radius=5)
            row_frame.pack(fill="x", pady=3, padx=10)
            
            # Configurar grid EXACTAMENTE igual que header
            row_frame.grid_columnconfigure(0, weight=3, minsize=180)  # Cliente
            row_frame.grid_columnconfigure(1, weight=1, minsize=100)  # Habitación
            row_frame.grid_columnconfigure(2, weight=2, minsize=150)  # Check-in
            row_frame.grid_columnconfigure(3, weight=2, minsize=150)  # Check-out
            row_frame.grid_columnconfigure(4, weight=1, minsize=100)  # Estado
            row_frame.grid_columnconfigure(5, weight=1, minsize=120)  # Servicios
            row_frame.grid_columnconfigure(6, weight=1, minsize=100)  # Acción
            
            # Obtener información de la reserva
            cliente_nombre = "N/A"
            
            if contrato.reserva:
                if contrato.reserva.cliente_paga:
                    cliente_nombre = f"{contrato.reserva.cliente_paga.nombre} {contrato.reserva.cliente_paga.apellidos}"
            
            # Formatear fechas
            fecha_checkin = "N/A"
            if contrato.fecha_checkin:
                fecha_checkin = contrato.fecha_checkin.strftime("%d/%m/%Y %H:%M")
            
            fecha_checkout = "N/A"
            estado = "✅ Activo"
            estado_color = ("#27AE60", "#2ECC71")
            contrato_activo = True
            
            if contrato.fecha_checkout:
                fecha_checkout = contrato.fecha_checkout.strftime("%d/%m/%Y %H:%M")
                estado = "🔒 Finalizado"
                estado_color = ("#7F8C8D", "#95A5A6")
                contrato_activo = False
            
            # Columnas de datos con padding UNIFORME
            ctk.CTkLabel(row_frame, text=cliente_nombre, font=ctk.CTkFont(size=13), anchor="w").grid(row=0, column=0, padx=5, pady=10, sticky="ew")
            ctk.CTkLabel(row_frame, text=str(contrato.numero_habitacion), font=ctk.CTkFont(size=13), anchor="center").grid(row=0, column=1, padx=5, pady=10, sticky="ew")
            ctk.CTkLabel(row_frame, text=fecha_checkin, font=ctk.CTkFont(size=13), anchor="center").grid(row=0, column=2, padx=5, pady=10, sticky="ew")
            ctk.CTkLabel(row_frame, text=fecha_checkout, font=ctk.CTkFont(size=13), anchor="center").grid(row=0, column=3, padx=5, pady=10, sticky="ew")
            
            estado_label = ctk.CTkLabel(row_frame, text=estado, font=ctk.CTkFont(size=13), text_color=estado_color, anchor="center")
            estado_label.grid(row=0, column=4, padx=5, pady=10, sticky="ew")
            
            # Botón de añadir servicios (solo si el contrato está activo)
            if contrato_activo:
                btn_servicios = ctk.CTkButton(
                    row_frame,
                    text="➕ Servicios",
                    command=lambda c=contrato: self._mostrar_anadir_servicios(c),
                    fg_color=("#F39C12", "#E67E22"),
                    hover_color=("#E67E22", "#D35400"),
                    font=ctk.CTkFont(size=12, weight="bold"),
                    height=38
                )
                btn_servicios.grid(row=0, column=5, padx=5, pady=8, sticky="ew")
            else:
                # Espacio vacío si el contrato está finalizado
                ctk.CTkLabel(row_frame, text="-", font=ctk.CTkFont(size=13), anchor="center").grid(row=0, column=5, padx=5, pady=10, sticky="ew")
            
            btn_ver = ctk.CTkButton(
                row_frame,
                text="👁️ Ver",
                command=lambda c=contrato: self._mostrar_detalle_contrato(c),
                fg_color=("#1F618D", "#154360"),
                hover_color=("#2E86C1", "#1A5490"),
                font=ctk.CTkFont(size=13, weight="bold"),
                height=38
            )
            btn_ver.grid(row=0, column=6, padx=5, pady=8, sticky="ew")
    
    def _mostrar_detalle_contrato(self, contrato):
        """Muestra el detalle de un contrato con opción de check-out"""
        # Limpiar resultados
        for widget in self.contratos_result_frame.winfo_children():
            widget.destroy()
        
        # Obtener datos completos del contrato desde la API para tener pernoctaciones con servicios
        try:
            response = self.api_client.get(f"contratos/{contrato.id_contrato}")
            if response.success:
                contrato_completo = response.data
                pernoctaciones = contrato_completo.get('pernoctaciones', [])
            else:
                pernoctaciones = []
        except:
            pernoctaciones = []
        
        # Frame de detalle con estilo mejorado
        detalle_frame = ctk.CTkFrame(self.contratos_result_frame, corner_radius=15)
        detalle_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título con mejor estilo
        titulo = ctk.CTkLabel(
            detalle_frame,
            text=f"📋 Detalle de Contrato #{contrato.id_contrato}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        titulo.pack(pady=25)
        
        # Calcular precio total con servicios
        precio_base = float(contrato.monto_total)
        precio_servicios = 0.0
        
        for pern in pernoctaciones:
            servicios = pern.get('servicios', [])
            for servicio_pern in servicios:
                servicio = servicio_pern.get('servicio', {})
                precio_servicios += float(servicio.get('Precio', 0))
        
        precio_total_final = precio_base + precio_servicios
        
        # Información del contrato con mejor estilo
        info_frame = ctk.CTkFrame(detalle_frame, corner_radius=12)
        info_frame.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Información básica del contrato
        info = [
            ("ID Contrato:", contrato.id_contrato),
            ("ID Reserva:", contrato.id_reserva),
            ("Número Habitación:", contrato.numero_habitacion),
            ("Monto Base (Habitación + Régimen):", f"{precio_base:.2f} €"),
        ]
        
        # Solo mostrar servicios si hay
        if precio_servicios > 0:
            info.append(("Servicios Adicionales:", f"{precio_servicios:.2f} €"))
            info.append(("💰 TOTAL FINAL:", f"{precio_total_final:.2f} €"))
        
        # Formatear fechas
        if contrato.fecha_checkin:
            fecha_checkin_str = contrato.fecha_checkin.strftime("%d/%m/%Y a las %H:%M")
        else:
            fecha_checkin_str = "N/A"
        
        if contrato.fecha_checkout:
            fecha_checkout_str = contrato.fecha_checkout.strftime("%d/%m/%Y a las %H:%M")
        else:
            fecha_checkout_str = "❌ Pendiente (Activo)"
        
        info.append(("Fecha Check-in:", fecha_checkin_str))
        info.append(("Fecha Check-out:", fecha_checkout_str))
        info.append(("Estado:", contrato.estado))
        
        # Información de la reserva (si existe)
        if hasattr(contrato, 'reserva') and contrato.reserva:
            info.append(("", ""))  # Espacio
            info.append(("━━━━━ INFORMACIÓN DE LA RESERVA ━━━━━", ""))
            
            if hasattr(contrato.reserva, 'cliente_paga') and contrato.reserva.cliente_paga:
                cliente_nombre = f"{contrato.reserva.cliente_paga.nombre} {contrato.reserva.cliente_paga.apellidos}"
                info.append(("Cliente:", cliente_nombre))
            
            if hasattr(contrato.reserva, 'fecha_entrada'):
                info.append(("Fecha Entrada:", contrato.reserva.fecha_entrada))
            if hasattr(contrato.reserva, 'fecha_salida'):
                info.append(("Fecha Salida:", contrato.reserva.fecha_salida))
            if hasattr(contrato.reserva, 'numero_noches'):
                info.append(("Noches:", contrato.reserva.numero_noches))
            
            if hasattr(contrato.reserva, 'precio_regimen') and contrato.reserva.precio_regimen:
                if hasattr(contrato.reserva.precio_regimen, 'regimen') and contrato.reserva.precio_regimen.regimen:
                    info.append(("Régimen:", contrato.reserva.precio_regimen.regimen.codigo))
            
            if hasattr(contrato.reserva, 'pernoctaciones') and contrato.reserva.pernoctaciones:
                if hasattr(contrato.reserva.pernoctaciones[0], 'tipo_habitacion'):
                    tipo_hab = contrato.reserva.pernoctaciones[0].tipo_habitacion
                    if tipo_hab and hasattr(tipo_hab, 'categoria'):
                        info.append(("Tipo Habitación:", tipo_hab.categoria))
        
        for idx, (campo, valor) in enumerate(info):
            if not campo and not valor:  # Espacio vacío
                continue
                
            # Separador visual
            if "━━━━━" in campo:
                sep_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                sep_frame.pack(fill="x", pady=15, padx=15)
                
                sep_label = ctk.CTkLabel(
                    sep_frame,
                    text=campo,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=("#2B7A78", "#14443F")
                )
                sep_label.pack()
            else:
                # Alternar colores de fondo
                bg_color = ("#2B2B2B", "#1E1E1E") if idx % 2 == 0 else "transparent"
                frame = ctk.CTkFrame(info_frame, fg_color=bg_color, corner_radius=8)
                frame.pack(fill="x", pady=6, padx=15)
                
                ctk.CTkLabel(
                    frame,
                    text=campo,
                    font=ctk.CTkFont(size=15, weight="bold"),
                    width=220,
                    anchor="w"
                ).pack(side="left", padx=15, pady=12)
                
                ctk.CTkLabel(
                    frame,
                    text=str(valor),
                    font=ctk.CTkFont(size=15),
                    anchor="w"
                ).pack(side="left", padx=10, pady=12)
        
        # Mostrar servicios añadidos (si hay)
        if pernoctaciones and precio_servicios > 0:
            servicios_frame = ctk.CTkFrame(detalle_frame, corner_radius=12)
            servicios_frame.pack(fill="x", padx=30, pady=15)
            
            servicios_titulo = ctk.CTkLabel(
                servicios_frame,
                text="🛎️ Servicios Adicionales",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=("#2B7A78", "#14443F")
            )
            servicios_titulo.pack(pady=15)
            
            for pern in pernoctaciones:
                servicios = pern.get('servicios', [])
                if servicios:
                    fecha_pern = pern.get('fechaPernoctacion', 'N/A')
                    if fecha_pern != 'N/A':
                        from datetime import datetime
                        fecha_obj = datetime.fromisoformat(fecha_pern.replace('Z', '+00:00'))
                        fecha_pern = fecha_obj.strftime("%d/%m/%Y")
                    
                    pern_label = ctk.CTkLabel(
                        servicios_frame,
                        text=f"📅 {fecha_pern}:",
                        font=ctk.CTkFont(size=14, weight="bold"),
                        anchor="w"
                    )
                    pern_label.pack(anchor="w", padx=20, pady=(10, 5))
                    
                    for servicio_pern in servicios:
                        servicio = servicio_pern.get('servicio', {})
                        codigo = servicio.get('codigoServicio', 'N/A')
                        precio = float(servicio.get('Precio', 0))
                        
                        serv_label = ctk.CTkLabel(
                            servicios_frame,
                            text=f"   • {codigo}: {precio:.2f}€",
                            font=ctk.CTkFont(size=13),
                            anchor="w"
                        )
                        serv_label.pack(anchor="w", padx=35, pady=2)
        
        # Botones al final con mejor estilo
        botones_frame = ctk.CTkFrame(detalle_frame, fg_color="transparent")
        botones_frame.pack(pady=35)
        
        # Botón Volver
        btn_volver = ctk.CTkButton(
            botones_frame,
            text="⬅️ Volver a la Lista",
            command=self._listar_todos_contratos,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=("#34495E", "#2C3E50"),
            hover_color=("#5D6D7E", "#566573"),
            width=220,
            height=50,
            corner_radius=10
        )
        btn_volver.pack(side="left", padx=15)
        
        # Botón de Check-out (solo si no tiene checkout)
        if not contrato.fecha_checkout:
            btn_checkout = ctk.CTkButton(
                botones_frame,
                text="🚪 Hacer Check-out",
                command=lambda: self._hacer_checkout(contrato.id_contrato),
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=("#A93226", "#7B1F1F"),
                hover_color=("#C0392B", "#922B21"),
                width=220,
                height=50,
                corner_radius=10
            )
            btn_checkout.pack(side="left", padx=15)
        else:
            status = ctk.CTkLabel(
                botones_frame,
                text="✅ Check-out ya realizado",
                font=ctk.CTkFont(size=17, weight="bold"),
                text_color=("#27AE60", "#2ECC71")
            )
            status.pack(side="left", padx=15)
    
    def _hacer_checkout(self, id_contrato):
        """Realiza el check-out de un contrato"""
        try:
            if messagebox.askyesno("Confirmar", f"¿Realizar check-out del contrato {id_contrato}?"):
                contrato = self.reserva_service.hacer_checkout(id_contrato)
                messagebox.showinfo("Éxito", f"Check-out realizado. Fecha: {contrato.fecha_checkout}")
                self._mostrar_buscar_contratos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al hacer check-out: {str(e)}")
    
    def _mostrar_crear_reserva(self):
        """Muestra el formulario para crear una reserva"""
        self._limpiar_contenido()
        
        # Título con estilo mejorado
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="➕ Crear Nueva Reserva",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        titulo.pack(pady=(10, 30))
        
        # Scroll para el formulario con mejor padding
        scroll_form = ctk.CTkScrollableFrame(self.content_frame, corner_radius=15)
        scroll_form.pack(fill="both", expand=True, padx=80, pady=20)
        
        # === DATOS DE LA RESERVA ===
        reserva_label = ctk.CTkLabel(
            scroll_form,
            text="📅 Datos de la Reserva",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        reserva_label.pack(pady=(15, 25))
        
        # INFO: Fecha de entrada automática
        info_fecha_frame = ctk.CTkFrame(scroll_form, fg_color="transparent")
        info_fecha_frame.pack(fill="x", pady=10, padx=50)
        
        info_fecha = ctk.CTkLabel(
            info_fecha_frame,
            text="ℹ️ Fecha de Entrada: HOY (automática - " + datetime.now().strftime("%Y-%m-%d") + ")",
            font=ctk.CTkFont(size=13),
            text_color=("#5DADE2", "#3498DB"),
            anchor="w"
        )
        info_fecha.pack(side="left", padx=10)
        
        # Campo de Fecha Salida con botón de calendario
        self._crear_campo_fecha_con_calendario(scroll_form, "Fecha Salida:", "entry_fecha_salida")
        print(f"🔍 Después de crear campo fecha_salida: {hasattr(self, 'entry_fecha_salida')}")
        if hasattr(self, 'entry_fecha_salida'):
            print(f"   entry_fecha_salida = {self.entry_fecha_salida}")
        
        # Placeholder para disponibilidad (se cargará al ingresar fecha)
        self.disponibilidad_frame = ctk.CTkFrame(scroll_form, fg_color="transparent")
        self.disponibilidad_frame.pack(fill="x", pady=10, padx=50)
        
        info_disponibilidad = ctk.CTkLabel(
            self.disponibilidad_frame,
            text="ℹ️ Ingrese la fecha de salida para ver disponibilidad",
            font=ctk.CTkFont(size=13),
            text_color=("#95A5A6", "#7F8C8D"),
            anchor="w"
        )
        info_disponibilidad.pack(side="left", padx=10)
        
        # Cargar regímenes y crear dropdown (filtrado por hotel seleccionado)
        self._cargar_y_crear_dropdown_regimen(scroll_form)
        
        # Precio Total con mejor estilo
        precio_frame = ctk.CTkFrame(scroll_form, fg_color=("#1E1E1E", "#2B2B2B"), corner_radius=12)
        precio_frame.pack(fill="x", pady=25, padx=50)
        
        precio_label = ctk.CTkLabel(
            precio_frame,
            text="💰 Precio Total Estimado:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#F39C12", "#F39C12")
        )
        precio_label.pack(pady=(20, 8), padx=20)
        
        self.label_precio_total = ctk.CTkLabel(
            precio_frame,
            text="0.00 €",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#27AE60", "#2ECC71")
        )
        self.label_precio_total.pack(pady=(0, 20), padx=20)
        
        # === DATOS DEL CLIENTE ===
        cliente_label = ctk.CTkLabel(
            scroll_form,
            text="👤 Datos del Cliente que Paga",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#2B7A78", "#2B7A78")
        )
        cliente_label.pack(pady=(35, 25))
        
        self._crear_campo_form(scroll_form, "DNI:", "entry_dni", "11111111A")
        self._crear_campo_form(scroll_form, "Nombre:", "entry_nombre", "Juan")
        self._crear_campo_form(scroll_form, "Apellidos:", "entry_apellidos", "Pérez García")
        self._crear_campo_form(scroll_form, "Email:", "entry_email", "juan@example.com")
        self._crear_campo_form(scroll_form, "Fecha Nacimiento:", "entry_fecha_nac", "1990-01-15")
        
        # Botón crear con mejor estilo
        btn_frame = ctk.CTkFrame(scroll_form, fg_color="transparent")
        btn_frame.pack(pady=45)
        
        btn_crear = ctk.CTkButton(
            btn_frame,
            text="✅ Crear Reserva",
            command=self._crear_reserva,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            width=280,
            height=55,
            corner_radius=12
        )
        btn_crear.pack()
    
    def _crear_dropdown_canal(self, parent):
        """Crea el dropdown para canal de reserva"""
        campo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        campo_frame.pack(fill="x", pady=10, padx=50)
        
        label = ctk.CTkLabel(
            campo_frame,
            text="Canal Reserva:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            anchor="w"
        )
        label.pack(side="left", padx=10)
        
        self.dropdown_canal = ctk.CTkOptionMenu(
            campo_frame,
            values=["Web", "Telefono", "Presencial", "Email", "App Movil"],
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=("#2B7A78", "#14443F"),
            button_color=("#3D9970", "#2A7A5E"),
            button_hover_color=("#2B7A78", "#14443F")
        )
        self.dropdown_canal.set("Web")  # Valor por defecto
        self.dropdown_canal.pack(side="left", fill="x", expand=True, padx=10)
    
    def _crear_dropdown_tipo(self, parent):
        """Crea el dropdown para tipo de reserva"""
        campo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        campo_frame.pack(fill="x", pady=10, padx=50)
        
        label = ctk.CTkLabel(
            campo_frame,
            text="Tipo:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            anchor="w"
        )
        label.pack(side="left", padx=10)
        
        self.dropdown_tipo = ctk.CTkOptionMenu(
            campo_frame,
            values=["Reserva", "Walkin"],
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=("#2B7A78", "#14443F"),
            button_color=("#3D9970", "#2A7A5E"),
            button_hover_color=("#2B7A78", "#14443F")
        )
        self.dropdown_tipo.set("Reserva")  # Valor por defecto
        self.dropdown_tipo.pack(side="left", fill="x", expand=True, padx=10)
    
    def _cargar_disponibilidad(self):
        """Carga la disponibilidad según las fechas ingresadas"""
        try:
            print("🔍 Cargando disponibilidad...")
            
            # Limpiar el frame de disponibilidad
            for widget in self.disponibilidad_frame.winfo_children():
                widget.destroy()
            
            # Validar hotel
            if not self.hotel_seleccionado:
                info = ctk.CTkLabel(
                    self.disponibilidad_frame,
                    text="❌ No hay hotel seleccionado",
                    font=ctk.CTkFont(size=13),
                    text_color=("#E74C3C", "#C0392B")
                )
                info.pack(side="left", padx=10)
                return
            
            # Validar fecha de salida
            if not hasattr(self, 'entry_fecha_salida'):
                return
            
            fecha_salida_str = self.entry_fecha_salida.get().strip()
            if not fecha_salida_str:
                info = ctk.CTkLabel(
                    self.disponibilidad_frame,
                    text="ℹ️ Ingrese la fecha de salida para ver disponibilidad",
                    font=ctk.CTkFont(size=13),
                    text_color=("#95A5A6", "#7F8C8D")
                )
                info.pack(side="left", padx=10)
                return
            
            # Validar formato de fecha
            try:
                fecha_entrada = date.today()
                fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
                
                if fecha_salida <= fecha_entrada:
                    info = ctk.CTkLabel(
                        self.disponibilidad_frame,
                        text="❌ La fecha de salida debe ser posterior a hoy",
                        font=ctk.CTkFont(size=13),
                        text_color=("#E74C3C", "#C0392B")
                    )
                    info.pack(side="left", padx=10)
                    return
            except ValueError:
                info = ctk.CTkLabel(
                    self.disponibilidad_frame,
                    text="❌ Formato de fecha inválido (use YYYY-MM-DD)",
                    font=ctk.CTkFont(size=13),
                    text_color=("#E74C3C", "#C0392B")
                )
                info.pack(side="left", padx=10)
                return
            
            # Llamar al endpoint de disponibilidad CON EL ID DEL HOTEL
            url = f"disponibilidad?fechaEntrada={fecha_entrada}&fechaSalida={fecha_salida}&hotel={self.hotel_seleccionado.id_hotel}"
            print(f"🌐 Llamando a disponibilidad para hotel ID: {self.hotel_seleccionado.id_hotel} ({self.hotel_seleccionado.nombre})")
            print(f"🌐 URL: {url}")
            
            response = self.api_client.get(url)
            
            if not response.success or not response.data:
                info = ctk.CTkLabel(
                    self.disponibilidad_frame,
                    text="❌ Error al consultar disponibilidad",
                    font=ctk.CTkFont(size=13),
                    text_color=("#E74C3C", "#C0392B")
                )
                info.pack(side="left", padx=10)
                return
            
            # Extraer tipos disponibles
            tipos_disponibles = response.data.get('tiposDisponibles', [])
            
            if not tipos_disponibles:
                info = ctk.CTkLabel(
                    self.disponibilidad_frame,
                    text="⚠️ No hay habitaciones disponibles para estas fechas",
                    font=ctk.CTkFont(size=13),
                    text_color=("#F39C12", "#E67E22")
                )
                info.pack(side="left", padx=10)
                return
            
            print(f"✅ Tipos disponibles: {tipos_disponibles}")
            
            # Crear label
            label = ctk.CTkLabel(
                self.disponibilidad_frame,
                text="Tipo Habitación:",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=180,
                anchor="w"
            )
            label.pack(side="left", padx=10)
            
            # Crear opciones para el dropdown
            self.disponibilidad_data = {}
            opciones_display = []
            
            for tipo in tipos_disponibles:
                categoria = tipo['categoria']
                precio = float(tipo['precioPorNoche'])  # ✅ Convertir a float
                disponibles = tipo['disponibles']
                id_tipo = tipo['idTipoHabitacion']
                
                # Formato: "Doble Estándar - 100.00€/noche (5 disponibles)"
                texto = f"{categoria} - {precio:.2f}€/noche ({disponibles} disp.)"
                opciones_display.append(texto)
                
                # Guardar datos completos
                self.disponibilidad_data[texto] = {
                    'idTipoHabitacion': id_tipo,
                    'categoria': categoria,
                    'precioPorNoche': precio,
                    'disponibles': disponibles
                }
            
            # Crear dropdown
            self.dropdown_tipo_hab = ctk.CTkOptionMenu(
                self.disponibilidad_frame,
                values=opciones_display,
                height=40,
                font=ctk.CTkFont(size=13),
                fg_color=("#2B7A78", "#14443F"),
                button_color=("#3D9970", "#2A7A5E"),
                button_hover_color=("#2B7A78", "#14443F"),
                command=self._actualizar_precio_desde_disponibilidad
            )
            self.dropdown_tipo_hab.set(opciones_display[0])
            self.dropdown_tipo_hab.pack(side="left", fill="x", expand=True, padx=10)
            
            # Calcular precio inicial
            self._actualizar_precio_desde_disponibilidad(opciones_display[0])
            
        except Exception as e:
            print(f"❌ Error al cargar disponibilidad: {e}")
            import traceback
            traceback.print_exc()
            
            info = ctk.CTkLabel(
                self.disponibilidad_frame,
                text=f"❌ Error: {str(e)}",
                font=ctk.CTkFont(size=13),
                text_color=("#E74C3C", "#C0392B")
            )
            info.pack(side="left", padx=10)
    
    def _actualizar_precio_desde_disponibilidad(self, seleccion=None):
        """Actualiza el precio total usando los datos de disponibilidad"""
        try:
            print(f"💰 Actualizando precio para: {seleccion}")
            
            if not hasattr(self, 'label_precio_total'):
                return
            
            if not hasattr(self, 'disponibilidad_data') or not self.disponibilidad_data:
                self.label_precio_total.configure(text="0.00 €")
                return
            
            # Si no se pasó selección, usar el valor actual del dropdown
            if seleccion is None and hasattr(self, 'dropdown_tipo_hab'):
                seleccion = self.dropdown_tipo_hab.get()
            
            # Obtener datos del tipo seleccionado
            tipo_data = self.disponibilidad_data.get(seleccion)
            if not tipo_data:
                print(f"❌ No se encontraron datos para: {seleccion}")
                self.label_precio_total.configure(text="0.00 €")
                return
            
            precio_habitacion_noche = tipo_data['precioPorNoche']
            print(f"🏨 Precio habitación por noche: {precio_habitacion_noche}€")
            
            # Obtener precio del régimen
            precio_regimen_noche = 0
            if hasattr(self, 'dropdown_regimen') and hasattr(self, 'regimen_opciones') and self.regimen_opciones:
                regimen_seleccionado = self.dropdown_regimen.get()
                if regimen_seleccionado in self.regimen_opciones:
                    # Extraer precio del texto: "AD - 15€"
                    if " - " in regimen_seleccionado:
                        precio_str = regimen_seleccionado.split(" - ")[1].replace("€", "").strip()
                        try:
                            precio_regimen_noche = float(precio_str)
                            print(f"🍽️ Precio régimen por noche: {precio_regimen_noche}€")
                        except ValueError:
                            print(f"⚠️ No se pudo parsear precio del régimen: {precio_str}")
            
            # Calcular número de noches
            if not hasattr(self, 'entry_fecha_salida'):
                self.label_precio_total.configure(text="0.00 €")
                return
            
            try:
                fecha_entrada = date.today()
                fecha_salida_str = self.entry_fecha_salida.get().strip()
                fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
                num_noches = (fecha_salida - fecha_entrada).days
                
                print(f"🌙 Número de noches: {num_noches}")
                
                if num_noches <= 0:
                    self.label_precio_total.configure(text="0.00 €")
                    return
                
                # Calcular precio total: (precio habitación + precio régimen) × noches
                precio_por_noche_total = precio_habitacion_noche + precio_regimen_noche
                precio_total = precio_por_noche_total * num_noches
                
                print(f"💵 Precio por noche total: {precio_por_noche_total:.2f}€ (habitación: {precio_habitacion_noche}€ + régimen: {precio_regimen_noche}€)")
                print(f"✅ PRECIO TOTAL: {precio_total:.2f}€ ({precio_por_noche_total:.2f}€ × {num_noches} noches)")
                
                self.label_precio_total.configure(text=f"{precio_total:.2f} €")
                
            except (ValueError, AttributeError) as e:
                print(f"❌ Error al calcular noches: {e}")
                self.label_precio_total.configure(text="0.00 €")
                
        except Exception as e:
            print(f"❌ Error al actualizar precio: {e}")
            import traceback
            traceback.print_exc()
            if hasattr(self, 'label_precio_total'):
                self.label_precio_total.configure(text="0.00 €")
    def _cargar_y_crear_dropdown_regimen(self, parent):
        """Carga los regímenes disponibles del hotel seleccionado y crea el dropdown"""
        campo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        campo_frame.pack(fill="x", pady=12, padx=50)
        
        label = ctk.CTkLabel(
            campo_frame,
            text="Precio Régimen:",
            font=ctk.CTkFont(size=15, weight="bold"),
            width=200,
            anchor="w"
        )
        label.pack(side="left", padx=12)
        label.pack(side="left", padx=10)
        
        try:
            # Verificar que haya un hotel seleccionado
            if not self.hotel_seleccionado:
                raise Exception("No hay hotel seleccionado")
            
            # Llamar al nuevo endpoint de regímenes por hotel
            response = self.api_client.get(f"regimenes/hotel/{self.hotel_seleccionado.id_hotel}")
            
            if not response.success:
                raise Exception("Error al cargar regímenes del hotel")
            
            # Crear diccionario de opciones: "Código - Precio" -> idPrecioRegimen
            self.regimen_opciones = {}
            opciones_display = []
            
            # Parsear la respuesta del API
            if response.data and 'regimenes' in response.data:
                for regimen_data in response.data['regimenes']:
                    codigo = regimen_data['regimen']['codigo']
                    precio = regimen_data['precio']
                    id_precio_regimen = regimen_data['idPrecioRegimen']
                    
                    texto = f"{codigo} - {precio}€"
                    opciones_display.append(texto)
                    self.regimen_opciones[texto] = id_precio_regimen
            
            if not opciones_display:
                opciones_display = ["No hay regímenes disponibles"]
                self.regimen_opciones["No hay regímenes disponibles"] = None
            self.dropdown_regimen = ctk.CTkOptionMenu(
                campo_frame,
                values=opciones_display,
                height=45,
                font=ctk.CTkFont(size=14),
                fg_color=("#2B7A78", "#14443F"),
                button_color=("#3D9970", "#2A7A5E"),
                button_hover_color=("#2B7A78", "#14443F"),
                corner_radius=8,
                command=lambda x: self._actualizar_precio_desde_disponibilidad()
            )
            self.dropdown_regimen.set(opciones_display[0])
            self.dropdown_regimen.pack(side="left", fill="x", expand=True, padx=12)
            self.dropdown_regimen.pack(side="left", fill="x", expand=True, padx=10)
            
        except Exception as e:
            print(f"❌ Error al cargar regímenes: {e}")
            import traceback
            # Si falla, mostrar dropdown con mensaje de error
            self.dropdown_regimen = ctk.CTkOptionMenu(
                campo_frame,
                values=["Error al cargar regímenes"],
                height=45,
                font=ctk.CTkFont(size=14),
                corner_radius=8
            )
            self.dropdown_regimen.set("Error al cargar regímenes")
            self.dropdown_regimen.pack(side="left", fill="x", expand=True, padx=12)
            self.regimen_opciones = None
    
    def _crear_campo_form(self, parent, label_text, entry_name, placeholder):
        """Crea un campo del formulario"""
        campo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        campo_frame.pack(fill="x", pady=12, padx=50)
        
        label = ctk.CTkLabel(
            campo_frame,
            text=label_text,
            font=ctk.CTkFont(size=15, weight="bold"),
            width=200,
            anchor="w"
        )
        label.pack(side="left", padx=12)
        
        entry = ctk.CTkEntry(
            campo_frame,
            placeholder_text=placeholder,
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        entry.pack(side="left", fill="x", expand=True, padx=12)
        
        # Guardar referencia al entry
        setattr(self, entry_name, entry)
        
        # Si es fecha_salida, agregar binding para cargar disponibilidad
        if entry_name == "entry_fecha_salida":
            entry.bind("<FocusOut>", lambda e: self._cargar_disponibilidad())
            entry.bind("<Return>", lambda e: self._cargar_disponibilidad())
    
    def _crear_campo_fecha_con_calendario(self, parent, label_text, entry_name):
        """Crea un campo de fecha con botón de calendario"""
        try:
            campo_frame = ctk.CTkFrame(parent, fg_color="transparent")
            campo_frame.pack(fill="x", pady=10, padx=50)
            
            label = ctk.CTkLabel(
                campo_frame,
                text=label_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=180,
                anchor="w"
            )
            label.pack(side="left", padx=10)
            
            # Frame para entry + botón
            entrada_frame = ctk.CTkFrame(campo_frame, fg_color="transparent")
            entrada_frame.pack(side="left", fill="x", expand=True, padx=10)
            
            entry = ctk.CTkEntry(
                entrada_frame,
                placeholder_text="YYYY-MM-DD",
                height=40,
                font=ctk.CTkFont(size=13)
            )
            entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Botón de calendario
            btn_calendario = ctk.CTkButton(
                entrada_frame,
                text="📅",
                width=50,
                height=40,
                font=ctk.CTkFont(size=18),
                fg_color=("#2B7A78", "#14443F"),
                hover_color=("#3D9970", "#2A7A5E"),
                command=lambda: self._abrir_calendario(entry)
            )
            btn_calendario.pack(side="left")
            
            # Guardar referencia al entry
            setattr(self, entry_name, entry)
            print(f"✅ Campo {entry_name} creado correctamente")
            
            # Agregar binding para cargar disponibilidad
            entry.bind("<FocusOut>", lambda e: self._cargar_disponibilidad())
            entry.bind("<Return>", lambda e: self._cargar_disponibilidad())
        except Exception as e:
            print(f"❌ Error al crear campo de fecha con calendario: {e}")
            import traceback
            traceback.print_exc()
            # Crear campo simple como fallback
            self._crear_campo_form(parent, label_text, entry_name, "YYYY-MM-DD")
    
    def _abrir_calendario(self, entry_fecha):
        """Abre un diálogo con calendario para seleccionar fecha"""
        # Crear ventana modal
        cal_window = Toplevel(self.root)
        cal_window.title("Seleccionar Fecha")
        cal_window.geometry("350x400")
        cal_window.resizable(False, False)
        
        # Centrar ventana
        cal_window.transient(self.root)
        cal_window.grab_set()
        
        # Configurar color de fondo
        cal_window.configure(bg="#2B2B2B")
        
        # Label
        label = ctk.CTkLabel(
            cal_window,
            text="📅 Seleccione la fecha de salida",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=20)
        
        # Obtener fecha actual o fecha del entry
        fecha_inicial = date.today() + timedelta(days=1)  # Mañana por defecto
        
        try:
            if entry_fecha.get():
                fecha_inicial = datetime.strptime(entry_fecha.get(), "%Y-%m-%d").date()
        except:
            pass
        
        # Crear calendario
        cal = Calendar(
            cal_window,
            selectmode='day',
            year=fecha_inicial.year,
            month=fecha_inicial.month,
            day=fecha_inicial.day,
            date_pattern='yyyy-mm-dd',
            background='#2B7A78',
            foreground='white',
            selectbackground='#F39C12',
            selectforeground='white',
            bordercolor='#2B7A78',
            headersbackground='#1E1E1E',
            headersforeground='white',
            normalbackground='#2B2B2B',
            normalforeground='white',
            weekendbackground='#3D3D3D',
            weekendforeground='white',
            othermonthforeground='#7F8C8D',
            othermonthbackground='#1E1E1E',
            mindate=date.today(),  # No permitir fechas pasadas
            font=('Arial', 10)
        )
        cal.pack(pady=20, padx=20)
        
        def seleccionar_fecha():
            """Inserta la fecha seleccionada en el entry"""
            fecha_seleccionada = cal.get_date()
            entry_fecha.delete(0, 'end')
            entry_fecha.insert(0, fecha_seleccionada)
            cal_window.destroy()
            # Cargar disponibilidad automáticamente
            self._cargar_disponibilidad()
        
        # Botones
        btn_frame = ctk.CTkFrame(cal_window, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        btn_seleccionar = ctk.CTkButton(
            btn_frame,
            text="✓ Seleccionar",
            command=seleccionar_fecha,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E"),
            width=120
        )
        btn_seleccionar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="✖ Cancelar",
            command=cal_window.destroy,
            font=ctk.CTkFont(size=14),
            fg_color=("#95A5A6", "#7F8C8D"),
            hover_color=("#BDC3C7", "#95A5A6"),
            width=120
        )
        btn_cancelar.pack(side="left", padx=10)
    
    def _crear_reserva(self):
        """Crea una nueva reserva según API_GUIDE"""
        try:
            # Datos de la reserva
            fecha_entrada = date.today()  # ✅ Fecha automática (HOY)
            
            # Validar que existe el campo fecha_salida
            if not hasattr(self, 'entry_fecha_salida') or self.entry_fecha_salida is None:
                messagebox.showerror("Error", "Campo de fecha de salida no encontrado. Por favor, recargue el formulario.")
                return
            
            fecha_salida_str = self.entry_fecha_salida.get().strip()
            if not fecha_salida_str:
                messagebox.showwarning("Advertencia", "Debe ingresar la fecha de salida")
                return
            
            fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d").date()
            
            # Canal y tipo siempre PMS y Walkin (gestión interna del hotel)
            canal = "PMS"
            tipo = "Walkin"
            
            # ID Precio Régimen desde dropdown
            if not hasattr(self, 'dropdown_regimen') or self.dropdown_regimen is None:
                messagebox.showerror("Error", "Dropdown de régimen no encontrado. Por favor, recargue el formulario.")
                print(f"❌ dropdown_regimen no existe o es None")
                return
                
            if self.regimen_opciones:
                texto_seleccionado = self.dropdown_regimen.get()
                id_precio_regimen = self.regimen_opciones.get(texto_seleccionado)
                if not id_precio_regimen:
                    messagebox.showerror("Error", "Debe seleccionar un régimen válido")
                    return
            else:
                # Fallback a campo de texto si no hay opciones
                id_precio_regimen = int(self.entry_precio_regimen.get().strip())
            
            # Tipo de habitación desde disponibilidad
            if not hasattr(self, 'dropdown_tipo_hab') or self.dropdown_tipo_hab is None:
                messagebox.showerror("Error", "Dropdown de tipo de habitación no encontrado. Debe cargar la disponibilidad primero.")
                print(f"❌ dropdown_tipo_hab no existe o es None")
                return
                
            if hasattr(self, 'disponibilidad_data') and self.disponibilidad_data:
                tipo_hab_seleccionado = self.dropdown_tipo_hab.get()
                print(f"🔍 DEBUG - Tipo habitación seleccionado: '{tipo_hab_seleccionado}'")
                print(f"🔍 DEBUG - Disponibilidad data keys: {list(self.disponibilidad_data.keys())}")
                tipo_data = self.disponibilidad_data.get(tipo_hab_seleccionado)
                if not tipo_data:
                    messagebox.showerror("Error", "Debe seleccionar un tipo de habitación válido")
                    return
                id_tipo_habitacion = tipo_data['idTipoHabitacion']
                print(f"🔍 DEBUG - ID tipo habitación: {id_tipo_habitacion}")
                print(f"🔍 DEBUG - Categoria: {tipo_data['categoria']}")
            else:
                messagebox.showerror("Error", "Debe cargar la disponibilidad primero (ingrese fecha de salida)")
                return
            
            # Datos del cliente - Validar que todos los campos existen
            campos_cliente = {
                'entry_dni': 'DNI',
                'entry_nombre': 'Nombre',
                'entry_apellidos': 'Apellidos',
                'entry_email': 'Email',
                'entry_fecha_nac': 'Fecha de Nacimiento'
            }
            
            for campo_attr, campo_nombre in campos_cliente.items():
                if not hasattr(self, campo_attr) or getattr(self, campo_attr) is None:
                    messagebox.showerror("Error", f"Campo '{campo_nombre}' no encontrado. Por favor, recargue el formulario.")
                    print(f"❌ Campo {campo_attr} no existe o es None")
                    return
            
            dni = self.entry_dni.get().strip()
            nombre = self.entry_nombre.get().strip()
            apellidos = self.entry_apellidos.get().strip()
            email = self.entry_email.get().strip()
            fecha_nac = self.entry_fecha_nac.get().strip()
            
            if not all([fecha_entrada, fecha_salida, tipo, id_precio_regimen, dni, nombre, apellidos, email]):
                messagebox.showwarning("Advertencia", "Complete todos los campos obligatorios")
                return
            
            # Crear pernoctaciones (una por cada noche)
            num_noches = (fecha_salida - fecha_entrada).days
            pernoctaciones = []
            for i in range(num_noches):
                fecha_pernoctacion = fecha_entrada + timedelta(days=i)
                pernoctaciones.append({
                    "fechaPernoctacion": fecha_pernoctacion.isoformat(),
                    "idTipoHabitacion": id_tipo_habitacion  # ✅ Usar tipo seleccionado
                })
            
            # Obtener datos del hotel, tipo habitación y régimen desde el precio_regimen
            # Necesitamos obtener estos datos de la disponibilidad cargada
            tipo_hab_data = self.disponibilidad_data.get(tipo_hab_seleccionado)
            categoria_habitacion = tipo_hab_data['categoria']
            print(f"🔍 DEBUG - Categoría habitación para API: '{categoria_habitacion}'")
            
            # Obtener régimen desde el dropdown
            texto_regimen = self.dropdown_regimen.get()
            # El texto tiene formato "Régimen X - XX.XX€"
            # Extraer el nombre del régimen (parte antes del " - ")
            regimen_nombre = texto_regimen.split(' - ')[0] if ' - ' in texto_regimen else texto_regimen
            
            # Mapear nombre de régimen a código (según la DB)
            regimen_map = {
                "Solo Alojamiento": "SA",
                "Alojamiento y Desayuno": "AD",
                "Media Pensión": "MP",
                "Pensión Completa": "PC",
                "Todo Incluido": "TI"
            }
            codigo_regimen = regimen_map.get(regimen_nombre, "SA")
            
            # Llamar al servicio
            reserva_data = {
                "fechaEntrada": fecha_entrada.isoformat(),
                "fechaSalida": fecha_salida.isoformat(),
                "canalReserva": canal,
                "tipo": tipo,
                "clientePaga": {
                    "nombre": nombre,
                    "apellidos": apellidos,
                    "correoElectronico": email,
                    "DNI": dni,
                    "fechaDeNacimiento": fecha_nac
                },
                "hotel": self.hotel_seleccionado.nombre,
                "tipoHabitacion": categoria_habitacion,
                "regimen": codigo_regimen,
                "huespedes": [{
                    "nombre": nombre,
                    "apellidos": apellidos,
                    "correoElectronico": email,
                    "DNI": dni
                }]
            }
            
            # Hacer POST directo a la API
            print(f"📤 Enviando datos de reserva: {reserva_data}")
            response = self.api_client.post("reservas", reserva_data)
            print(f"📥 Respuesta recibida - success: {response.success}, data: {response.data}, error: {response.error}")
            
            if not response.success:
                error_msg = response.error or "Error desconocido al crear la reserva"
                if response.data and isinstance(response.data, dict):
                    error_msg = response.data.get('message', error_msg)
                messagebox.showerror("Error", f"No se pudo crear la reserva:\n\n{error_msg}")
                return
            
            reserva_creada = response.data
            if not reserva_creada:
                messagebox.showerror("Error", "La API no devolvió datos de la reserva creada")
                return
            
            id_reserva = reserva_creada.get('idReserva', 'desconocido')
            messagebox.showinfo("Éxito", f"✅ Reserva creada con ID: {id_reserva}")
            self._mostrar_buscar_reservas()
            
        except ValueError as e:
            print(f"❌ ValueError en _crear_reserva: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Verifique que todos los campos tengan el formato correcto\n\nDetalle: {str(e)}")
        except Exception as e:
            print(f"❌ Exception en _crear_reserva: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al crear reserva: {str(e)}")
    
    def _mostrar_anadir_servicios(self, contrato):
        """Muestra el panel para añadir servicios a las pernoctaciones de un contrato"""
        try:
            # Limpiar contenido principal
            self._limpiar_contenido()
            
            # Obtener datos completos del contrato desde la API
            response = self.api_client.get(f"contratos/{contrato.id_contrato}")
            if not response.success:
                messagebox.showerror("Error", f"No se pudo obtener el contrato: {response.error}")
                return
            
            contrato_data = response.data
            pernoctaciones = contrato_data.get('pernoctaciones', [])
            
            if not pernoctaciones:
                messagebox.showwarning("Advertencia", "Este contrato no tiene pernoctaciones")
                return
            
            # Obtener servicios disponibles
            servicios_response = self.api_client.get("servicios")
            if not servicios_response.success:
                messagebox.showerror("Error", f"No se pudieron obtener los servicios: {servicios_response.error}")
                return
            
            servicios_disponibles = servicios_response.data
            
            # Título
            titulo = ctk.CTkLabel(
                self.content_frame,
                text=f"🛎️ Añadir Servicios al Contrato #{contrato.id_contrato}",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=("#2B7A78", "#2B7A78")
            )
            titulo.pack(pady=20)
            
            # Información del cliente
            if contrato.reserva and contrato.reserva.cliente_paga:
                info_cliente = ctk.CTkLabel(
                    self.content_frame,
                    text=f"Cliente: {contrato.reserva.cliente_paga.nombre} {contrato.reserva.cliente_paga.apellidos} | Habitación: {contrato.numero_habitacion}",
                    font=ctk.CTkFont(size=14),
                    text_color=("#7F8C8D", "#95A5A6")
                )
                info_cliente.pack(pady=5)
            
            # Frame principal con scroll
            scroll_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=15)
            scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Mostrar cada pernoctación
            for idx, pernoctacion in enumerate(pernoctaciones):
                fecha_pern = pernoctacion.get('fechaPernoctacion', 'N/A')
                if fecha_pern != 'N/A':
                    from datetime import datetime
                    fecha_obj = datetime.fromisoformat(fecha_pern.replace('Z', '+00:00'))
                    fecha_pern = fecha_obj.strftime("%d/%m/%Y")
                
                tipo_hab = pernoctacion.get('tipoHabitacion', {})
                tipo_hab_nombre = tipo_hab.get('categoria', 'N/A')
                
                # Frame para esta pernoctación
                pern_frame = ctk.CTkFrame(scroll_frame, corner_radius=12)
                pern_frame.pack(fill="x", pady=10, padx=10)
                
                # Header de la pernoctación
                header_frame = ctk.CTkFrame(pern_frame, fg_color=("#2B7A78", "#14443F"), corner_radius=8)
                header_frame.pack(fill="x", padx=10, pady=10)
                
                pern_label = ctk.CTkLabel(
                    header_frame,
                    text=f"🌙 Noche {idx + 1} - {fecha_pern} ({tipo_hab_nombre})",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                pern_label.pack(pady=10)
                
                # Servicios ya añadidos a esta pernoctación
                servicios_actuales = pernoctacion.get('servicios', [])
                if servicios_actuales:
                    servicios_label = ctk.CTkLabel(
                        pern_frame,
                        text=f"✓ Servicios actuales: {', '.join([s.get('servicio', {}).get('codigoServicio', 'N/A') for s in servicios_actuales])}",
                        font=ctk.CTkFont(size=12),
                        text_color=("#27AE60", "#2ECC71")
                    )
                    servicios_label.pack(pady=5)
                
                # Dropdown para seleccionar servicio
                servicios_frame = ctk.CTkFrame(pern_frame, fg_color="transparent")
                servicios_frame.pack(fill="x", pady=10, padx=15)
                
                label_servicio = ctk.CTkLabel(
                    servicios_frame,
                    text="Servicio:",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                label_servicio.pack(side="left", padx=10)
                
                # Crear opciones con nombre y precio
                servicios_opciones = {}
                for servicio in servicios_disponibles:
                    codigo = servicio.get('codigoServicio', '')
                    precio = float(servicio.get('Precio', 0))
                    texto = f"{codigo} - {precio:.2f}€"
                    servicios_opciones[texto] = codigo
                
                dropdown_servicio = ctk.CTkOptionMenu(
                    servicios_frame,
                    values=list(servicios_opciones.keys()),
                    font=ctk.CTkFont(size=13),
                    width=250
                )
                dropdown_servicio.pack(side="left", padx=10)
                dropdown_servicio.set(list(servicios_opciones.keys())[0] if servicios_opciones else "")
                
                # Botón añadir
                btn_anadir = ctk.CTkButton(
                    servicios_frame,
                    text="➕ Añadir",
                    command=lambda p=pernoctacion, d=dropdown_servicio, ops=servicios_opciones: self._anadir_servicio_pernoctacion_inline(p, d, ops, contrato),
                    fg_color=("#27AE60", "#229954"),
                    hover_color=("#2ECC71", "#27AE60"),
                    font=ctk.CTkFont(size=13, weight="bold"),
                    width=120
                )
                btn_anadir.pack(side="left", padx=10)
            
            # Botón volver
            btn_volver = ctk.CTkButton(
                self.content_frame,
                text="⬅️ Volver a Contratos",
                command=self._mostrar_buscar_contratos,
                fg_color=("#95A5A6", "#7F8C8D"),
                hover_color=("#BDC3C7", "#95A5A6"),
                font=ctk.CTkFont(size=15, weight="bold"),
                width=200,
                height=45
            )
            btn_volver.pack(pady=20)
            
        except Exception as e:
            print(f"❌ Error al mostrar añadir servicios: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al mostrar servicios: {str(e)}")
    
    def _anadir_servicio_pernoctacion_inline(self, pernoctacion, dropdown, opciones, contrato):
        """Añade un servicio a una pernoctación específica (versión inline sin ventana modal)"""
        try:
            id_pernoctacion = pernoctacion.get('idPernoctacion')
            servicio_seleccionado = dropdown.get()
            codigo_servicio = opciones.get(servicio_seleccionado)
            
            if not codigo_servicio:
                messagebox.showwarning("Advertencia", "Debe seleccionar un servicio")
                return
            
            # Llamar a la API
            response = self.api_client.post(
                f"pernoctaciones/{id_pernoctacion}/servicios",
                {"codigoServicio": codigo_servicio}
            )
            
            if not response.success:
                error_msg = response.error or "Error desconocido"
                if response.data and isinstance(response.data, dict):
                    error_msg = response.data.get('message', error_msg)
                messagebox.showerror("Error", f"No se pudo añadir el servicio:\n\n{error_msg}")
                return
            
            # Mostrar mensaje de éxito en consola
            print(f"✅ Servicio {codigo_servicio} añadido correctamente")
            
            # Refrescar la pantalla completa
            self._mostrar_anadir_servicios(contrato)
            
        except Exception as e:
            print(f"❌ Error al añadir servicio: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al añadir servicio: {str(e)}")
    
    # ============= MÉTODOS PARA GESTIÓN DE HUÉSPEDES INLINE =============
    
    def _anadir_huesped_checkin(self):
        """Añade un huésped a la lista temporal del check-in"""
        try:
            nombre = self.checkin_nombre_entry.get().strip()
            apellidos = self.checkin_apellidos_entry.get().strip()
            email = self.checkin_email_entry.get().strip()
            dni = self.checkin_dni_entry.get().strip()
            
            if not all([nombre, apellidos, email, dni]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                return
            
            # Validar capacidad (+1 por el cliente que paga)
            capacidad = self.checkin_data['capacidad']
            huespedes_actuales = len(self.checkin_data['huespedes'])
            
            if huespedes_actuales + 1 >= capacidad:
                messagebox.showwarning(
                    "Capacidad Excedida",
                    f"La habitación solo tiene capacidad para {capacidad} persona(s).\n"
                    f"Ya has añadido {huespedes_actuales} huésped(es) + 1 cliente que paga = {huespedes_actuales + 1}"
                )
                return
            
            # Validar DNI duplicado
            if any(h['DNI'] == dni for h in self.checkin_data['huespedes']):
                messagebox.showwarning("DNI Duplicado", "Ya existe un huésped con ese DNI")
                return
            
            # Añadir huésped
            huesped = {
                'nombre': nombre,
                'apellidos': apellidos,
                'correoElectronico': email,
                'DNI': dni
            }
            self.checkin_data['huespedes'].append(huesped)
            
            # Actualizar UI
            self._actualizar_lista_huespedes_checkin()
            self._limpiar_formulario_checkin()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al añadir huésped: {str(e)}")
    
    def _actualizar_lista_huespedes_checkin(self):
        """Actualiza la visualización de la lista de huéspedes"""
        try:
            # Limpiar lista
            for widget in self.checkin_lista_scroll.winfo_children():
                widget.destroy()
            
            # Actualizar título
            huespedes_count = len(self.checkin_data['huespedes'])
            total = huespedes_count + 1  # +1 por el cliente que paga
            capacidad = self.checkin_data['capacidad']
            
            self.checkin_lista_title_label.configure(
                text=f"📋 Huéspedes Añadidos ({huespedes_count}) - Total: {total}/{capacidad}"
            )
            
            # Cliente que paga (info)
            cliente_frame = ctk.CTkFrame(self.checkin_lista_scroll, corner_radius=8, fg_color=("#E8F5E9", "#1B5E20"))
            cliente_frame.pack(fill="x", pady=2, padx=5)
            
            info_label = ctk.CTkLabel(
                cliente_frame,
                text="👤 Cliente que paga (se añade automáticamente)",
                font=ctk.CTkFont(size=11),
                text_color=("#2E7D32", "#A5D6A7")
            )
            info_label.pack(pady=8, padx=10)
            
            # Mostrar huéspedes
            for idx, huesped in enumerate(self.checkin_data['huespedes']):
                huesped_frame = ctk.CTkFrame(self.checkin_lista_scroll, corner_radius=8)
                huesped_frame.pack(fill="x", pady=2, padx=5)
                
                # Info del huésped
                info_frame = ctk.CTkFrame(huesped_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
                
                nombre_label = ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {huesped['nombre']} {huesped['apellidos']}",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                nombre_label.pack(anchor="w")
                
                detalles_label = ctk.CTkLabel(
                    info_frame,
                    text=f"DNI: {huesped['DNI']} | Email: {huesped['correoElectronico']}",
                    font=ctk.CTkFont(size=10),
                    text_color="gray"
                )
                detalles_label.pack(anchor="w")
                
                # Botón eliminar
                btn_eliminar = ctk.CTkButton(
                    huesped_frame,
                    text="🗑️",
                    width=40,
                    command=lambda i=idx: self._eliminar_huesped_checkin(i),
                    fg_color=("#E74C3C", "#C0392B"),
                    hover_color=("#C0392B", "#A93226")
                )
                btn_eliminar.pack(side="right", padx=5)
                
        except Exception as e:
            print(f"Error actualizando lista: {e}")
    
    def _eliminar_huesped_checkin(self, index: int):
        """Elimina un huésped de la lista temporal"""
        try:
            if messagebox.askyesno("Confirmar", "¿Eliminar este huésped?"):
                del self.checkin_data['huespedes'][index]
                self._actualizar_lista_huespedes_checkin()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar huésped: {str(e)}")
    
    def _limpiar_formulario_checkin(self):
        """Limpia los campos del formulario de check-in"""
        try:
            self.checkin_nombre_entry.delete(0, 'end')
            self.checkin_apellidos_entry.delete(0, 'end')
            self.checkin_email_entry.delete(0, 'end')
            self.checkin_dni_entry.delete(0, 'end')
        except Exception as e:
            print(f"Error limpiando formulario: {e}")
    
    def _realizar_checkin_final(self):
        """Realiza el check-in final con todos los huéspedes añadidos"""
        try:
            reserva = self.checkin_data['reserva']
            numero_hab = self.checkin_data['numero_hab']
            huespedes_lista = self.checkin_data['huespedes']
            
            # Hacer check-in con número de habitación y huéspedes
            checkin_payload = {
                "numeroHabitacion": numero_hab,
                "huespedes": huespedes_lista
            }
            
            checkin_response = self.api_client.post(
                f"reservas/{reserva.id_reserva}/checkin",
                checkin_payload
            )
            
            if not checkin_response.success:
                messagebox.showerror(
                    "Error",
                    f"Error al hacer check-in: {checkin_response.error}"
                )
                return
            
            # Éxito - mostrar en consola sin popup
            print(f"✅ Check-in realizado correctamente")
            print(f"📍 Habitación: {numero_hab}")
            print(f"👥 Huéspedes registrados: {len(huespedes_lista)} + 1 (titular)")
            print(f"🏨 Tipo: {self.checkin_data['categoria']}")
            
            messagebox.showinfo(
                "Éxito",
                f"✅ Check-in realizado correctamente\n"
                f"📍 Habitación: {numero_hab}\n"
                f"👥 Huéspedes registrados: {len(huespedes_lista)} + 1 (titular)\n"
                f"🏨 Tipo: {self.checkin_data['categoria']}"
            )
            
            # Volver a la búsqueda de reservas
            self._mostrar_buscar_reservas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar check-in: {str(e)}")
