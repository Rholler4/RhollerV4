# Pull system resource usage and get it ready in JSON to send

import subprocess

def get_cpu_usage():
    """Returns the current CPU load as a percentage."""
    try:
        cpu_load = subprocess.check_output('cut -f 1 -d " " /proc/loadavg', shell=True).decode("utf-8").strip()
        return float(cpu_load) * 100  # Convert to percentage for consistency
    except Exception as e:
        print(f"Error retrieving CPU usage: {e}")
        return None

def get_ram_usage():
    """Returns the RAM usage in MB and as a percentage of total RAM."""
    try:
        mem_info = subprocess.check_output("free -m | awk 'NR==2{printf \"%s %s\", $3, $3*100/$2 }'", shell=True).decode("utf-8").strip().split()
        return {"used": int(mem_info[0]), "percentage": float(mem_info[1])}
    except Exception as e:
        print(f"Error retrieving RAM usage: {e}")
        return None

def get_ip_address():
    """Returns the IP address of the system."""
    try:
        IP = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True).decode("utf-8").strip()
        return IP
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None

def get_disk_usage():
    """Returns the disk usage as used/total GB and percentage."""
    try:
        disk_info = subprocess.check_output('df -h | awk \'$NF=="/"{printf "%d %d %s", $3,$2,$5}\'', shell=True).decode("utf-8").strip().split()
        return {"used_gb": int(disk_info[0]), "total_gb": int(disk_info[1]), "percentage": disk_info[2]}
    except Exception as e:
        print(f"Error retrieving disk usage: {e}")
        return None



"""
HOW TO USE THIS SHIT

from system_info_module import get_cpu_usage, get_ram_usage, get_ip_address, get_disk_usage

# Example usage
system_info = {
    "cpu_usage": get_cpu_usage(),
    "ram_usage": get_ram_usage(),
    # "ip_address": get_ip_address(),  # Uncomment if needed
    # "disk_usage": get_disk_usage()  # Uncomment if needed
}

# This `system_info` dictionary can now be converted to JSON and sent to the laptop

"""