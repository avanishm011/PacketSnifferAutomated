import os
import subprocess

def capture_packets(interface="eth0", duration=30):
    print("[*] Capturing packets...")
    subprocess.run(["tshark", "-i", interface, "-a", f"duration:{duration}", "-w", "capture.pcap"])

def filter_packets():
    os.makedirs("http_packets", exist_ok=True)
    os.makedirs("non_http_packets", exist_ok=True)

    print("[*] Filtering HTTP packets...")
    subprocess.run(["tshark", "-r", "capture.pcap", "-Y", "http", "-w", "http_packets/http_packets.pcap"])

    print("[*] Filtering non-HTTP packets...")
    subprocess.run(["tshark", "-r", "capture.pcap", "-Y", "not http", "-w", "non_http_packets/non_http_packets.pcap"])

def extract_http_post_data():
    print("[*] Extracting POST data from HTTP packets...")
    result = subprocess.run(
        ["tshark", "-r", "http_packets/http_packets.pcap", "-Y", "http.request.method == POST", 
         "-T", "fields", "-e", "http.file_data"],
        capture_output=True, text=True)
    with open("http_post_data.txt", "w") as f:
        f.write(result.stdout)

if __name__ == "__main__":
    capture_packets()
    filter_packets()
    extract_http_post_data()
    print("[*] Done. Packets stored in respective folders.")

