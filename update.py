import base64
import urllib.parse
import requests

# Проверенные сверхбольшие агрегаторы подписок
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/base64",
    "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber/main/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/v2rayng-sub/v2ray/main/v2ray.txt",
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
]

OUTPUT_NAME = "isyzan vpn"


def decode_base64_safe(data_str):
    try:
        data_str = data_str.strip().replace("\r", "").replace("\n", "")
        padded = data_str + "=" * (-len(data_str) % 4)
        return base64.b64decode(padded).decode("utf-8", errors="ignore")
    except Exception:
        return data_str


def fetch_nodes(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Ошибка {response.status_code} для {url}")
            return []

        content = response.text.strip()
        decoded = decode_base64_safe(content)

        if any(
            proto in decoded
            for proto in [
                "vless://",
                "vmess://",
                "trojan://",
                "ss://",
                "hysteria2://",
            ]
        ):
            content = decoded

        lines = content.splitlines()
        valid_lines = [
            line.strip()
            for line in lines
            if any(
                line.strip().startswith(p)
                for p in [
                    "vless://",
                    "vmess://",
                    "trojan://",
                    "ss://",
                    "ssr://",
                    "hysteria2://",
                    "tuic://",
                ]
            )
        ]
        return valid_lines
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return []


def rename_node(node_str, index):
    try:
        base = node_str.split("#")[0] if "#" in node_str else node_str
        new_name = urllib.parse.quote(f"{OUTPUT_NAME} #{index}")
        return f"{base}#{new_name}"
    except Exception:
        return node_str


def main():
    raw_nodes = []
    for src in SOURCES:
        nodes = fetch_nodes(src)
        print(f"Успешно получено из {src}: {len(nodes)} узлов")
        raw_nodes.extend(nodes)

    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего уникальных серверов: {len(unique_nodes)}")

    if not unique_nodes:
        print("Не удалось извлечь узлы из подписок.")
        return

    working_nodes = []
    # Сохраняем первые 100 серверов
    for i, node in enumerate(unique_nodes[:100], 1):
        working_nodes.append(rename_node(node, i))

    result_text = "\n".join(working_nodes)

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Успешно сохранено {len(working_nodes)} серверов.")


if __name__ == "__main__":
    main()
    
