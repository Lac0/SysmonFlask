# Memory Information
import psutil, os, socket, threading
from flask import Flask, render_template

def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/memoryinfo")
def get_memory_info():
    #  get the memory details
    svmem = psutil.virtual_memory()
    RAM_total=(f"{get_size(svmem.total)}")
    RAM_free=(f"{get_size(svmem.available)}")
    RAM_used=(f"{get_size(svmem.used)}")
    RAM_percentage=(f"{svmem.percent}%")

    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    SWAP_total=(f"{get_size(swap.total)}")
    SWAP_free=(f"{get_size(swap.free)}")
    SWAP_used=(f"{get_size(swap.used)}")
    SWAP_percentage=(f"{swap.percent}%")

    memory_dict ={}
    for variable in ["RAM_total", "RAM_free", "RAM_used","RAM_percentage","SWAP_total", "SWAP_free", "SWAP_used","SWAP_percentage"]:
        memory_dict[variable]=eval(variable)
    return(memory_dict)

@app.route("/systemload")
def system_load():
    system_load_dict={}
    load1, load5, load15 = os.getloadavg()
    for variable in ["load1","load5","load15"]:
        system_load_dict[variable]=eval(variable)
    return(system_load_dict)
    
@app.route("/cpuinfo")
def cpuinfo():
    cpuinfo_dict={}
    physical_cores=(psutil.cpu_count(logical=False))
    total_cores=(psutil.cpu_count(logical=True))
    cpufreq = psutil.cpu_freq()
    max_frequency=(f"{cpufreq.max:.2f}Mhz")
    for var in ["physical_cores","total_cores","max_frequency"]:
        cpuinfo_dict[var]=eval(var)
    return cpuinfo_dict
    
@app.route("/inodeinfo")
def inode_info():
    inode_dict={}

    inodes_max=os.popen("df -i / | awk '{print $2}' | grep -v 'Inodes'").read().strip()
    inodes_used=os.popen("df -i / | awk '{print $3}'| grep -v 'IUsed'").read().strip()
    inodes_percentage_used=os.popen("df -i / | awk '{print $5}'| grep -v 'IUse%'").read().strip()
    
    for var in ["inodes_max","inodes_used","inodes_percentage_used"]:
        inode_dict[var]=eval(var)
    return inode_dict

@app.route("/OpenPorts")
def open_ports():
    open_ports_dict={}
    target = "127.0.0.1" 
    def port_scanner(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            print(f"{port}")
            plort=str(port)
            open_ports_dict[plort]=eval(plort)
            
        except:
            pass
    for port in range(1,65535):
        thread = threading.Thread(target =port_scanner, args=[port])
        thread.start()
    return open_ports_dict

@app.route("/liveTCP_UDPconnections")
def TCP_UDPconnections():
    konekcije=(os.popen("netstat -natu | grep 'ESTABLISHED'").read())
    return konekcije

if __name__ == "__main__":
    app.run(host='0.0.0.0')   