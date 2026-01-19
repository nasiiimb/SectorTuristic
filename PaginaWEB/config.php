<?php
/**
 * Configuración de la aplicación
 */

// URL base del WebService
define('API_BASE_URL', 'http://localhost:3000/api');

// Configuración de la sesión
ini_set('session.cookie_httponly', 1);
ini_set('session.use_only_cookies', 1);
session_start();

/**
 * Función para hacer peticiones HTTP al WebService
 */
function apiRequest($endpoint, $method = 'GET', $data = null) {
    $url = API_BASE_URL . $endpoint;
    
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    
    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Content-Length: ' . strlen(json_encode($data)),
            'x-source: Pagina Web'
        ]);
    } elseif ($method === 'PUT') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Content-Length: ' . strlen(json_encode($data)),
            'x-source: Pagina Web'
        ]);
    } elseif ($method === 'DELETE') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
    }
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    // Debug: Log request details
    error_log("API Request: $method $url");
    if ($data) {
        error_log("Request Data: " . json_encode($data));
    }
    error_log("Response Code: $httpCode");
    error_log("Response: " . substr($response, 0, 500));
    
    if ($response === false) {
        $error = curl_error($ch);
        error_log("cURL Error: $error");
        return ['success' => false, 'error' => 'Error de conexión con el servidor: ' . $error];
    }
    
    $result = json_decode($response, true);
    
    return [
        'success' => $httpCode >= 200 && $httpCode < 300,
        'data' => $result,
        'httpCode' => $httpCode,
        'raw_response' => $response // Para debug
    ];
}

/**
 * Función para verificar si el usuario está logueado
 */
function isLoggedIn() {
    return isset($_SESSION['user']);
}

/**
 * Función para obtener el usuario actual
 */
function getCurrentUser() {
    return $_SESSION['user'] ?? null;
}

/**
 * Función para hacer logout
 */
function logout() {
    session_destroy();
    header('Location: index.php');
    exit;
}

/**
 * Función para escapar HTML (seguridad)
 */
function e($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

/**
 * Función para formatear fechas
 */
function formatDate($date) {
    return date('d/m/Y', strtotime($date));
}

/**
 * Función para formatear precios
 */
function formatPrice($price) {
    return number_format($price, 2, ',', '.') . ' €';
}

/**
 * Función para calcular noches entre dos fechas
 */
function calculateNights($checkIn, $checkOut) {
    $date1 = new DateTime($checkIn);
    $date2 = new DateTime($checkOut);
    $diff = $date1->diff($date2);
    return $diff->days;
}
?>
