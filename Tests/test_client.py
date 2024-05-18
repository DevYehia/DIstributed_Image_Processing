import unittest
from unittest.mock import MagicMock, patch

import unittest
import sys
import os


# Determine the parent directory of client.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.append(parent_dir)

import client
class TestSendImagesNumber(unittest.TestCase):
    
    @patch('client.client')
    def test_send_images_number(self, mock_client):
        print("Testing SendImagesNumber function: ")
        mock_client.send.return_value = None
        mock_client.recv.return_value = b'OK'

        client.send_images_number(5)

        mock_client.send.assert_called_once_with(b'5')
        mock_client.recv.assert_called_once()


class TestSendOperation(unittest.TestCase):
    
    @patch('client.client')
    def test_send_operation(self, mock_client):
        print("Testing SendOperation function: ")
        mock_client.send.return_value = None
        mock_client.recv.return_value = b'OK'

        client.send_operation('Invert')

        mock_client.send.assert_called_once_with(b'Invert')
        mock_client.recv.assert_called_once()


class TestSendImage(unittest.TestCase):
    
    @patch('client.client')
    def test_send_image(self, mock_client):
        print("Testing SendImage function: ")
        with patch('builtins.open', unittest.mock.mock_open(read_data=b'file_data')) as mock_open:
            client.send_image('distributed_icon2.png')

        mock_client.send.assert_called()
        # Add assertions for other calls if needed


if __name__ == '__main__':
    print("\n---- Note . means successfull testcase!------\n")
    unittest.main()
