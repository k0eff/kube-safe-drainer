from datetime import datetime
from typing import List
from src.util.k8s.parentLookup import ParentLookup

from src.util.k8s.pod import Pod


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


def filterOutPodsInNodes(pods, nodes):
    i = 0
    filteredItems = []
    while i < len(pods.items)-1:
        if pods.items[i].spec.node_name in nodes: filteredItems.append(pods.items[i])
        i += 1
    pods.items = filteredItems
    return pods


def getAllPodsAndParents(replicaSets, statefulSets, daemonSets, deployments, pods):
    plkup = ParentLookup(replicaSets, statefulSets, daemonSets, deployments)
    data = []
    for eachPod in pods.items:
        eachPodName = eachPod.metadata.name
        eachPodParent = eachPod.metadata.owner_references[0].name
        eachPodParentKind = eachPod.metadata.owner_references[0].kind
        eachPodNamespace = eachPod.metadata.namespace

        realParent = plkup.findParent(eachPodParentKind, eachPodParent, eachPodNamespace)

        data.append(
            Pod(
                name=eachPodName, 
                namespace=eachPodNamespace, 
                parent=realParent)
        )
    return data

def filterDeploymentsOnly(podList):
    results = []
    for pod in podList:
        if pod.hasParent() and pod.parent.kind == "Deployment": results.append(pod)
    return results


def restartDeployments(kubeV1AppsApi, podList):
    now = datetime.now()
    now = str(now.isoformat('T') + 'Z')
    body = {
        'spec': {
            'template': {
                'metadata': {
                    'annotations': {
                        'kubectl.kubernetes.io/restartedAt': now
                    }
                }
            }
        }
    }
    for pod in podList:
        kubeV1AppsApi.patch_namespaced_deployment(pod.parent.name, pod.parent.namespace, body, pretty='true')

def cordon(kubeV1Api, nodesList, nodesToUnschedule, direction:bool=True):
    body = {
        'spec': {
            'unschedulable': direction
        }
    }
    for node in nodesList.items:
        if node.metadata.name in nodesToUnschedule:
            kubeV1Api.patch_node(node.metadata.name, body)
    return True

def getDeploymentsForRollout(podList):
    l = []
    for one in podList:
        l.append(str(one.parent.name + ':' + one.parent.namespace))
    return l

def printList(l):
    for each in l:
        print(each)