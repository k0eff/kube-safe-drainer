from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
# from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
import azure.identity as ai

def run(args):
    credential = InteractiveBrowserCredential()
    token = credential.get_token()

    resouceClient=ResourceManagementClient(token,args.subscription, )
    resouceList=resouceClient.resources.list_by_resource_group(args.g)
    for i in resouceList:
        print(i)
    
    containerClient=ContainerServiceClient(credential,args.subscription)
    pass