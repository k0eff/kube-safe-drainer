from src.util.k8s.podParent import PodParent


class Pod:

    name: str
    kind: str
    namespace: str
    parent: PodParent

    def __init__(self, name, namespace, parent: PodParent = None):
        self.name = name
        self.kind = "Pod"
        self.namespace = namespace
        if parent: self.parent = parent

    def setParent(self, parent: PodParent):
        self.parent = parent
