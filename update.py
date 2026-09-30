import base64
import urllib.parse
import urllib.request

# Рабочие и регулярно обновляемые источники узлов
SOURCES = [
    "https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/top.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/V2Ray-Config-By-EbraSha-All-Type.txt",
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
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
    """Скачивание и извлечение V2Ray/VLESS/VMess/Trojan конфигураций"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()

            # Если подписка полностью зашифрована в Base64
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
    """Замена оригинального имени узла на isyzan vpn #N"""
    try:
        # Отрезаем старый хэштег с именем
        base = node_str.split("#")[0] if "#" in node_str else node_str
        new_name = urllib.parse.quote(f"{OUTPUT_NAME} #{index}")
        return f"{base}#{new_name}"
    except Exception:
        return node_str


def main():
    raw_nodes = []
    for src in SOURCES:
        nodes = fetch_nodes(src)
        print(f"Загружено из {src}: {len(nodes)} узлов")
        raw_nodes.extend(nodes)

    # Удаляем дубликаты
    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего уникальных серверов: {len(unique_nodes)}")

    if not unique_nodes:
        print("Внимание: Ни один источник не вернул узлы.")
        return

    working_nodes = []
    # Берём первые 150 серверов и переименовываем
    for i, node in enumerate(unique_nodes[:150], 1):
        working_nodes.append(rename_node(node, i))

    result_text = "\n".join(working_nodes)

    # Сохраняем в sub.txt
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Сохраняем в sub_base64.txt (для приложений)
    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Успешно сохранено {len(working_nodes)} серверов isyzan vpn!")


if __name__ == "__main__":
    main()
    
