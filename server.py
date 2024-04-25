import socket
from operations import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 1234))
server.listen(5)

client, addr = server.accept()
payload = client.recv(1024).decode("utf-8")
client.send(b"1")
operation = payload.split(";")[0]
print("Operation Selected is: ",operation)
img_name = payload.split(";")[1]
print("Image Name is: ",img_name)

img = open(img_name,"wb")
img_data = b""

done = False
while True:
    data = client.recv(1024)
    if not data: break
    img_data += data
img.write(img_data)

org_img = cv2.imread(img_name)
if operation == "blur":
    plt.imshow(blur(org_img),cmap="gray")
    plt.show()
elif operation == "GrayScale":
    new_img = gray(org_img)
elif operation == "remove_SaltandPepper":
    plt.imshow(apply_median_filter(org_img),cmap="gray")
    plt.show()
elif operation == "Invert":  
    new_img = invert_photo(org_img)
elif operation == "Rotate 90°":
    new_img = rotate(org_img)
elif operation == "adjust_contrast":
    plt.imshow(check_and_adjust_contrast(org_img),cmap="gray")
    plt.show()

cv2.imwrite("new" + img_name, new_img)  


img.close()
client.close()
server.close()
