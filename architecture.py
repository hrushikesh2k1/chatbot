from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.k8s.storage import PV
from diagrams.onprem.database import MongoDB
from diagrams.azure.compute import VM
from diagrams.azure.network import VirtualNetworks

with Diagram(
    name="chatbot-aks-runtime-architecture",
    filename="docs/architecture/chatbot-runtime",
    outformat="png",
    show=False
):

    user = Users("Client")

    with Cluster("Azure VNet"):
        vnet = VirtualNetworks("Chatbot VNet")

        with Cluster("AKS Nodepool"):
            vm = VM("Worker Node")

            with Cluster("Kubernetes Cluster"):

                ingress = Ingress("NGINX Ingress")

                with Cluster("Chatbot Deployment"):
                    pod = Pod("Flask Pod")
                    docker = Docker("Chatbot Container")

                with Cluster("MongoDB StatefulSet"):
                    mongo = MongoDB("MongoDB")
                    storage = PV("Persistent Volume")

    user >> ingress >> pod >> docker
    docker >> mongo >> storage
    pod >> vm >> vnet