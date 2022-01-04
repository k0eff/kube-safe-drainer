# kube-safe-drainer

# # What does this do?
It drains nodes

# # How?
Using the following procedure:
- cordon a node
- check all running pods and extract Deployments and Daemonsets
- rollout restart all extracted pods
- drain the node - optionally

# # Why?
Because `kubectl drain` deletes pods and this might make an app unavailable

# # Additional info
usage: python3 main.py [-h] [--context CONTEXT] [--nodes NODES] [--pause PAUSE] [--uncordon UNCORDON]

optional arguments:
  -h, --help           show this help message and exit
  --context CONTEXT    Use specific kubeconfig context
  --nodes NODES        Look for pods in these nodes
  --pause PAUSE        How much to wait before uncordoning, applicable only if uncordoning is enabled
  --uncordon UNCORDON  If enabled will finish by uncordoning the node(s). If set to false (default value) will leave the node cordoned which is expected to result in the node being halted by the autoscaler