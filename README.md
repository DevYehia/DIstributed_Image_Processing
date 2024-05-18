# DIstributed_Image_Processing

## Description

DIstributed_Image_Processing is a project that aims to implement distributed image processing algorithms.

## Installation

1. Clone the repository: `git clone https://github.com/your-username/DIstributed_Image_Processing.git`
2. Install the required dependencies (OpenCv - mpi4py - pip) on the 3 server instances you are goining to use.

   1. `sudo apt update`
   2. `sudo apt install python3-pip`
   3. `sudo apt install python3-opencv`
   4. `sudo apt install python3-mpi4py`

3. Change the IP addresses of the 3 instances in `loadBalancer.py` in the following list: `slavesIP`

4. make sure to have the following libraries for the GUI and client to run successfully: PIL and tkinter.

5. make sure to have the following libraries for the loadBalncer: numpy and cv2

## Usage

1. Navigate to the project directory: `cd DIstributed_Image_Processing`
2. Run the loadBalancer script: `python loadBalancer.py`
3. Run the server script: `python server.py`
4. Run the GUI script: `python GUI.py`

## License

This project is licensed under the [ASU License]().

## Contact

For any questions or feedback, feel free to reach out to us at [Yehia Hasan](mailto:20P1043@eng.asu.edu.e) or [Mohamed Ayman](mailto:20P9260@eng.asu.edu.e) or [Kerolos Noshy](mailto:21P0132@eng.asu.edu.e) or [Ismail Ahmed](mailto:20P8233@eng.asu.edu.e).
