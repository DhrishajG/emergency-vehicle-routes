from enum import Enum

class StartNode(Enum):
    small_block = "25445347" 
    city_block = "cluster_1496838998_9238240945_9238240946"
    kyoto = "402756569"
    salt_lake_city = "cluster_1581511473_6617107590_6617107592_6617107594_#1more"

class EndNode(Enum):
    small_block = "cluster_12485172228_30763597"
    city_block = "3356864"
    kyoto = "5832017725"
    salt_lake_city = "cluster_1226595452_1226595691_1226595858_1226596304_#13more"

class StartEdge(Enum):
    small_block = "4794926#1"

class EndEdge(Enum):
    small_block = "-4794936#1"

class NetworkFile(Enum):
    small_block = "../sumo_simulations/small_block/osm.net.xml.gz"
    city_block = "../sumo_simulations/city_block/osm.net.xml.gz"
    kyoto = "../sumo_simulations/kyoto/osm.net.xml.gz"
    salt_lake_city = "../sumo_simulations/salt_lake_city/osm.net.xml.gz"

class ConfigFile(Enum):
    small_block = "../sumo_simulations/small_block/osm.sumocfg"
    city_block = "../sumo_simulations/city_block/osm.sumocfg"
    kyoto = "../sumo_simulations/kyoto/osm.sumocfg"
    salt_lake_city = "../sumo_simulations/salt_lake_city/osm.sumocfg"

class CongestionPath(Enum):
    small_block = ["628003088#2", "648408521#0","648408521#2", "648408521#4", "648408521#6", "648408521#9", "648408521#10", "1266310080#1"]
    city_block = ["-780336#7", "-780336#6", "-780336#5", "-780336#4", "-780336#3", "-780336#2", "-1003177677#0"]

class AccidentEdge(Enum):
    small_block = "648408521#2"
    city_block = "-780336#5"

class AmbulanceRoutes(Enum):
    city_block = [
        ("a1", "1837761454", "cluster_11733791581_11787450057_30890505"),
        ("a2", "cluster_1496838998_9238240945_9238240946", "3356864"),
        ("a3", "cluster_11975219383_1837761525", "cluster_28889609_643133_8239185538_8239185541_#4more"),
        ("a4", "2934047986", "3562485"),
        ("a5", "cluster_11594016602_11594016604_25423456", "25345878"),
        ("a6", "30891126", "cluster_11877028868_4618187"),
        ("a7", "1837761454", "3562485"),
        ("a8", "cluster_11594016602_11594016604_25423456", "cluster_28889609_643133_8239185538_8239185541_#4more")
    ]
    kyoto = [
        ("a1", "402756569", "5832017725"),
        ("a2", "11001012538", "372657189"),
        ("a3", "354847841", "356288174"),
        ("a4", "cluster_2737069339_2737069341_332507385_3834323572_#4more", "cluster_434344373_4600871790"),
        ("a5", "cluster_2624724422_2731038428_2731038430_2731038462_#4more", "cluster_243798390_2731038331_2731038332_2731038334_#4more"),
        ("a6", "cluster_2085630430_2783198760_2783198762_307683995", "434344383"),
        ("a7", "354847839", "354840398"),
        ("a8", "372657146", "372657243")
    ]