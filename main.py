from kubernetes import client, config
from argparse import ArgumentParser
import sys
from src.lib.k8s.k8s import checkIfContextExists, filterOutPodsInNodes, getNmspNames, raiseExceptionIfFalse
from src.lib.validation.args import sanitizeArgs

from src.util.k8s.parentLookup import ParentLookup
from src.util.k8s.pod import Pod

parser = ArgumentParser()
parser.add_argument('--context', help='Use specific kubeconfig context')
parser.add_argument('--nodes', help='Look for pods in these nodes', required=False)
args = sanitizeArgs(parser.parse_args())



try:

    contexts, activeContext = config.list_kube_config_contexts()
    raiseExceptionIfFalse(checkIfContextExists(contexts,args.context),'Given Context does not exist.')
    # config.load_kube_config()
    apiClient = config.new_client_from_config(context=args.context)
    v1 = client.CoreV1Api(apiClient)
    v1ext = client.AppsV1Api(apiClient)
    nmspData = v1.list_namespace().items
    namespaces = getNmspNames(nmspData)
    pods = filterOutPodsInNodes(v1.list_pod_for_all_namespaces(), args.nodes)
    rsets = v1ext.list_replica_set_for_all_namespaces()
    statefulsets = v1ext.list_stateful_set_for_all_namespaces()
    daemonsets = v1ext.list_daemon_set_for_all_namespaces()
    mydeployment = rsets.items[0].metadata.owner_references[0].name
    deployments = v1ext.list_deployment_for_all_namespaces()

    plkup = ParentLookup(replicaSets=rsets, statefulSets=statefulsets, daemonSets=daemonsets, deployments=deployments)
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

    print(data)

except Exception as e:
    print("Fatal error occured. Giving up: ", e)



