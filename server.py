from mpi4py import MPI
import numpy as np
import cv2
from operations import *
import os
import socket
import threading

def handle_client(client_socket, client_addr):
    while True:
        payload = client_socket.recv(1024).decode("utf-8")
        if not payload:
            break
        
        client_socket.send(b"1")
        operation = payload.split(";")[0]
        print("Operation Selected is: ", operation)
        img_name = payload.split(";")[1]
        print("Image Name is: ", img_name)
        img_size = int(payload.split(";")[2])
        print("Image Size is", img_size)
        
        img_data = b""
        while img_size:
            data = client_socket.recv(min(img_size, 4096))
            img_size -= len(data)
            img_data += data
        
        # Broadcast image data to all processes
        comm.bcast(img_data, root=0)
        
        # Each process handles the client payload
        handle_client_payload(payload, img_data)

    client_socket.close()

def handle_client_payload(payload, img_data):
    operation = payload.split(";")[0]
    img_name = payload.split(";")[1]
    img_size = int(payload.split(";")[2])
    
    # Decode image data
    image_bytes = bytes(img_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    org_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Divide image processing task among processes
    chunk_size = org_img.shape[0] // size
    start_row = rank * chunk_size
    end_row = start_row + chunk_size if rank < size - 1 else org_img.shape[0]

    if operation == "Edge Detection":
        print(org_img[start_row:end_row, :],"Before")
        new_img_chunk = edges(org_img[start_row:end_row, :])
    elif operation == "GrayScale":
        new_img_chunk = gray(org_img[start_row:end_row, :])
    elif operation == "Invert":
        new_img_chunk = invert_photo(org_img[start_row:end_row, :])
    elif operation == "Rotate 90°":
        new_img_chunk = rotate(org_img[start_row:end_row, :])
    elif operation == "Increase Brightness":
        new_img_chunk = incerase_brightness(org_img[start_row:end_row, :])

    # Gather processed image chunks from all processes to rank 0
    new_img_gathered = comm.gather(new_img_chunk, root=0)

    if rank == 0:
        # Concatenate gathered image chunks along rows to form final image
        new_img = np.concatenate(new_img_gathered, axis=0)

        # Save processed image
        cv2.imwrite("new_" + img_name, new_img)

        # Get size of processed image
        new_img_length = os.path.getsize("new_" + img_name)

        # Send size of processed image back to client
        comm.send(new_img_length, dest=0)

        # Send processed image back to client
        if rank != 0:
            comm.send(new_img, dest=0)

print("Server started, waiting for connections...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))
server.listen(5)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
