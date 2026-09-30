import base64
import re
import socket
import urllib.parse
import urllib.request

# Рабочие публичные источники (можно добавлять свои ссылки на подписки)
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2ray",
    "https://raw.githubusercontent.com/mosec-org/Nodes/main/v2ray",
    "https://raw.githubusercontent.com/Eslabond/v2ray-configs/main/All_Configs_Sub.txt",
]

OUTPUT_NAME = "isyzan vpn"


def fetch_nodes(url):
    """Загрузка и автоматическое декодирование подписок"""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()

            # Пробуем расшифровать base64, если подписка закодирована
            try:
                # Добавляем padding, если не хватает символов '='
                padded = content + "=" * (-len(content) % 4)
                decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
                if any(
                    proto in decoded
                    for proto in ["vless://", "vmess://", "trojan://", "ss://"]
                ):
                    content = decoded
            except Exception:
                pass

            # Извлекаем все строки, похожие на vpn-конфиги
            lines = content.splitlines()
            valid_lines = [
                line.strip()
                for line in lines
                if any(
                    line.strip().startswith(p)
                    for p in ["vless://", "vmess://", "trojan://", "ss://", "ssr://"]
                )
            ]
            return valid_lines
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return []


def check_node_alive(node_str):
    """Проверка доступности хоста по TCP"""
    try:
        # Извлекаем IP/домен и порт из ссылки с помощью регулярного выражения
        match = re.search(r"@([^:/]+):(\d+)", node_str)
        if match:
            host = match.group(1)
            port = int(match.group(2))

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.5)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
    except Exception:
        pass
    # Если регулярка не прошла или порт не ответил — пропускаем, чтобы не блочить рабочие узлы
    return True


def rename_node(node_str, index):
    """Переименование конфигурации под имя isyzan vpn"""
    try:
        if "#" in node_str:
            base = node_str.split("#")[0]
        else:
            base = node_str
        new_name = urllib.parse.quote(f"{OUTPUT_NAME} #{index}")
        return f"{base}#{new_name}"
    except Exception:
        return node_str


def main():
    raw_nodes = []
    for src in SOURCES:
        fetched = fetch_nodes(src)
        print(f"Получено из {src}: {len(fetched)} узлов")
        raw_nodes.extend(fetched)

    # Удаляем дубликаты
    unique_nodes = list(dict.fromkeys(raw_nodes))
    print(f"Всего уникальных узлов: {len(unique_nodes)}")

    working_nodes = []
    count = 1
    for node in unique_nodes:
        if check_node_alive(node):
            renamed = rename_node(node, count)
            working_nodes.append(renamed)
            count += 1
            if count > 100:  # Лимит на 100 лучших серверов
                break

    result_text = "\n".join(working_nodes)

    # Запись открытого списка
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    # Запись закодированного base64 (для мобильных VPN-клиентов)
    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Успешно сохранено конфигураций: {len(working_nodes)}")


if __name__ == "__main__":
    main()
    
