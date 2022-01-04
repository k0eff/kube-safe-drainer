from argparse import ArgumentParser
import sys
from src.lib.validation.args import sanitizeArgs

from src.util.k8s.parentLookup import ParentLookup
from src.util.k8s.pod import Pod

from src.controllers.main import Controllers

parserMain = ArgumentParser()
subparsers = parserMain.add_subparsers(dest='mode')


parserDrainer = subparsers.add_parser('drain',description='drain mode', help='Use this to safely drain nodes')
parserDrainer.add_argument('--context', help='Use specific kubeconfig context')
parserDrainer.add_argument('--nodes', help='Look for pods in these nodes', required=False)
parserDrainer.add_argument('--pause', help='How much to wait before uncordoning, applicable only if uncordoning is enabled', required=False)
parserDrainer.add_argument('--uncordon', help='If enabled will finish by uncordoning the node(s). If set to false (default value) will leave the node cordoned which is expected to result in the node being halted by the autoscaler', required=False)


parserUpgrade = subparsers.add_parser('upgrade', description='upgrade mode', help='Use this to upgrade control plane and node pools')


# args = sanitizeArgs(parserMain.parse_args())
args = parserMain.parse_args()


try:
    
    ctrls = Controllers()
    ctrls.get(args.mode)(args)

except Exception as e:
    print("Fatal error occured. Giving up: ", e)



