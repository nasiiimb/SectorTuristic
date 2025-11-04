"""
ConsultaPanel - Panel de consultas con diseño moderno
"""
import customtkinter as ctk
from tkinter import messagebox


class ConsultaPanel:
    """Panel para consultar todas las tablas con CustomTkinter"""
    
    def __init__(self, parent, consulta_service):
        self.parent = parent
        self.consulta_service = consulta_service
        
        # Configurar parent
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea los widgets principales"""
        # TabView para las diferentes consultas
        self.tabview = ctk.CTkTabview(
            self.main_container,
            corner_radius=15,
            segmented_button_fg_color=("#2B7A78", "#14443F"),
            segmented_button_selected_color=("#3D9970", "#2A7A5E"),
            segmented_button_selected_hover_color=("#4CAF8F", "#358F6F"),
            segmented_button_unselected_color=("#1E5F5C", "#0F3532"),
            segmented_button_unselected_hover_color=("#276F6C", "#1A4A47")
        )
        self.tabview.grid(row=0, column=0, sticky="nsew")
        
        # Crear pestañas
        self.tabview.add(" Hoteles")
        self.tabview.add(" Ciudades")
        self.tabview.add(" Tipos Habitación")
        self.tabview.add(" Regímenes")
        self.tabview.add(" Contratos")
        
        # Configurar pestañas
        for tab_name in [" Hoteles", " Ciudades", " Tipos Habitación", " Regímenes", " Contratos"]:
            self.tabview.tab(tab_name).grid_rowconfigure(0, weight=1)
            self.tabview.tab(tab_name).grid_columnconfigure(0, weight=1)
        
        # Crear tablas
        self._create_hoteles_table()
        self._create_ciudades_table()
        self._create_tipos_habitacion_table()
        self._create_regimenes_table()
        self._create_contratos_table()
    
    def _create_hoteles_table(self):
        """Crea la tabla de hoteles"""
        tab = self.tabview.tab(" Hoteles")
        
        container = ctk.CTkFrame(tab, corner_radius=15)
        container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(header_frame, text=" Hoteles Disponibles", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, sticky="w")
        
        btn_refresh = ctk.CTkButton(header_frame, text=" Actualizar", command=self._load_hoteles, width=120, height=32, font=ctk.CTkFont(size=12), fg_color=("#2B7A78", "#14443F"), hover_color=("#3D9970", "#2A7A5E"))
        btn_refresh.grid(row=0, column=1, sticky="e")
        
        self.hoteles_scroll = ctk.CTkScrollableFrame(container, fg_color=("gray90", "gray15"))
        self.hoteles_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.hoteles_scroll.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        headers = ["ID", "Nombre", "Estrellas", "Ciudad", "Teléfono"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.hoteles_scroll, text=header, font=ctk.CTkFont(size=14, weight="bold"), fg_color=("#2B7A78", "#14443F"), corner_radius=5)
            label.grid(row=0, column=col, sticky="ew", padx=5, pady=5)
        
        self._load_hoteles()
    
    def _load_hoteles(self):
        for widget in self.hoteles_scroll.winfo_children()[5:]:
            widget.destroy()
        try:
            hoteles = self.consulta_service.obtener_hoteles()
            for idx, hotel in enumerate(hoteles, start=1):
                row = idx
                bg_color = ("#2B2B2B", "#1E1E1E") if row % 2 == 0 else ("#252525", "#252525")
                id_frame = ctk.CTkFrame(self.hoteles_scroll, fg_color=bg_color, corner_radius=5)
                id_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=3)
                ctk.CTkLabel(id_frame, text=str(hotel.id_hotel), font=ctk.CTkFont(size=13), anchor="center").pack(padx=10, pady=10, fill="x")
                nombre_frame = ctk.CTkFrame(self.hoteles_scroll, fg_color=bg_color, corner_radius=5)
                nombre_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
                ctk.CTkLabel(nombre_frame, text=hotel.nombre, font=ctk.CTkFont(size=13), anchor="w").pack(fill="x", padx=10, pady=10)
                estrellas_frame = ctk.CTkFrame(self.hoteles_scroll, fg_color=bg_color, corner_radius=5)
                estrellas_frame.grid(row=row, column=2, sticky="ew", padx=5, pady=3)
                estrellas_text = "⭐" * hotel.numero_estrellas if hotel.numero_estrellas else "N/A"
                ctk.CTkLabel(estrellas_frame, text=estrellas_text, font=ctk.CTkFont(size=13), anchor="center").pack(padx=10, pady=10, fill="x")
                ciudad_frame = ctk.CTkFrame(self.hoteles_scroll, fg_color=bg_color, corner_radius=5)
                ciudad_frame.grid(row=row, column=3, sticky="ew", padx=5, pady=3)
                ciudad_text = hotel.ciudad.nombre if hotel.ciudad else "N/A"
                ctk.CTkLabel(ciudad_frame, text=ciudad_text, font=ctk.CTkFont(size=13), anchor="w").pack(fill="x", padx=10, pady=10)
                tel_frame = ctk.CTkFrame(self.hoteles_scroll, fg_color=bg_color, corner_radius=5)
                tel_frame.grid(row=row, column=4, sticky="ew", padx=5, pady=3)
                ctk.CTkLabel(tel_frame, text=hotel.telefono or "N/A", font=ctk.CTkFont(size=13), anchor="w").pack(fill="x", padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar hoteles: {str(e)}")

    
    def _create_ciudades_table(self):
        tab = self.tabview.tab(" Ciudades")
        label = ctk.CTkLabel(tab, text="Tabla de Ciudades - Funcional", font=ctk.CTkFont(size=16))
        label.pack(expand=True)
    
    def _create_tipos_habitacion_table(self):
        tab = self.tabview.tab(" Tipos Habitación")
        label = ctk.CTkLabel(tab, text="Tabla de Tipos Habitación - Funcional", font=ctk.CTkFont(size=16))
        label.pack(expand=True)
    
    def _create_regimenes_table(self):
        tab = self.tabview.tab(" Regímenes")
        label = ctk.CTkLabel(tab, text="Tabla de Regímenes - Funcional", font=ctk.CTkFont(size=16))
        label.pack(expand=True)
    
    def _create_contratos_table(self):
        tab = self.tabview.tab(" Contratos")
        label = ctk.CTkLabel(tab, text="Tabla de Contratos - Funcional", font=ctk.CTkFont(size=16))
        label.pack(expand=True)
