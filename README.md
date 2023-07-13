# MazeSolver

## Description
An ESP rover and Raspberry Pi Control Server using computer vision to solve a line maze.

Features Include:​
-  Computer Vision to extract, straighten and transform the maze​.
-  Dynamic calibration using a PID controller based on computer vision​.
-  Finding shortest path in a dynamic maze using A-star.

## Table of Contents

- [Camera](#camera)
- [ESP32](#esp32)
- [Image-processing](#image-processing)
- [Robot](#robot)
- [Server](#server)
- [Distance-calibration](#distance-calibration)
- [Maze-controller-app](#maze-controller-app)
- [Hardware individual tests](#hardware-individual-tests)
- [Project Poster](#project-poster)

## Camera

This module contains the Pi-camera code for the camera entity. It provides functionality for capturing images and video using the Raspberry Pi camera.

## ESP32

The ESP32 module includes all the code related to the robot. It handles movement control, application communication protocol to receive messages, and the main loop that manages different states and behaviors of the robot.

## Image-processing

The Image-processing module is responsible for processing the camera images using the OpenCV module. It includes functionality for finding the maze frame, skeletonizing the maze, and finding the shortest path using the A-star algorithm.

## Robot

The Robot module is a virtual representation of the physical robot. It stores all the parameters required by the Raspberry Pi to activate and control the robot's movements.

## Server

The Server module is a basic web server that facilitates communication between the ESP32-robot and the React application. It initiates connections, listens for requests, and handles communication between different components of the system.

## Distance-calibration

The Distance-calibration module includes the PID (Proportional, Integral, and Derivative) algorithm for distance calibration. It provides functionality to fine-tune and control the robot's movement and distance measurements.

## maze-controller-app

The maze-controller-app is a reactive application that allows users to control the system. It provides features such as starting/stopping the car, recalculating the path, and capturing real-time pictures using the camera module.

## Hardware individual tests

The hardware individual tests module is used to check each component of the hardware independently. It includes various tests to ensure the proper functioning of different hardware components.

## Project Poster:
![poster](https://github.com/ordavid-s/MazeSolver/assets/73240562/d23f6bc4-4e0a-4a0d-8d07-c5c4173bc9de)

This project is part of ICST - The Interdisciplinary Center for Smart Technologies, Taub Faculty of Computer Science, Technion https://icst.cs.technion.ac.il/
