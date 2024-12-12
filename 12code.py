from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

#Validate, Classify, and Process IP addresses
user_input = input(Fore.LIGHTMAGENTA_EX+"Enter IP addresses separated by spaces: "+Fore.RESET)

# Split the input into a list of IP addresses
ip_addresses = user_input.split()

# List to store the IP details
ip_details = []

for ip in ip_addresses:
    ip_octets = ip.split(".")

    # Check for exactly 4 octets
    if len(ip_octets) != 4:
        print(Fore.RED+f"Error: '{ip}' is missing octet.")
        continue

    valid = True  # Assume IP is valid initially

    # Check each octet for validity
    for octet in ip_octets:
        # Check if the octet is numeric
        if not octet.isdigit():
            print( Fore.YELLOW+f"Error: '{ip}' has an invalid octet '{octet}'. (Not a number)")
            valid = False
            continue

        # Convert the octet to an integer for further checks
        octet_int = int(octet)

        # Check for leading zeros (but allow single digit "0")
        if octet != str(octet_int):
            print(Fore.BLUE+f"Error: '{ip}' has an invalid octet '{octet}'(Leading zeros)")
            valid = False
            continue

        # Check if the octet is in the valid range (0-255)
        if octet_int < 0 or octet_int > 255:
            print(Fore.CYAN + f"Error: '{ip}' has an invalid octet '{octet}'. (Out of range)")
            valid = False
            
    if not valid:
        continue  # Skip to next IP if any octet is invalid

    # Classify IP and determine privacy
    first_octet = int(ip_octets[0])

    if 1 <= first_octet <= 126:
        ip_class = "A"
        subnet_mask = "255.0.0.0"
        privacy = "Private" if first_octet == 10 else "Public"
    elif 128 <= first_octet <= 191:
        ip_class = "B"
        subnet_mask = "255.255.0.0"
        privacy = "Private" if first_octet == 172 and 16 <= int(ip_octets[1]) <= 31 else "Public"
    elif 192 <= first_octet <= 223:
        ip_class = "C"
        subnet_mask = "255.255.255.0"
        privacy = "Private" if first_octet == 192 and int(ip_octets[1]) == 168 else "Public"
    elif 224 <= first_octet <= 239:
        ip_class = "D (Multicast)"
        subnet_mask = "N/A"
        privacy = "Public"
    elif 240 <= first_octet <= 255:
        ip_class = "E (Experimental)"
        subnet_mask = "N/A"
        privacy = "Public"  
    elif first_octet == 127:
        ip_class = "Loopback"
        subnet_mask = "255.0.0.0"
        privacy = "Private"
    else:
        ip_class = "Unknown"
        subnet_mask = "N/A"
        privacy = "N/A"

    # Calculate network and broadcast addresses if applicable
    if subnet_mask != "N/A":
        mask_octets = subnet_mask.split(".")
        network = []
        broadcast = []
        for i in range(4):
            network.append(str(int(ip_octets[i]) & int(mask_octets[i])))  # Bitwise AND
            broadcast.append(str(int(ip_octets[i]) | (255 - int(mask_octets[i]))))  # Bitwise OR
        network_address = ".".join(network)
        broadcast_address = ".".join(broadcast)
    else:
        network_address = "N/A"
        broadcast_address = "N/A"

    # Append to details list
    ip_details.append([ip, ip_class, privacy, network_address, broadcast_address])

# Step 4: Display a Summary Table
print("\n+--------------------------------------------------------------------+")
print(Fore.GREEN+"|   IP Address     | Class | Privacy  | Network       | Broadcast    |")
print("+--------------------------------------------------------------------+")
for row in ip_details:
    print(Fore.LIGHTMAGENTA_EX+f"| {row[0]:<15}  | {row[1]:<5}| {row[2]:<8}  | {row[3]:<13} | {row[4]:<13}|")
print("+---------------------------------------------------------------------+")
