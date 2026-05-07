import json

input_file = "raw_ips"   # file with IPs (one per line)
output_file = "short_ips.json"

data = []

with open(input_file, "r") as f:
    for line in f:
        ip = line.strip()
        if ip:  # skip empty lines
            data.append({"ip": ip})

with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

print("Done. Output saved to", output_file)
