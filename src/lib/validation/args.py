import re

def sanitizeArgs(args):
    if bool(args.nodes): args.nodes = args.nodes.split(',')
    else: args.nodes = []
    
    if not hasattr(args, 'pause') or not re.search('^[0-9]{1,}$', str(args.pause)): args.pause = 30
    else: args.pause = int(args.pause)

    if not hasattr(args, 'uncordon') or len(str(args.uncordon)) > 0: args.uncordon = True
    elif not str(args.uncordon) == 'false': args.uncordon = False
    return args