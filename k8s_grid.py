import sys
from termcolor import colored
from kubernetes import client, config
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def usage():
    print("Usage")
    print("# python k8s_grid.py --host <host> --token <token>")
    sys.exit(1)

if (len(sys.argv) != 5):
    usage()

Token = sys.argv[4]

config.load_kube_config()
configuration=client.Configuration()
configuration.verify_ssl = False
configuration.host = sys.argv[2]
configuration.api_key = {"authorization": "bearer " + Token}
client.Configuration.set_default(configuration)
v1 = client.CoreV1Api()
print("Listing pods Running/Failed/Pending/Succeeded/Total for every nodes")
ret = v1.list_node()

for node in ret.items:
    counter_running = 0
    counter_notrunning = 0
    counter_failed = 0
    counter_pending = 0
    counter_succeeded = 0
    counter = 0
    field_selector='spec.nodeName='+node.metadata.name
    ret2 = v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
    
    for pod in ret2.items:
         counter += 1
         if (pod.status.phase == "Running"):
            counter_running += 1
         elif (pod.status.phase == "Failed"):
            counter_failed += 1
         elif (pod.status.phase == "Pending"):
            counter_pending += 1
         elif (pod.status.phase == "Succeeded"):
            counter_succeeded += 1

    try:
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (colored(node.metadata.name, 'blue'), node.metadata.labels["nodegroup"] , " Running: "+colored(str(counter_running),'green')," Failed: "+colored(str(counter_failed),'red')," Pending: "+colored(str(counter_pending),'yellow')," Succeeded: "+colored(str(counter_succeeded),'cyan')," Total: "+colored(str(counter),'white')))
    except KeyError:
        print("%s\t%s\t%s\t%s\t%s\t%s" % (colored(node.metadata.name, 'blue'), " Running: "+colored(str(counter_running),'green')," Failed: "+colored(str(counter_failed),'red')," Pending: "+colored(str(counter_pending),'yellow')," Succeeded: "+colored(str(counter_succeeded),'cyan')," Total: "+colored(str(counter),'white')))        

print("")
print("Unschedulable nodes:")
field_selector='spec.unschedulable=true'
ret = v1.list_node(field_selector=field_selector)

for node in ret.items:
    print (colored(node.metadata.name,'red'))
