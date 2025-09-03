<?php
// הגדרת כותרת לתגובה מסוג JSON
header('Content-Type: application/json');

// רק בקשת POST מותרת
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["error" => "Only POST allowed"]);
    exit;
}

// בדיקת פרמטרים
$key = $_GET['key'] ?? null;
$apiKey = $_GET['api_key'] ?? null;

if (!$key || !$apiKey) {
    http_response_code(400);
    echo json_encode(["error" => "Missing 'key' or 'api_key' in URL"]);
    exit;
}

// אימות מפתח API (אפשר גם להגדיר אותו כאן קבוע אם אין ENV)
$expectedKey = "your-secret-api-key"; // ← תחליפי למפתח שלך
if ($apiKey !== $expectedKey) {
    http_response_code(403);
    echo json_encode(["error" => "Invalid API key"]);
    exit;
}

// קריאת גוף הבקשה
$raw = file_get_contents("php://input");
$data = json_decode($raw, true);

if ($data === null) {
    http_response_code(400);
    echo json_encode(["error" => "Invalid JSON"]);
    exit;
}

// שמירה לקובץ
$filename = basename($key) . ".json";  // להימנע משמות בעייתיים
if (file_put_contents($filename, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE))) {
    echo json_encode(["ok" => true, "saved" => $filename]);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Failed to write file"]);
}
?>
