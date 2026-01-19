<?php
/**
 * API Endpoint para peticiones AJAX
 */
require_once 'config.php';

header('Content-Type: application/json');

$action = $_GET['action'] ?? '';

switch ($action) {
    case 'paises':
        // Obtener lista de países únicos
        $response = apiRequest('/ciudades');
        if ($response['success']) {
            $ciudades = $response['data'];
            $paises = array_unique(array_column($ciudades, 'pais'));
            sort($paises);
            echo json_encode(['success' => true, 'data' => $paises]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Error al obtener países']);
        }
        break;
        
    case 'ciudades':
        // Obtener ciudades de un país
        $pais = $_GET['pais'] ?? '';
        $response = apiRequest('/ciudades');
        if ($response['success']) {
            $ciudades = $response['data'];
            $ciudadesFiltradas = array_filter($ciudades, function($c) use ($pais) {
                return $c['pais'] === $pais;
            });
            echo json_encode(['success' => true, 'data' => array_values($ciudadesFiltradas)]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Error al obtener ciudades']);
        }
        break;
        
    case 'hoteles':
        // Obtener hoteles de una ciudad
        $ciudad = $_GET['ciudad'] ?? '';
        $response = apiRequest('/hoteles');
        if ($response['success']) {
            $hoteles = $response['data'];
            $hotelesFiltrados = array_filter($hoteles, function($h) use ($ciudad) {
                return isset($h['ciudad']) && $h['ciudad']['nombre'] === $ciudad;
            });
            echo json_encode(['success' => true, 'data' => array_values($hotelesFiltrados)]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Error al obtener hoteles']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Acción no válida']);
        break;
}
