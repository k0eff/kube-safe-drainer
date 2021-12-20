from kubernetes import client, config
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument('--context', help='Use specific kubeconfig context')
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

    config.load_kube_config()
    contexts, activeContext = config.list_kube_config_contexts()

    raiseExceptionIfFalse(checkIfContextExists(contexts,args.context),'Given Context does not exist.')

    v1 = client.CoreV1Api()
    nmspData = v1.list_namespace().items
    namespaces = getNmspNames(nmspData)


    print(namespaces)

except Exception as e:
    print("Fatal error occured. Giving up: ", e)



