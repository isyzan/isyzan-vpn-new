import base64
import os
import urllib.parse


def decode_base64_safe(data_str):
    try:
        data_str = data_str.strip().replace("\r", "").replace("\n", "")
        padded = data_str + "=" * (-len(data_str) % 4)
        return base64.b64decode(padded).decode("utf-8", errors="ignore")
    except Exception:
        return data_str


def parse_and_clean():
    if not os.path.exists("raw_nodes.txt"):
        print("Файл raw_nodes.txt не найден!")
        return []

    with open("raw_nodes.txt", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()

    # Попытка декодировать Base64 целиком
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
    valid_nodes = []

    for line in lines:
        line = line.strip()
        # Извлекаем закодированные строки внутри текстовых блоков если они есть
        if (
            not line.startswith("vless://")
            and not line.startswith("vmess://")
            and not line.startswith("trojan://")
        ):
            decoded_line = decode_base64_safe(line)
            if any(
                p in decoded_line
                for p in ["vless://", "vmess://", "trojan://", "ss://"]
            ):
                for sub_line in decoded_line.splitlines():
                    if any(
                        sub_line.strip().startswith(p)
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
                        valid_nodes.append(sub_line.strip())
                continue

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
            valid_nodes.append(line)

    # Удаляем дубликаты
    return list(dict.fromkeys(valid_nodes))


def rename_node(node_str, index):
    try:
        base = node_str.split("#")[0] if "#" in node_str else node_str
        new_name = urllib.parse.quote(f"isyzan vpn #{index}")
        return f"{base}#{new_name}"
    except Exception:
        return node_str


def main():
    nodes = parse_and_clean()
    print(f"Всего извлечено и расшифровано серверов: {len(nodes)}")

    if not nodes:
        print("Внимание: Не удалось извлечь серверы!")
        return

    working_nodes = []
    # Сохраняем первые 100 серверов
    for i, node in enumerate(nodes[:100], 1):
        working_nodes.append(rename_node(node, i))

    result_text = "\n".join(working_nodes)

    # Запись в sub.txt
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Запись в sub_base64.txt
    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Успешно сгенерирована подписка с {len(working_nodes)} серверами!")


if __name__ == "__main__":
    main()
    
