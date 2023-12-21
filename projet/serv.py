import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def decrypt(encrypted_text):
    iv_str, message = encrypted_text.split(';')

    iv = [int(byte_str) for byte_str in iv_str.split(',')]

    # Decode Base64-encoded encrypted message to bytes
    encrypted_message = base64.b64decode(message)

    # AES key (must be the same key used for encryption in your C++ code)
    aes_key = bytes([23, 45, 56, 67, 67, 87, 98, 12, 32, 34, 45, 56, 67, 87, 65, 5 ])

    # Create an AES cipher object with CBC mode and PKCS7 padding
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(bytes(iv)), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the message
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    decrypted_text = decrypted_message
    # return decrypted_text
    #fct pas car bytes bizzare
    decrypted_text = decrypted_text[0:5]
    decrypted_text = decrypted_text.decode('utf-8')

    return decrypted_text



# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to the topics you are interested in
        client.subscribe("humidite")
        client.subscribe("temperature")
    else:
        print(f"Connection failed with error code {rc}")

def write_to_file(data,file):
    with open(file, 'a') as f:
        f.write(data + '\n')

# Callback when a message is received from the MQTT broker

style.use('fivethirtyeight')

fig = plt.figure()
axe1 = fig.add_subplot(1, 1, 1)

# Set the maximum number of points to be displayed
max_points = 10


def animate(interval):
    graph_data = open('filedata.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = map(int, line.split(','))
            xs.append(x)
            ys.append(y)

    # Display only the last 'max_points' points
    xs = xs[-max_points:]
    ys = ys[-max_points:]

    axe1.clear()
    axe1.plot(xs, ys)

def on_message(client, userdata, msg):
    topic = msg.topic
    msg = msg.payload.decode('utf-8')
    msg = decrypt(msg)

    print(f"Received message on topic {topic}: {msg}")

    with open("filedata.txt", 'w+') as file:
        # Write content to the file
        x = len(file.readlines())
        file.write(f"{x}, ',', {msg}\n")

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.username_pw_set("toto","tata")
client.on_connect = on_connect
client.on_message = on_message

# Specify the MQTT broker's address and port
broker_address = "192.168.21.193"
port = 1883

# Connect to the broker
client.connect(broker_address, port, keepalive=60)

# Start the MQTT client loop
client.loop_start()

# Keep the program running to maintain the MQTT connection and process incoming messages
try:
    while True:
        pass
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from MQTT broker")
