# import json
# import os

# primary_ips = []
# secondary_ips = []

# with open("public_ips.json") as f:
#     public_ips = json.load(f)

# for i, ip in enumerate(public_ips):
#     if i < 1:
#         primary_ips.append(ip)
#     else:
#         secondary_ips.append(ip)

# with open("hosts.ini", "w") as f:
#     f.write("[db_master]\n")
#     # print(os.environ["ip_prim"])

#     for ip in primary_ips:
#         f.write(ip + " ansible_connection=ssh ansible_ssh_user=ubuntu ansible_ssh_private_key_file=./postgres-db-key-test\n")
        

#     f.write("\n[db_replica]\n")
#     for ip in secondary_ips:
#         f.write(ip + " ansible_connection=ssh ansible_ssh_user=ubuntu ansible_ssh_private_key_file=./postgres-db-key-test\n")

####################################

import json
import os

primary_ips = []
secondary_ips = []

def generate_ansible_hosts(private_ips, public_ips):
    ip_mapping = {}
    
    # Create a dictionary mapping private IP addresses to public IP addresses
    for private_ip, public_ip in zip(private_ips, public_ips):
        ip_mapping[private_ip] = public_ip
    
    ansible_hosts = []
    
    # Generate the Ansible host strings
    for private_ip, public_ip in ip_mapping.items():
        ansible_host = f"{private_ip} ansible_host={public_ip}\n"
        ansible_hosts.append(ansible_host)
    
    return ansible_hosts


def generate_ansible_hosts_master_replica(private_ips, public_ips):
    ip_mapping = {}
    
    # Create a dictionary mapping private IP addresses to public IP addresses
    for private_ip, public_ip in zip(private_ips, public_ips):
        ip_mapping[private_ip] = public_ip
    
    ansible_hosts = {
        'master': [],
        'replica': []
    }
    
    # Generate the Ansible host strings
    for private_ip, public_ip in ip_mapping.items():
        ansible_host = f"{private_ip} ansible_host={public_ip}"
        
        # Add the host string to the appropriate group
        if private_ip == private_ips[0]:
            ansible_hosts['master'].append(ansible_host)
        else:
            ansible_hosts['replica'].append(ansible_host)
    
    return ansible_hosts

with open("public_ips.json") as f:
    public_ips = json.load(f)
with open("private_ips.json") as f:
    private_ips = json.load(f)

with open("hosts.ini", "w") as f:
    ansible_hosts = generate_ansible_hosts(private_ips, public_ips)

    f.write("[etcd_cluster]\n")
    # Print the generated Ansible host strings
    for host in ansible_hosts:
        f.write(host)

    f.write("[balancers]\n")
    # Print the generated Ansible host strings
    for host in ansible_hosts:
        f.write(host)
    f.write("[pgbackrest]\n")
    # Print the generated Ansible host strings
    for host in ansible_hosts:
        f.write(host)
    ansible_hosts_master_replica = generate_ansible_hosts_master_replica(private_ips, public_ips)

    for group, hosts in ansible_hosts_master_replica.items():
        f.write(f"[{group}]\n")
        f.write('\n'.join(hosts) + '\n')


    f.write("[postgres_cluster:children]\n")
    f.write("master\n")
    f.write("replica\n")

    f.write("[all:vars]\n")
    f.write("ansible_connection='ssh'\n")
    f.write("ansible_ssh_port='22'\n")
    f.write("ansible_ssh_user=ubuntu\n")
    # f.write("ansible_python_interpreter='/usr/bin/python3'")
    f.write("ansible_ssh_private_key_file=./postgres-db-key-test\n")

    f.write("[pgbackrest:vars]\n")
    f.write("ansible_connection='ssh'\n")
    f.write("ansible_ssh_port='22'\n")
    f.write("ansible_ssh_user=ubuntu\n")
    f.write("ansible_ssh_private_key_file=./postgres-db-key-test\n")
