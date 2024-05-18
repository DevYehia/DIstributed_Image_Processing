import unittest
import sys
import os
import cv2
import numpy as np

# Determine the parent directory of operations.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.append(parent_dir)

# Import the operations module
import operations

class TestOperations(unittest.TestCase):

    def setUp(self):
        # Load a sample image for testing
        self.image = cv2.imread('image.jpeg')

    def test_edges(self):
        # Test the edges function
        print("Testing edges function: ")
        edge_image = operations.edges(self.image)
        self.assertTrue(isinstance(edge_image, np.ndarray))

    def test_gray(self):
        # Test the gray function
        print("Testing gray function: ")
        gray_image = operations.gray(self.image)
        self.assertTrue(isinstance(gray_image, np.ndarray))
        self.assertEqual(len(gray_image.shape), 2)  # Check if the image is grayscale

    def test_rotate(self):
        # Test the rotate function
        print("Testing rotate function: ")
        rotated_image = operations.rotate(self.image)
        self.assertTrue(isinstance(rotated_image, np.ndarray))


if __name__ == '__main__':
    print("\n---- Note . means successfull testcase!------\n")
    unittest.main()