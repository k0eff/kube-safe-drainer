import time
from src.lib.k8s.k8s import checkIfContextExists, cordon, filterDeploymentsOnly, filterOutPodsInNodes, getAllPodsAndParents, getDeploymentsForRollout, getNmspNames, printList, raiseExceptionIfFalse, restartDeployments
from kubernetes import client, config

def run(args):
    contexts, activeContext = config.list_kube_config_contexts()
    raiseExceptionIfFalse(checkIfContextExists(contexts,args.context),'Given Context does not exist.')
    # config.load_kube_config()
    apiClient = config.new_client_from_config(context=args.context)
    v1 = client.CoreV1Api(apiClient)
    v1ext = client.AppsV1Api(apiClient)
    nmspData = v1.list_namespace().items
    namespaces = getNmspNames(nmspData)

    nodes = v1.list_node()
    pods = filterOutPodsInNodes(v1.list_pod_for_all_namespaces(), args.nodes)
    replicaSets = v1ext.list_replica_set_for_all_namespaces()
    statefulSets = v1ext.list_stateful_set_for_all_namespaces()
    daemonSets = v1ext.list_daemon_set_for_all_namespaces()
    deployments = v1ext.list_deployment_for_all_namespaces()


    podList = getAllPodsAndParents(replicaSets, statefulSets, daemonSets, deployments, pods)
    podsDeploymentsOnly = filterDeploymentsOnly(podList)
    print("### Beginning...")
    print("### Rollout plan:")
    printList(getDeploymentsForRollout(podsDeploymentsOnly))

    print("### Cordoning nodes:")
    printList(args.nodes)
    cordon(kubeV1Api=v1, nodesList=nodes, nodesToUnschedule=args.nodes, direction=True)

    
    print("### Executing rollout...")
    restartDeployments(kubeV1AppsApi=v1ext, podList=podsDeploymentsOnly)


    if (args.uncordon == True):
        print("### Pausing for 30 secs before uncordoning back...")
        time.sleep(30)
        print("### Uncordoning...")
        cordon(kubeV1Api=v1, nodesList=nodes, nodesToUnschedule=args.nodes, direction=False)

