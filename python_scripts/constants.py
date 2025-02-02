from enum import Enum

class StartNode(Enum):
    small_block = "25445347" 
    city_block = "cluster_1496838998_9238240945_9238240946"

class EndNode(Enum):
    small_block = "cluster_12485172228_30763597"
    city_block = "3356864"

class StartEdge(Enum):
    small_block = "4794926#1"

class EndEdge(Enum):
    small_block = "-4794936#1"

class NetworkFile(Enum):
    small_block = "../sumo_simulations/small_block/osm.net.xml.gz"
    city_block = "../sumo_simulations/city_block/osm.net.xml.gz"

class ConfigFile(Enum):
    small_block = "../sumo_simulations/small_block/osm.sumocfg"
    city_block = "../sumo_simulations/city_block/osm.sumocfg"