"""
HuespedesDialog - Diálogo para gestionar huéspedes de una reserva
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict


class HuespedesDialog(ctk.CTkToplevel):
    """Diálogo modal para añadir huéspedes a una reserva"""
    
    def __init__(self, parent, capacidad_max: int, nombre_habitacion: str):
        super().__init__(parent)
        
        self.capacidad_max = capacidad_max
        self.nombre_habitacion = nombre_habitacion
        self.huespedes: List[Dict] = []
        self.result = None
        
        # Configurar ventana con tamaño más razonable
        self.title("Gestionar Huéspedes")
        self.geometry("700x650")
        self.resizable(False, False)
        
        # Hacer que la ventana aparezca al frente
        self.lift()
        self.focus_force()
        
        # Configurar como modal después de que la ventana esté visible
        self.after(10, lambda: self._configure_modal(parent))
        
        # Centrar en la pantalla
        self.update_idletasks()
        width = 700
        height = 650
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"700x650+{x}+{y}")
        
        self._create_ui()
    
    def _configure_modal(self, parent):
        """Configura el diálogo como modal después de que esté visible"""
        try:
            self.transient(parent)
            self.grab_set()
        except:
            pass  # Ignorar errores de configuración modal
        
    def _create_ui(self):
        """Crea la interfaz del diálogo - ESTRUCTURA SIMPLE"""
        
        # ============= BOTONES AL FINAL - PRIMERO =============
        # Los creo PRIMERO y los pongo ABAJO para que SIEMPRE estén visibles
        button_container = ctk.CTkFrame(self, fg_color="transparent", height=80)
        button_container.pack(side="bottom", fill="x", padx=20, pady=20)
        
        btn_cancelar = ctk.CTkButton(
            button_container,
            text="❌ CANCELAR",
            command=self._cancelar,
            height=50,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#A93226", "#7B1F1F"),
            hover_color=("#C0392B", "#922B21")
        )
        btn_cancelar.pack(side="left", padx=20, expand=True)
        
        btn_aceptar = ctk.CTkButton(
            button_container,
            text="✅ ACEPTAR Y HACER CHECK-IN",
            command=self._aceptar,
            height=50,
            width=300,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#148F77", "#0E6655"),
            hover_color=("#16A085", "#117A65")
        )
        btn_aceptar.pack(side="right", padx=20, expand=True)
        
        # ============= CONTENIDO ARRIBA =============
        content_frame = ctk.CTkScrollableFrame(self)
        content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(20, 0))
        
        # Título
        title = ctk.CTkLabel(
            content_frame,
            text=f"👥 Gestionar Huéspedes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 10))
        
        # Información de capacidad
        info_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=f"📍 Habitación: {self.nombre_habitacion}\n"
                 f"👤 Capacidad máxima: {self.capacidad_max} persona(s)\n"
                 f"ℹ️  El cliente que paga cuenta como 1 huésped",
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        info_label.pack(padx=15, pady=15)
        
        # Frame del formulario
        form_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        form_frame.pack(fill="x", pady=(0, 15))
        
        # Nombre
        nombre_label = ctk.CTkLabel(form_frame, text="Nombre:", font=ctk.CTkFont(size=13))
        nombre_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.nombre_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Nombre del huésped",
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.nombre_entry.pack(fill="x", padx=20, pady=(0, 8))
        
        # Apellidos
        apellidos_label = ctk.CTkLabel(form_frame, text="Apellidos:", font=ctk.CTkFont(size=13))
        apellidos_label.pack(anchor="w", padx=20, pady=(3, 0))
        
        self.apellidos_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Apellidos del huésped",
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.apellidos_entry.pack(fill="x", padx=20, pady=(0, 8))
        
        # Email
        email_label = ctk.CTkLabel(form_frame, text="Correo Electrónico:", font=ctk.CTkFont(size=13))
        email_label.pack(anchor="w", padx=20, pady=(3, 0))
        
        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="email@ejemplo.com",
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.email_entry.pack(fill="x", padx=20, pady=(0, 8))
        
        # DNI
        dni_label = ctk.CTkLabel(form_frame, text="DNI:", font=ctk.CTkFont(size=13))
        dni_label.pack(anchor="w", padx=20, pady=(3, 0))
        
        self.dni_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="12345678A",
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.dni_entry.pack(fill="x", padx=20, pady=(0, 8))
        
        # Botón añadir
        btn_añadir = ctk.CTkButton(
            form_frame,
            text="➕ Añadir Huésped",
            command=self._añadir_huesped,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#2B7A78", "#14443F"),
            hover_color=("#3D9970", "#2A7A5E")
        )
        btn_añadir.pack(fill="x", padx=20, pady=(5, 15))
        
        # Lista de huéspedes
        lista_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        lista_frame.pack(fill="x", pady=(0, 15))
        
        lista_title = ctk.CTkLabel(
            lista_frame,
            text="📋 Huéspedes Añadidos (0)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        lista_title.pack(pady=(10, 5))
        self.lista_title_label = lista_title
        
        # Scrollable frame para la lista con altura razonable
        self.lista_scroll = ctk.CTkScrollableFrame(lista_frame, height=150)
        self.lista_scroll.pack(fill="x", padx=10, pady=(0, 10))
        
    def _añadir_huesped(self):
        """Añade un huésped a la lista"""
        nombre = self.nombre_entry.get().strip()
        apellidos = self.apellidos_entry.get().strip()
        email = self.email_entry.get().strip()
        dni = self.dni_entry.get().strip()
        
        if not all([nombre, apellidos, email, dni]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        
        # Validar capacidad (+1 por el cliente que paga)
        if len(self.huespedes) + 1 >= self.capacidad_max:
            messagebox.showwarning(
                "Capacidad Excedida",
                f"La habitación solo tiene capacidad para {self.capacidad_max} persona(s).\n"
                f"Ya has añadido {len(self.huespedes)} huésped(es) + 1 cliente que paga = {len(self.huespedes) + 1}"
            )
            return
        
        # Validar DNI duplicado
        if any(h['DNI'] == dni for h in self.huespedes):
            messagebox.showwarning("DNI Duplicado", "Ya existe un huésped con ese DNI")
            return
        
        # Añadir huésped
        huesped = {
            'nombre': nombre,
            'apellidos': apellidos,
            'correoElectronico': email,
            'DNI': dni
        }
        self.huespedes.append(huesped)
        
        # Actualizar UI
        self._actualizar_lista()
        self._limpiar_formulario()
        
    def _actualizar_lista(self):
        """Actualiza la visualización de la lista de huéspedes"""
        # Limpiar lista
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
        
        # Actualizar título
        total = len(self.huespedes) + 1  # +1 por el cliente que paga
        self.lista_title_label.configure(
            text=f"📋 Huéspedes Añadidos ({len(self.huespedes)}) - Total: {total}/{self.capacidad_max}"
        )
        
        # Cliente que paga (info)
        cliente_frame = ctk.CTkFrame(self.lista_scroll, corner_radius=8, fg_color=("#E8F5E9", "#1B5E20"))
        cliente_frame.pack(fill="x", pady=2, padx=5)
        
        info_label = ctk.CTkLabel(
            cliente_frame,
            text="👤 Cliente que paga (se añade automáticamente)",
            font=ctk.CTkFont(size=11),
            text_color=("#2E7D32", "#A5D6A7")
        )
        info_label.pack(pady=8, padx=10)
        
        # Mostrar huéspedes
        for idx, huesped in enumerate(self.huespedes):
            huesped_frame = ctk.CTkFrame(self.lista_scroll, corner_radius=8)
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
                command=lambda i=idx: self._eliminar_huesped(i),
                fg_color=("#E74C3C", "#C0392B"),
                hover_color=("#C0392B", "#A93226")
            )
            btn_eliminar.pack(side="right", padx=5)
    
    def _eliminar_huesped(self, index: int):
        """Elimina un huésped de la lista"""
        if messagebox.askyesno("Confirmar", "¿Eliminar este huésped?"):
            del self.huespedes[index]
            self._actualizar_lista()
    
    def _limpiar_formulario(self):
        """Limpia los campos del formulario"""
        self.nombre_entry.delete(0, 'end')
        self.apellidos_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.dni_entry.delete(0, 'end')
    
    def _aceptar(self):
        """Acepta y cierra el diálogo"""
        self.result = self.huespedes
        self._cerrar_dialogo()
    
    def _cancelar(self):
        """Cancela y cierra el diálogo"""
        self.result = None
        self._cerrar_dialogo()
    
    def _cerrar_dialogo(self):
        """Cierra el diálogo de forma segura"""
        try:
            self.grab_release()
        except:
            pass
        
        # Restaurar foco a la ventana principal
        parent = self.master
        self.destroy()
        
        if parent:
            try:
                parent.lift()
                parent.focus_force()
                parent.update()
            except:
                pass
    
    def get_huespedes(self) -> List[Dict]:
        """Retorna la lista de huéspedes o None si se canceló"""
        self.wait_window()
        return self.result
