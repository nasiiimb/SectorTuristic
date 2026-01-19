"""
API Client - Comunicación HTTP con el WebService
Principio de Responsabilidad Única: Solo maneja comunicación HTTP
"""
import requests
from typing import Dict, Any, Optional
from .config import Config


class APIResponse:
    """Value Object que encapsula la respuesta de la API"""
    
    def __init__(self, success: bool, data: Any = None, error: Any = None, status_code: int = 200):
        self.success = success
        self.data = data
        self.error = error
        self.status_code = status_code
    
    def __bool__(self) -> bool:
        return self.success
    
    def __repr__(self) -> str:
        return f"APIResponse(success={self.success}, status={self.status_code})"


class APIClient:
    """
    Cliente HTTP para comunicación con el WebService.
    Implementa el patrón Adapter para abstraer la librería requests.
    """
    
    def __init__(self, config: Config):
        """
        Inyección de dependencias: recibe la configuración
        """
        self._config = config
        self._base_url = config.api_base_url
        self._timeout = config.request_timeout
    
    def _build_url(self, endpoint: str) -> str:
        """Construye la URL completa"""
        return f"{self._base_url}/{endpoint.lstrip('/')}"
    
    def _handle_response(self, response: requests.Response) -> APIResponse:
        """
        Maneja la respuesta HTTP y convierte errores.
        Principio de Inversión de Dependencias: retorna APIResponse, no Response de requests.
        """
        try:
            response.raise_for_status()
            data = response.json() if response.text else None
            return APIResponse(success=True, data=data, status_code=response.status_code)
        except requests.exceptions.HTTPError as e:
            error_data = {}
            try:
                error_data = response.json()
            except:
                error_data = {"error": str(e)}
            return APIResponse(
                success=False,
                error=error_data,
                status_code=response.status_code
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> APIResponse:
        """
        Realiza una petición GET.
        
        Args:
            endpoint: Ruta del endpoint (ej: "clientes" o "/clientes/1")
            params: Parámetros de query string
            
        Returns:
            APIResponse con el resultado
        """
        try:
            url = self._build_url(endpoint)
            response = requests.get(url, params=params, timeout=self._timeout)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                error="No se pudo conectar al WebService. ¿Está ejecutándose?"
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def post(self, endpoint: str, data: Dict) -> APIResponse:
        """
        Realiza una petición POST.
        
        Args:
            endpoint: Ruta del endpoint
            data: Datos a enviar en el body (se convierte a JSON)
            
        Returns:
            APIResponse con el resultado
        """
        try:
            url = self._build_url(endpoint)
            headers = {'x-source': 'PMS'}
            response = requests.post(url, json=data, headers=headers, timeout=self._timeout)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                error="No se pudo conectar al WebService. ¿Está ejecutándose?"
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> APIResponse:
        """
        Realiza una petición PUT.
        
        Args:
            endpoint: Ruta del endpoint
            data: Datos a enviar (opcional para algunos endpoints)
            
        Returns:
            APIResponse con el resultado
        """
        try:
            url = self._build_url(endpoint)
            kwargs = {"timeout": self._timeout}
            if data is not None:
                kwargs["json"] = data
            response = requests.put(url, **kwargs)
            return self._handle_response(response)
        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                error="No se pudo conectar al WebService. ¿Está ejecutándose?"
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def delete(self, endpoint: str) -> APIResponse:
        """
        Realiza una petición DELETE.
        
        Args:
            endpoint: Ruta del endpoint
            
        Returns:
            APIResponse con el resultado
        """
        try:
            url = self._build_url(endpoint)
            response = requests.delete(url, timeout=self._timeout)
            return APIResponse(success=True, status_code=response.status_code)
        except requests.exceptions.HTTPError as e:
            return APIResponse(success=False, error=str(e), status_code=response.status_code)
        except requests.exceptions.ConnectionError:
            return APIResponse(
                success=False,
                error="No se pudo conectar al WebService. ¿Está ejecutándose?"
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con el WebService.
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        response = self.get("hoteles")
        return response.success
