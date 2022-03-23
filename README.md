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

# # Examples

```python3 main.py drain --context=my_context --nodes=my_node1,my_node2 --pause=60```

# # Additional info
To get additional info, just write the following in the console:

```python3 main.py -h```

```python3 main.py drain -h```

```python3 main.py upgrade -h```


# Installation
```
git clone https://github.com/k0eff/kube-safe-drainer
cd kube-safe-drainer
git checkout drainer
chmod u+x scripts/requirements-install.sh
python3 main.py drain --context <kube cluster context> --nodes <node1>,<node2>
```