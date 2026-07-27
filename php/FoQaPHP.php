<?php
/**
 * 调用 DeepSeek API，问"什么是无我"，打印返回的 JSON 中 content 字段。
 * 运行前需设置环境变量：DEEPSEEK_API_KEY=你的key
 * 运行方式：php FoQaPHP.php
 */

$apiKey = getenv('DEEPSEEK_API_KEY');
if (!$apiKey) {
    echo "请先设置环境变量 DEEPSEEK_API_KEY\n";
    exit(1);
}

$data = [
    'model' => 'deepseek-v4-flash',
    'messages' => [
        ['role' => 'user', 'content' => '什么是无我']
    ],
    'stream' => false
];

$ch = curl_init('https://api.deepseek.com/chat/completions');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($data),
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $apiKey
    ],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 60,
    CURLOPT_SSL_VERIFYPEER => false
]);

$response = curl_exec($ch);

if ($response === false) {
    echo "cURL 错误：" . curl_error($ch) . "\n";
    curl_close($ch);
    exit(1);
}

curl_close($ch);

$json = json_decode($response, true);

if (isset($json['error'])) {
    echo "API 返回错误：" . $json['error']['message'] . "\n";
    exit(1);
}

echo $json['choices'][0]['message']['content'] . "\n";
