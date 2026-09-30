import base64
import socket
import urllib.parse
import urllib.request

# Список исходных подписок (подставьте свои ссылки)
SOURCES = [
    "https://example.com/sub1",
    "https://example.com/sub2",
]

OUTPUT_NAME = "isyzan vpn"


def fetch_nodes(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore").strip()
            # Пробуем декодировать base64, если подписка зашифрована
            try:
                content = base64.b64decode(content).decode("utf-8", errors="ignore")
            except Exception:
                pass
            return [line.strip() for line in content.splitlines() if line.strip()]
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return []


def check_node_alive(node_str):
    """Базовая проверка доступности хоста по TCP"""
    try:
        if node_str.startswith("vless://") or node_str.startswith("vmess://"):
            # Извлечение хоста и порта из URI
            parsed = urllib.parse.urlparse(node_str)
            netloc = parsed.netloc
            if "@" in netloc:
                netloc = netloc.split("@")[-1]
            if ":" in netloc:
                host, port = netloc.split(":")
                port = int(port.split("?")[0])
            else:
                host = netloc
                port = 443

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3.0)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
    except Exception:
        pass
    return False


def rename_node(node_str, index):
    """Переименование узла в формат isyzan vpn #N"""
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
        raw_nodes.extend(fetch_nodes(src))

    # Удаляем дубликаты
    unique_nodes = list(dict.fromkeys(raw_nodes))

    working_nodes = []
    count = 1
    for node in unique_nodes:
        if check_node_alive(node):
            renamed = rename_node(node, count)
            working_nodes.append(renamed)
            count += 1

    # Запись текстового списка и base64 версии
    result_text = "\n".join(working_nodes)
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    b64_content = base64.b64encode(result_text.encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64_content)

    print(f"Сохранено рабочих узлов: {len(working_nodes)}")


if __name__ == "__main__":
    main()
