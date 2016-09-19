# traceroute -w 1 -q 1 -a -m 30 citibank.com

import subprocess
from pprint import pprint
domain = "nytimes.com"

# adapted from here: http://stackoverflow.com/a/4417735
def run(command):    
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    return iter(popen.stdout.readline, b"")




class Router(object):
    """docstring for Router"""
    def __init__(self, idx, as_number, name, ip):
        self.idx = idx
        self.as_number = as_number
        self.name = name
        self.ip = ip


def trace():
    end_after_empty = 5
    routers = list()

    empty_count = 0
    found_end = True
    command = "traceroute -w 1 -q 1 -a " + domain
    for line in run(command.split()):
        line = line.strip()
        # print line
        info = line.split()

        idx = info[0]

        if len(info) > 2:
            empty_count = 0
            info[3] = info[3][1:-1] #cleaning brackets from ip

            as_number = info[1]
            name = info[2]
            ip = info[3]
            
        else:
            empty_count += 1

            as_number = "[UNKNOWW]"
            name = "[UNKNOWW]"
            ip = "[UNKNOWW]"
            if empty_count >= end_after_empty:
                as_number = "[...]"
                name = "[...]"
                ip = "[...]"
                routers.append(Router(idx, as_number, name, ip))
                found_end = False
                break


        routers.append(Router(idx, as_number, name, ip))

    if found_end:
        routers[-1].ip += " [END]"

    return routers


def run_traces(num):
    traces = list()

    for i in range(num):
        print "tracing", i
        traces.append(trace())

    return traces


#to get terminal width and print centered:
# from here: http://stackoverflow.com/a/566752
def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])
(width, height) = getTerminalSize()       



traces = run_traces(20) 

routers_total = dict()


for trace in traces:
    for i, router in enumerate(trace):
        if i not in routers_total:
            routers_total[i] = dict()
            routers_total[i]["data"] = dict()
            routers_total[i]["total"] = 0

        if router.ip not in routers_total[i]["data"]:
            routers_total[i]["data"][router.ip] = 0
        routers_total[i]["data"][router.ip] += 1
        routers_total[i]["total"] += 1

pprint(routers_total)

print "\n"*5
print "~~~ YOU ~~~".center(width, ' ')
print ""
print "v".center(width, ' ')
print ""
print "|".center(width, ' ')
print ""

for step in routers_total:
    # print "STEP",step, ":",

    string = ""
    for i, ip in enumerate(routers_total[step]["data"]):
        if i > 0:
            string += " - "

        string += ip + " ("+str(100*(float(routers_total[step]["data"][ip])/float(routers_total[step]["total"])))+"%)"
    print string.center(width, ' ')
    print ""
    print "|".center(width, ' ')
    print ""
    # print 
print "v".center(width, ' ')
print ""
domain_string = "~~~ "+domain+" ~~~"
print domain_string.center(width, ' ')
print "\n"*5

