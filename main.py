from kubernetes import client, config
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument('--context', help='Use specific kubeconfig context')
parser.add_argument('--nodes', help='Look for pods in these nodes', required=False)
args = parser.parse_args()




def raiseExceptionIfFalse(val,msg):
    if val == False: raise Exception(msg)

def checkIfContextExists(ctxs, ctx):
    for e in ctxs:
        if e['name'] == ctx: return True
    return False


def getNmspNames(items):
    all = []
    for item in items:
        if (bool(item._metadata) and bool(item._metadata.name)): all.append(item._metadata.name)
        else: raise Exception('Error: BadNmspItem')
    return all

try:

    contexts, activeContext = config.list_kube_config_contexts()
    raiseExceptionIfFalse(checkIfContextExists(contexts,args.context),'Given Context does not exist.')
    # config.load_kube_config()
    apiClient = config.new_client_from_config(context=args.context)
    v1 = client.CoreV1Api(apiClient)
    v1ext = client.AppsV1Api(apiClient)
    nmspData = v1.list_namespace().items
    namespaces = getNmspNames(nmspData)
    pods = v1.list_pod_for_all_namespaces()
    rsets = v1ext.list_replica_set_for_all_namespaces()
    mydeployment = rsets.items[0].metadata.owner_references[0].name
    deployments = v1ext.list_deployment_for_all_namespaces()

    data = []
    for eachPod in pods.items:
        eachPodName = eachPod.metadata.name
        eachPodParent = eachPod.metadata.owner_references[0].name
        eachPodParentKind = eachPod.metadata.owner_references[0].kind


        eachRset = rsets.items[0].metadata.owner_references[0].name

    print(namespaces)

except Exception as e:
    print("Fatal error occured. Giving up: ", e)



