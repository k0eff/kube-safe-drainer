
def sanitizeArgs(args):
    if bool(args.nodes): args.nodes = args.nodes.split(',')
    else: args.nodes = []
    return args