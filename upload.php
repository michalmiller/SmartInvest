<?php
// Simple upload handler for JSON via POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["error" => "Only POST allowed"]);
    exit;
}

if (!isset($_GET['key']) || !isset($_GET['api_key'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing key or api_key"]);
    exit;
}

// Validate API key (optional)
$expected_key = getenv("SOMEE_API_KEY"); // You can hardcode if needed
if ($_GET['api_key'] !== $expected_key) {
    http_response_code(403);
    echo json_encode(["error" => "Invalid API key"]);
    exit;
}

$raw = file_get_contents("php://input");
$data = json_decode($raw, true);
if ($data === null) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid JSON"]);
    exit;
}

$file = $_GET['ke";
file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

echo json_encode(["ok" => true, "saved" => $file]);
?>
