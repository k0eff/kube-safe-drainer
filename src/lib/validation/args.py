import re

def sanitizeArgs(args):
    if args.mode == 'drain': # TODO: provide better logic to check for modes

        if bool(args.nodes): args.nodes = args.nodes.split(',')
        else: args.nodes = []
        
        if not hasattr(args, 'pause') or not re.search('^[0-9]{1,}$', str(args.pause)): args.pause = 30
        else: args.pause = int(args.pause)

        if hasattr(args, 'uncordon') and len(str(args.uncordon)) > 0 and str(args.uncordon) == 'true': args.uncordon = True
        else: args.uncordon = False
    return args