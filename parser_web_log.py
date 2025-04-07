import argparse
import os
import json
import re
from collections import Counter


def parse_log_line(line):
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) \S+ \S+ \[(?P<date>.*?)] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\S+) "(?P<referer>.*?)" "(?P<user_agent>.*?)" (?P<duration>\d+)'
    )
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    else:
        return None


def process_log_file(file_path):
    total_requests = 0
    method_counter = Counter()
    ip_counter = Counter()
    top_longest = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parsed = parse_log_line(line)
            if parsed:
                total_requests += 1
                method = parsed["request"].split()[0]
                method_counter[method] += 1
                ip_counter[parsed["ip"]] += 1
                duration = int(parsed["duration"])
                if len(top_longest) < 3:
                    top_longest.append(
                        {
                            "ip": parsed["ip"],
                            "date": parsed["date"],
                            "method": method,
                            "url": parsed["request"].split()[1],
                            "duration": duration,
                        }
                    )
                    top_longest.sort(key=lambda x: x["duration"], reverse=True)
                else:
                    if duration > top_longest[-1]["duration"]:
                        top_longest.append(
                            {
                                "ip": parsed["ip"],
                                "date": parsed["date"],
                                "method": method,
                                "url": parsed["request"].split()[1],
                                "duration": duration,
                            }
                        )
                        top_longest.sort(key=lambda x: x["duration"], reverse=True)
                        top_longest.pop()

    top_ips = ip_counter.most_common(3)

    result = {
        "top_ips": {ip: count for ip, count in top_ips},
        "top_longest": top_longest,
        "total_stat": dict(method_counter),
        "total_requests": total_requests,
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Анализатор лог-файлов access.log")
    parser.add_argument(
        "path", type=str, help="Путь к директории с лог-файлами или к конкретному файлу"
    )
    args = parser.parse_args()

    path = args.path

    if os.path.isdir(path):
        log_files = [
            os.path.join(path, f) for f in os.listdir(path) if f.endswith(".log")
        ]
    elif os.path.isfile(path):
        log_files = [path]
    else:
        print("Указанный путь не является ни файлом, ни директорией")
        return

    for log_file in log_files:
        print(f"Обработка файла: {log_file}")
        result = process_log_file(log_file)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        base_name = os.path.basename(log_file)
        json_file_name = f"{base_name}.json"
        with open(json_file_name, "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)
        print(f"Результаты сохранены в файл: {json_file_name}\n")


if __name__ == "__main__":
    main()
