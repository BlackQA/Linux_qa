import subprocess
from datetime import datetime


def get_system_report():
    try:

        result = subprocess.run(
            ["ps", "aux"], stdout=subprocess.PIPE, text=True, check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды ps aux: {e}")
        return

    users = set()
    process_count = 0
    memory_usage = 0.0
    cpu_usage = 0.0
    memory_usage_per_process = {}
    cpu_usage_per_process = {}

    for line in output.splitlines():
        if line.startswith('USER'):
            continue
        parts = line.split()
        if len(parts) < 11:
            continue
        user = parts[0]
        cpu_str = parts[2].replace(',', '.')
        mem_str = parts[3].replace(',', '.')
        try:
            cpu = float(cpu_str)
            mem = float(mem_str)
        except ValueError as e:
            print(f"Ошибка преобразования числа: {e}")
            continue

        users.add(user)
        process_count += 1
        memory_usage += mem
        cpu_usage += cpu

        if user in memory_usage_per_process:
            memory_usage_per_process[user] += mem
            cpu_usage_per_process[user] += cpu
        else:
            memory_usage_per_process[user] = mem
            cpu_usage_per_process[user] = cpu

    max_memory_user = max(memory_usage_per_process, key=memory_usage_per_process.get)
    max_cpu_user = max(cpu_usage_per_process, key=cpu_usage_per_process.get)

    report = []
    report.append("Отчёт о состоянии системы:")
    report.append(f"Пользователи системы: {', '.join(sorted(users))}")
    report.append(f"Процессов запущено: {process_count}")
    report.append("")
    report.append("Пользовательских процессов:")
    for user in sorted(users):
        report.append(f"{user}: {int(memory_usage_per_process[user])}")
    report.append("")
    report.append(f"Всего памяти используется: {memory_usage:.1f}%")
    report.append(f"Всего CPU используется: {cpu_usage:.1f}%")
    report.append(
        f"Больше всего памяти использует: {max_memory_user} ({memory_usage_per_process[max_memory_user]:.1f}%)"
    )
    report.append(
        f"Больше всего CPU использует: {max_cpu_user} ({cpu_usage_per_process[max_cpu_user]:.1f}%)"
    )

    for line in report:
        print(line)

    current_time = datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{current_time}-scan.txt"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            for line in report:
                file.write(line + "\n")
        print(f"Отчёт сохранён в файл: {filename}")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")


if __name__ == "__main__":
    get_system_report()
