import os
import shutil
import fileinput
import sys

PG_PATH = r"C:\Program Files\PostgreSQL\18\data\pg_hba.conf"
BACKUP_PATH = PG_PATH + ".bak"

def modify_config():
    print(f"Modifying {PG_PATH}...")
    with open(PG_PATH, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Target IPv4 and IPv6 local connections
        if (line.strip().startswith("host") and "127.0.0.1/32" in line) or \
           (line.strip().startswith("host") and "::1/128" in line):
            # Replace method with trust
            parts = line.split()
            # method is usually the last part
            parts[-1] = "trust"
             # Join with tabs/spaces. Original file often uses spaces alignment, but tabs work.
             # We'll just reconstruct simple space separation
            new_line = "\t".join(parts) + "\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    with open(PG_PATH, 'w') as f:
        f.writelines(new_lines)
    print("Config modified to TRUST.")

def restore_config():
    print("Restoring config...")
    shutil.copyfile(BACKUP_PATH, PG_PATH)
    print("Config restored.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_config()
    else:
        modify_config()
