import base64
import urllib.parse
import urllib.request

# Крупные и надежные агрегаторы с сотнями рабочих конфигураций
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/xray/base64",
    "https://raw.githubusercontent.com/Lクリ/v2ray-share/main/v2ray",
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
    "https://raw.githubusercontent.com/mosec-org/Nodes/main/v2ray",
    "https://raw.githubusercontent.com/Pawroid/Free-Servers/main/sub.txt",
    "https://raw.githubusercontent.com/Eslabond/v2ray-configs/main/All_Configs_Sub.txt",
]

OUTPUT_NAME = "isyzan vpn"


def decode_base64_safe(data_str):
    """Надежное декодирование Base64 с исправлением длины"""
    try:
        data_str = data_str.strip().replace("\r", "").replace("\n", "")
        padded = data_str + "=" * (-len(data_str) % 4)
        return base64.b64decode(padded).decode("utf-8", errors="ignore")
    except Exception:
        return data_str


def fetch_nodes(url):
    """Скачивание с продвинутой маскировкой под браузер"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()

            # Попытка декодировать Base64
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
            valid_lines = []

            for line in lines:
                line = line.strip()
                if any(
                    line.startswith(p)
                    for p in [
                        "vless://",
                        "vmess://",
                        "trojan://",
                        "ss://",
                        "ssr://",
                        "hysteria2://",
                        "tuic://",
                    ]
                ):
                    valid_lines.append(line)

            return valid_lines
    except Exception as e:
        print(f"Ошибка при чтении {url}: {e}")
        return []


def rename_node(node_str, index):
    """Присвоение имени isyzan vpn #N"""
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
        print(f"Загружено из {src}: {len(nodes)} серверов")
        raw_nodes.extend(nodes)

    # Удаление дубликатов
    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего уникальных узлов найдено: {len(unique_nodes)}")

    if not unique_nodes:
        print("Не удалось загрузить сервера.")
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

    print(f"Успешно сгенерировано и сохранено {len(working_nodes)} серверов!")


if __name__ == "__main__":
    main()
    
