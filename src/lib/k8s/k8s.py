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
