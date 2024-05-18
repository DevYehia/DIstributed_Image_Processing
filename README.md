# Distributed_Image_Processing

## Description

Distributed_Image_Processing is a project that aims to implement an application that the user uses to apply different image operations on his images. The System always to take the images and distribute them to multiple machines using aa load balancer.

## Installation

1. Clone the repository: `git clone https://github.com/your-username/DIstributed_Image_Processing.git`
2. Install the required dependencies (OpenCv - mpi4py - pip) on the 3 server instances you are goining to use.

   1. `sudo apt update`
   2. `sudo apt install python3-pip`
   3. `sudo apt install python3-opencv`
   4. `sudo apt install python3-mpi4py`

3. Change the IP addresses of the 3 instances in `loadBalancer.py` in the following list: `slavesIP`

4. Make sure to have the following libraries for the GUI and client to run successfully: PIL and tkinter.

5. Make sure to have the following libraries for the loadBalncer: numpy and cv2

## Usage

1. Navigate to the project directory: `cd DIstributed_Image_Processing`
2. Run the loadBalancer script: `python loadBalancer.py`
3. Run the server script: `python server.py`
4. Run the GUI script: `python GUI.py`

## License

This project is licensed under the [ASU License]().

## Contact

For any questions or feedback, feel free to reach out to us at [Yehia Hasan](https://github.com/DevYehia) or [Mohamed Ayman](https://github.com/M0hAyman) or [Kerolos Noshy](https://github.com/Kerolos-Noshy) or [Ismail Ahmed](https://github.com/Ismailseddik).
