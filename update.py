import base64
import urllib.parse
import urllib.request

# Расширенный список проверенных публичных источников
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
    "https://raw.githubusercontent.com/mosec-org/Nodes/main/v2ray",
    "https://raw.githubusercontent.com/Eslabond/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Pawroid/Free-Servers/main/sub.txt",
    "https://raw.githubusercontent.com/ssrsub/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
]

OUTPUT_NAME = "isyzan vpn"


def decode_base64_safe(data_str):
    """Безопасное декодирование строк Base64"""
    try:
        data_str = data_str.strip().replace("\r", "").replace("\n", "")
        padded = data_str + "=" * (-len(data_str) % 4)
        return base64.b64decode(padded).decode("utf-8", errors="ignore")
    except Exception:
        return data_str


def fetch_nodes(url):
    """Скачивание и обработка конфигураций"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()

            # Декодирование, если файл целиком в Base64
            decoded = decode_base64_safe(content)
            if any(
                proto in decoded
                for proto in [
                    "vless://",
                    "vmess://",
                    "trojan://",
                    "ss://",
                    "hysteria2://",
                    "tuic://",
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
        print(f"Ошибка загрузки из {url}: {e}")
        return []


def rename_node(node_str, index):
    """Переименование узла в isyzan vpn #N"""
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

    # Удаляем дубликаты
    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего найденных уникальных серверов: {len(unique_nodes)}")

    if not unique_nodes:
        print("Внимание: Источники не ответили.")
        return

    working_nodes = []
    # Сохраняем первые 100 рабочих серверов
    for i, node in enumerate(unique_nodes[:100], 1):
        working_nodes.append(rename_node(node, i))

    result_text = "\n".join(working_nodes)

    # Запись текстового файла
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Запись Base64 версии
    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Готово! Сохранено {len(working_nodes)} серверов в подписку.")


if __name__ == "__main__":
    main()
    
