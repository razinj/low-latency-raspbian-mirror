import json
import re
import subprocess
import typing as t

list_of_urls = []
average_times = []


def display_result():
    sorted_data = sorted(average_times, key=lambda item: item["avg"])
    print("\n[!] Top 5 averages: ")
    for item in sorted_data[:5]:
        print(f"[!] {item['avg']}ms - {item['domain']}")


def ping_domain(domain: str) -> t.Union[float, None]:
    try:
        response = subprocess.run(
            ["ping", "-c", "5", domain], capture_output=True, text=True
        )
        # print("Response: stderr: ", response.stderr)
        # print("Response: stdout: ", response.stdout)
        # print("Response: returncode: ", response.returncode)

        # Use regular expression to extract the average time
        match = re.search(r"min/avg/max/stddev = \S+/\S+", response.stdout)
        if match:
            avg_time = match.group().split("/")[4]
            return float(avg_time)
        else:
            print("[X] Average time not found for domain")
            return None
    except subprocess.CalledProcessError:
        print("[X] Failed to ping domain")
        return None


def ping_urls():
    for url in list_of_urls:
        if not url.startswith("http://"):
            continue

        url_without_prefix = url[7:]
        try:
            index_of_first_slash = url_without_prefix.index("/")
        except ValueError:
            continue

        base_domain = url_without_prefix[:index_of_first_slash]
        print(f"[!] Pinging {base_domain}")
        avg_time = ping_domain(base_domain)
        if avg_time is not None:
            average_times.append({"domain": base_domain, "avg": avg_time})
        print('---------------------------------------------------')


def read_file():
    file = open("./raspbian_mirrors/urls.jsonl", "r")

    for raw_item in file:
        item_obj = json.loads(raw_item)
        list_of_urls.append(item_obj["url"])

    file.close()


read_file()
ping_urls()
display_result()
