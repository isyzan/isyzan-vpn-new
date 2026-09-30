import base64
import os
import re
import urllib.parse
import urllib.request

# Рабочие публичные источники (зеркала и direct-ссылки)
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
    "https://raw.githubusercontent.com/mosec-org/Nodes/main/v2ray",
    "https://raw.githubusercontent.com/Eslabond/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/vysecurity/v2ray/main/v2ray",
    "https://raw.githubusercontent.com/snakemcdonald/v2ray-nodes/main/nodes.txt",
    "https://raw.githubusercontent.com/peassfull/v2ray-free/main/v2ray.txt",
    "https://raw.githubusercontent.com/Pawroid/Free-Servers/main/sub.txt",
]

OUTPUT_NAME = "isyzan vpn"


def decode_base64_safe(data_str):
    """Надежное декодирование Base64 с исправлением длины строки"""
    try:
        data_str = data_str.strip().replace("\r", "").replace("\n", "")
        padded = data_str + "=" * (-len(data_str) % 4)
        return base64.b64decode(padded).decode("utf-8", errors="ignore")
    except Exception:
        return data_str


def fetch_nodes(url):
    """Загрузка конфигураций с обработкой двойного Base64"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()

            # Пробуем декодировать содержимое
            decoded = decode_base64_safe(content)
            if any(
                proto in decoded
                for proto in ["vless://", "vmess://", "trojan://", "ss://"]
            ):
                content = decoded

            lines = content.splitlines()
            valid_lines = []

            for line in lines:
                line = line.strip()
                # Проверка на прямое соответствие протоколам
                if any(
                    line.startswith(p)
                    for p in ["vless://", "vmess://", "trojan://", "ss://", "ssr://"]
                ):
                    valid_lines.append(line)

            return valid_lines
    except Exception as e:
        print(f"Ошибка загрузки источника {url}: {e}")
        return []


def rename_node(node_str, index):
    """Переименование узла под имя isyzan vpn"""
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
        print(f"Из {src} успешно загружено: {len(nodes)} узлов")
        raw_nodes.extend(nodes)

    # Удаление дубликатов с сохранением порядка
    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего найдено уникальных серверов: {len(unique_nodes)}")

    if not unique_nodes:
        print("Внимание: Ни один источник не ответил. Файл не будет перезаписан.")
        return

    working_nodes = []
    # Берем до 200 рабочих серверов
    for i, node in enumerate(unique_nodes[:200], 1):
        working_nodes.append(rename_node(node, i))

    result_text = "\n".join(working_nodes)

    # Сохраняем текстовую версию
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Сохраняем Base64 версию для VPN-клиентов
    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Успешно обновлено и сохранено {len(working_nodes)} серверов!")


if __name__ == "__main__":
    main()
    
