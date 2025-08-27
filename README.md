# Algorithmic Approach to Ambulance Routing
## Project Overview

This project aims to evaluate and compare the performance of different pathfinding algorithms for ambulance routing under dynamic traffic conditions. By exploring traditional algorithms like **Dijkstra's** and **A\* (Euclidean)** alongside **Swarm Intelligence-based methods** such as **Ant Colony Optimization (ACO)**, this project investigates their effectiveness in real-time, congestion-aware routing. The primary goal is to reduce ambulance response times in urban environments with varying traffic conditions.

Screencast: https://youtu.be/FapgTwcBCPk

### **Key Algorithms Implemented:**
- **Dijkstra's Algorithm**: A classic shortest-path algorithm that computes the shortest route between nodes in a graph.
- **A\* Algorithm (Euclidean)**: An optimized version of Dijkstra's, which uses heuristics to improve pathfinding efficiency.
- **A\* with Real-Time Traffic**: An extension of A\* that dynamically adjusts its pathfinding based on real-time traffic data.
- **Ant Colony Optimization (ACO)**: A nature-inspired optimization technique based on the foraging behavior of ants, suitable for dynamic environments.

## **Objective and Goals**

### **Main Objective**:
- **To develop and compare different algorithms for ambulance routing**, considering dynamic traffic conditions, using real-time or simulated data. The goal is to find the most effective pathfinding strategy for reducing response time and improving efficiency in urban traffic environments.

### **Specific Goals**:
- Model the road network as a weighted graph based on real-time traffic data or simulated conditions.
- Implement and compare the performance of **Dijkstra’s**, **A\***, and **ACO** algorithms for route selection in various traffic scenarios.
- Develop a **hybrid A\* + ACO algorithm**, incorporating ACO’s pheromone influence to improve the real-time route selection of ambulances.
- Perform **traffic simulation** using the **SUMO** framework with varying congestion conditions, simulating a week of traffic behavior with different rush hour patterns.
- Assess the **performance** of each algorithm under different levels of congestion, tracking metrics like **response time**, **success rate**, and **computational complexity**.

## **Data Sources**

1. **OpenStreetMap (OSM)**:
   - The road network for the Kyoto block was extracted using **OSM Web Wizard** for accurate representation of the area's infrastructure.
  
2. **SUMO Traffic Simulation**:
   - Traffic patterns were simulated using the **SUMO framework** and **randomTrips.py** to create realistic vehicle flows on the road network.

3. **Kyoto Traffic Data**:
   - Traffic data sources, such as **TomTom Traffic Index** and Kyoto-specific congestion data, were used to define the dynamic nature of traffic and simulate rush-hour congestion patterns.


## **How to Run the Project**

### **Requirements**:
- Python 3.x
- **SUMO**: Install the SUMO traffic simulator to simulate traffic patterns.
- **NetworkX**: For graph-based algorithms like Dijkstra’s and A*.

### **Setup Instructions**:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DhrishajG/emergency-vehicle-routes.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install traci
   pip install matplotlib
   pip install sumolib
   pip install networkx
   pip install numpy
   ```

3. **Running the Simulation**:
   - To run the simulation, navigate to the project directory and use the following command:
     ```bash
     cd python_scripts
     python main.py
     ```

## **Python Script**
   - `main.py`: Running the SUMO simulation with ambulance routing algorithms implemented in Python
   - `graph_utils.py`: Graph extraction files
   - `algorithms.py`: Implementations of different algorithms
   - `aco.py`: Implementation of Ant Colony Optimisations customised for pathfinding
   - `ambulance_simulation.py`: For adding and tracking the ambulance in the simulation
   - `traffic_simulation.py`: For simulating congestion and accidents in the simulation
   - Other files include files that are experimental set-ups used for rhobust comparison between algorithms and parameter tuning.

## **Contributions**

- **Ambulance Routing Simulation**: Contributed to the implementation of pathfinding algorithms (Dijkstra's, A*, ACO) and their evaluation under various traffic conditions.
- **SUMO Traffic Simulation Setup**: Developed the traffic simulation environment and integrated it with pathfinding algorithms.
- **Data Analysis**: Conducted performance analysis using response time, success rate, and efficiency metrics.
