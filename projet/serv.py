import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
humidity2_data = []
import matplotlib.pyplot as plt

# Variables to store the data
time_data = []
temperature1_data = []
humidity1_data = []
temperature2_data = []

def update_plots(temperature_device1, temperature_device2, hum1, hum2):
    # Plotting Temperature Device 1
    plt.subplot(2, 2, 1)
    plt.plot(temperature_device1, label='Temperature Device 1')
    plt.title('Temperature Device 1')
    plt.legend()

    # Plotting Temperature Device 2
    plt.subplot(2, 2, 2)
    plt.plot(temperature_device2, label='Temperature Device 2', color='orange')
    plt.title('Temperature Device 2')
    plt.legend()

    # Plotting Humidity 1
    plt.subplot(2, 2, 3)
    plt.plot(hum1, label='Humidity 1', color='green')
    plt.title('Humidity 1')
    plt.legend()

    # Plotting Humidity 2
    plt.subplot(2, 2, 4)
    plt.plot(hum2, label='Humidity 2', color='red')
    plt.title('Humidity 2')
    plt.legend()

    # Adjust layout for better visualization
    plt.tight_layout()

    # Show the plots
    plt.show()


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

def on_message(client, userdata, msg):
    topic = msg.topic
    decrypted_msg = decrypt(msg.payload.decode('utf-8'))
    print(f"Received message on topic {topic}: {decrypted_msg}")

    # Update data lists
    if topic == "temperature1":
        temperature1_data.append(float(decrypted_msg))
    elif topic == "humidity1":
        humidity1_data.append(float(decrypted_msg))
    elif topic == "temperature2":
        temperature2_data.append(float(decrypted_msg))
    elif topic == "humidity2":
        humidity2_data.append(float(decrypted_msg))
    update_plots(temperature1_data, temperature2_data, humidity1_data, humidity2_data)
    print(f"Received message on topic {topic}: {decrypted_msg}")

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
