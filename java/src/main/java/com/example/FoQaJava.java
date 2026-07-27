package com.example;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;

/**
 * 调用 DeepSeek API，问"什么是无我"，打印返回 JSON 中 content 字段。
 * 运行前需设置环境变量：DEEPSEEK_API_KEY=你的key
 */
public class FoQaJava {

    private static final String API_URL = "https://api.deepseek.com/chat/completions";
    private static final String API_KEY = System.getenv("DEEPSEEK_API_KEY");
    private static final Gson GSON = new Gson();

    public static void main(String[] args) throws Exception {
        if (API_KEY == null || API_KEY.isBlank()) {
            System.out.println("请先设置环境变量 DEEPSEEK_API_KEY");
            return;
        }

        // 构建请求体
        Map<String, Object> requestBody = Map.of(
                "model", "deepseek-v4-flash",
                "messages", List.of(
                        Map.of("role", "user", "content", "什么是无我")
                ),
                "stream", false
        );

        HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(60))
                .build();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + API_KEY)
                .POST(HttpRequest.BodyPublishers.ofString(GSON.toJson(requestBody)))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        String responseBody = response.body();

        // 用 Gson 解析 JSON，提取 choices[0].message.content
        JsonObject json = GSON.fromJson(responseBody, JsonObject.class);

        // 检查错误
        if (json.has("error")) {
            JsonObject error = json.getAsJsonObject("error");
            System.out.println("API 返回错误：" + error.get("message").getAsString());
            return;
        }

        String content = json
                .getAsJsonArray("choices")
                .get(0).getAsJsonObject()
                .getAsJsonObject("message")
                .get("content").getAsString();

        System.out.println(content);
    }
}
