from src.util.k8s.podParent import PodParent


class ParentLookup:

    replicaSets: object
    daemonSets: object
    statefulSets: object
    deployments: object


    def __init__(self, replicaSets, daemonSets, statefulSets, deployments):
        self.replicaSets = replicaSets
        self.daemonSets = daemonSets
        self.statefulSets = statefulSets
        self.deployments = deployments

    def findParent(self, kind, name, namespace):
        if kind == "ReplicaSet": return self.findParentInReplicaSet(name, kind, namespace)
        if kind == "StatefulSet": return self.findParentStatefulSet(name, kind, namespace)
        if kind == "DaemonSet": return self.findParentDaemonSet(name, kind, namespace)
        if kind == "Deployment": return self.findParentDeployment(name, kind, namespace)

    def recurseFind(self, name, kind, namespace, data):
        for each in data:
            if each.metadata.name == name and each.metadata.namespace == namespace:
                if bool(each.metadata.owner_references) and len(each.metadata.owner_references) > 0:
                    innerParent = self.findParent(
                        each.metadata.owner_references[0].kind,
                        each.metadata.owner_references[0].name,
                        namespace)
                    ret = PodParent(
                        name = innerParent['name'],
                        kind = innerParent['kind'],
                        namespace = namespace
                    )
                    return ret
                else:
                    return PodParent(
                        name = name,
                        kind = kind,
                        namespace = namespace
                    )
        return {}

    def findParentInReplicaSet(self, name, kind, namespace):
        return self.recurseFind(name, kind, namespace, self.replicaSets.items)

    def findParentDaemonSet(self, name, kind, namespace):
        return self.recurseFind(name, kind, namespace, self.daemonSets.items)

    def findParentDeployment(self, name, kind, namespace):
        return self.recurseFind(name, kind, namespace, self.deployments.items)

    def findParentStatefulSet(self, name, kind, namespace):
        return self.recurseFind(name, kind, namespace, self.statefulSets.items)

