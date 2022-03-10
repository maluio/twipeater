# diagram.py
from diagrams import Diagram, Edge, Cluster
from diagrams.programming.framework import Flask
from diagrams.saas.social import Twitter
from diagrams.onprem.client import Client

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "pad": "0.5",
}

# https://diagrams.mingrammer.com/docs/getting-started/installation
with Diagram("Request flow", filename="docs/twipeater-diagram", graph_attr=graph_attr):
    with Cluster("Web Service"):
        service = Client()

    with Cluster("Twipeater"):
        app = Flask()

    with Cluster("Twitter"):
        twitter = Twitter()

    service << Edge(label="GET /tweets/<twitter username>.json") << app << Edge(label="\n") << twitter

    service >> Edge(label="\n\n[{tweet1 {..}, tweet2 {...}}]") >> app >> Edge(label="\n") >> twitter
