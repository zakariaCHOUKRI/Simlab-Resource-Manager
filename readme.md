# Resource Management System for Cluster Partitions

## Overview

The Resource Management System for Cluster Partitions is an application designed to facilitate the management of cluster resources. Users can select a partition and automatically view the number of available CPUs and GPUs in that partition. The application utilizes ```scontrol```, ```squeue```, and ```sinfo``` commands for data collection and employs Dash to create a user interface.

## Prerequisites

Before running the application, ensure that you have the following:

- Access to UM6P WiFi network.
- SSH access to the simlab.

## Getting Started

1. Connect to the UM6P WiFi network.

2. Open your terminal and connect to simlab using the following command:

   ```
   ssh -L 5000:localhost:5000 username@simlab-cluster.um6p.ma
   ```

   Replace `username` with your HPC username and enter your password when prompted.

3. Clone this repository:

   ```
   git clone https://github.com/zakariaCHOUKRI/Simlab-Resource-Manager.git
   ```

4. Change into the project directory:

   ```
   cd Simlab-Resource-Manager
   ```

5. Run the resource manager script:

   ```
   ./resource-manager.sh
   ```

6. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).

## Usage


- The application will establish an SSH tunnel to the HPC, run the necessary scripts, and open a web interface on [http://localhost:5000](http://localhost:5000).

- Use the web interface to select a partition from the list of available partitions.

- The number of available CPUs and GPUs in the selected partition will be automatically displayed.

## Project by


- [Abderrahmane Baidoune](https://github.com/baidoune01)
- [Zakaria Choukri](https://github.com/zakariaCHOUKRI)
- [Ayman Youss](https://github.com/aymanyouss)
  
Special thanks to [Imad Kissami](https://github.com/imadki) for the guidance :)