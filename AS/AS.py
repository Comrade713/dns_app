import socket
import json

DNS_RECORD_FILE = "dns_records.json"

try:
    with open(DNS_RECORD_FILE, 'r') as f:
        dns_records = json.load(f)
except FileNotFoundError:
    dns_records = {}
    with open(DNS_RECORD_FILE, 'w') as f:
        json.dump(dns_records, f)

def handle_registration(data, address):
    try:
        lines = data.split('\n')
        if len(lines) < 4:
            return "Invalid registration request"

        type_ = lines[0].split('=')[1]
        name = lines[1].split('=')[1]
        value = lines[2].split('=')[1]
        ttl = lines[3].split('=')[1]

        if type_ != "A":
            return "Unsupported DNS record type"

        dns_records[name] = {"value": value, "ttl": ttl}
        with open(DNS_RECORD_FILE, 'w') as f:
            json.dump(dns_records, f)

        return "Registration successful"
    except Exception as e:
        return f"Registration failed: {str(e)}"

def handle_dns_query(data, address):
    try:
        lines = data.split('\n')
        if len(lines) < 2:
            return "Invalid DNS query request"

        type_ = lines[0].split('=')[1]
        name = lines[1].split('=')[1]

        if type_ != "A":
            return "Unsupported DNS query type"

        if name in dns_records:
            record = dns_records[name]
            return f"TYPE=A\nNAME={name}\nVALUE={record['value']}\nTTL={record['ttl']}"
        else:
            return "DNS record not found"
    except Exception as e:
        return f"DNS query failed: {str(e)}"

server_address = ('0.0.0.0', 53533)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

print(f"Authoritative Server is running on {server_address}")

while True:
    try:
        data, address = sock.recvfrom(4096)
        data = data.decode()

        if "TYPE=A" in data and "NAME=" in data:
            if "VALUE=" in data:
                response = handle_registration(data, address)
            else:
                response = handle_dns_query(data, address)
        else:
            response = "Invalid request"

        sock.sendto(response.encode(), address)
    except KeyboardInterrupt:
        print("Shutting down server.")
        break
    except Exception as e:
        print(f"An error occurred: {str(e)}")