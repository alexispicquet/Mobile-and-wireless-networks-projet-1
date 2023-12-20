import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64


def decrypt(encrypted_text):
    iv_str, message = encrypted_text.split(';')

    iv = [int(byte_str) for byte_str in iv_str.split(',')]

    # Decode Base64-encoded encrypted message to bytes
    encrypted_message = base64.b64decode(message)

    # AES key (must be the same key used for encryption in your C++ code)
    aes_key = bytes([23, 45, 56, 67, 67, 87, 98, 12, 32, 34, 45, 56, 67, 87, 65, 5])

    # Create an AES cipher object with CBC mode and PKCS7 padding
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(bytes(iv)), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the message
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    # decrypted_text = decrypted_message.decode('utf-8')
    #
    # return decrypted_text
    #fct pas car bytes bizzare
    return decrypted_message

# Exempleq d'utilisation:
encrypted_string = "196,161,204,13,153,108,186,11,152,148,103,2,145,218,161,82;xKHMDZlsuguYlGcCkdqhUg=="
decrypted_result = decrypt(encrypted_string)
print(decrypted_result)



# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to the topics you are interested in
        client.subscribe("humidite")
        client.subscribe("temperature")
    else:
        print(f"Connection failed with error code {rc}")

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")

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
