# Unipharm
Unipharm is a pharmaceutical company based in Israel. The goal of this project is to help Unipharm with their stock management, specifically identifying mismatches between the expected locations of containers and their actual locations.
# Components
The system consists of 4 main components:
1) Image Processing Server (IPS) - Receives images taken at the warehouse by the cameras on the forklift, detects the barcodes on both the containers and the shelves, translates them to material # and location respectively, and finally outputs a log with all the mismatches
2) Unipharm's Database - Contains the "ground truth", meaning the data we compare the results of the IPS with. The info, i.e where each container is located, is inserted manually
3) Cameras equipped with Raspberry Pi - There are two cameras, one on each side of the forklift, each equipped with a Raspberry Pi running a process constantly feeding the IPS with images using FTP
4) Web Client - Contains a friendly UI for tuning parameters
# Installing Dependencies
To install all the necessary dependencies run the following command inside the terminal when inside this project's directory:
`./install_deps.sh`
