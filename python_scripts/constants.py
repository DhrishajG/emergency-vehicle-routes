from enum import Enum

class StartNode(Enum):
    small_block = "25445347" 

class EndNode(Enum):
    small_block = "cluster_12485172228_30763597"

class StartEdge(Enum):
    small_block = "4794926#1"

class EndEdge(Enum):
    small_block = "-4794936#1"

class NetworkFile(Enum):
    small_block = "../sumo_simulations/small_block/osm.net.xml.gz"

class ConfigFile(Enum):
    small_block = "../sumo_simulations/small_block/osm.sumocfg"