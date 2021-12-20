class PodParent:

    name: str
    kind: str
    namespace: str

    def __new__(self, name, kind, namespace):
        self.name = name
        self.kind = kind
        self.namespace = namespace


