import base64
import os
import re
import urllib.request

# Рабочие публичные подписки
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
    "https://raw.githubusercontent.com/mosec-org/Nodes/main/v2ray",
    "https://raw.githubusercontent.com/Eslabond/v2ray-configs/main/All_Configs_Sub.txt",
]

OUTPUT_NAME = "isyzan vpn"


def fetch_nodes(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()

            # Декодирование Base64
            try:
                padded = content + "=" * (-len(content) % 4)
                decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
                if any(
                    proto in decoded
                    for proto in ["vless://", "vmess://", "trojan://", "ss://"]
                ):
                    content = decoded
            except Exception:
                pass

            lines = content.splitlines()
            valid_lines = [
                line.strip()
                for line in lines
                if any(
                    line.strip().startswith(p)
                    for p in ["vless://", "vmess://", "trojan://", "ss://"]
                )
            ]
            return valid_lines
    except Exception as e:
        print(f"Ошибка загрузки источника {url}: {e}")
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
        print(f"Из {src} получено серверов: {len(nodes)}")
        raw_nodes.extend(nodes)

    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего уникальных серверов: {len(unique_nodes)}")

    if not unique_nodes:
        # Если ничего не удалось загрузить, создаём тестовую запись для проверки появления файла
        unique_nodes = [
            "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443#isyzan%20vpn%20Test"
        ]

    working_nodes = []
    for i, node in enumerate(unique_nodes[:100], 1):
        working_nodes.append(rename_node(node, i))

    result_text = "\n".join(working_nodes)

    # Запись текстового файла
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Запись Base64 файла
    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print("Файлы sub.txt и sub_base64.txt успешно сформированы на диске.")


if __name__ == "__main__":
    main()
    
