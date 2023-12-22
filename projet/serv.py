import threading
import time

import hashlib
import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import matplotlib.pyplot as plt

time_data = []
temperature1_data = []
humidity1_data = []
temperature2_data = []
humidity2_data = []


def update_plots(temperature_device1, temperature_device2, humidity_device1, humidity_device2):
    """
    Function that plots the data received from the MQTT broker. Each data has its separate plot.
    :param temperature_device1: temperature detected on device 1
    :param temperature_device2: temperature detected on device 2
    :param humidity_device1: humidity detected on device 1
    :param humidity_device2: humidity detected on device 2
    :return:
    """
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
    plt.plot(humidity_device1, label='Humidity 1', color='green')
    plt.title('Humidity 1')
    plt.legend()

    # Plotting Humidity 2
    plt.subplot(2, 2, 4)
    plt.plot(humidity_device2, label='Humidity 2', color='red')
    plt.title('Humidity 2')
    plt.legend()

    # Adjust layout for better visualization
    plt.tight_layout()

    # Show the plots
    plt.show()


def calculate_blake2s_hash(cipher, key):
    """
    Function that calculates the hash of the cipher and the key using the blake2s algorithm
    :param cipher: cipher to hash
    :param key: key with which the cipher is hashed
    :return:
    """
    data_to_hash = cipher.encode('utf-8') + key.encode('utf-8')
    blake2s_hash = hashlib.blake2s(data_to_hash)
    hash_result = blake2s_hash.hexdigest()
    return hash_result


def decrypt(encrypted_text):
    """
    Function that decrypts the encrypted text received from the MQTT broker. The encrypted text is decrypted using the
    AES algorithm. We set the symmetric key and the AES cipher object with CBC mode and PKCS7 padding. Finally, we
    decrypt the encrypted text and return the decrypted text.
    :param encrypted_text: text to decrypt
    :return:
    """
    iv_str, message, hash = encrypted_text.split(';')
    key = "mySecretKeyUsedForHMAC"
    cipher = message
    # hmac not 100% working
    # if hash != calculate_blake2s_hash(cipher, key):
    #     print(calculate_blake2s_hash(cipher, key),'\n',hash,'\n')
    #     print("HMAC verification failed!")
    iv = [int(byte_str) for byte_str in iv_str.split(',')]

    encrypted_message = base64.b64decode(message)
    aes_key = bytes([23, 45, 56, 67, 67, 87, 98, 12, 32, 34, 45, 56, 67, 87, 65, 5])

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(bytes(iv)), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    decrypted_text = decrypted_message

    decrypted_text = decrypted_text[0:5]
    decrypted_text = decrypted_text.decode('utf-8')

    return decrypted_text


def on_connect(client, userdata, flags, rc):
    """
    Callback function that is called when the client connects to the MQTT broker. If the connection is successful, the
    client subscribes to different topics.
    :param client: client that connects to the MQTT broker
    :param userdata: data of the user
    :param flags: flags of the connection
    :param rc: return code of the connection
    :return:
    """
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("humidity1")
        client.subscribe("temperature1")
        client.subscribe("humidity2")
        client.subscribe("temperature2")
    else:
        print(f"Connection failed with error code {rc}")


last_update_time = time.time()


def on_message(client, userdata, msg):
    """
    Callback function that is called when the client receives a message from the MQTT broker. The function decrypts the
    message and updates the data lists, containing all that the broker has sent concerning all the topics.
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    global last_update_time

    topic = msg.topic
    decrypted_msg = decrypt(msg.payload.decode('utf-8'))

    if topic == "temperature1":
        temperature1_data.append(float(decrypted_msg[0:2]))
    elif topic == "humidity1":
        humidity1_data.append(float(decrypted_msg[0:2]))
    elif topic == "temperature2":
        temperature2_data.append(float(decrypted_msg[0:2]))
    elif topic == "humidity2":
        humidity2_data.append(float(decrypted_msg[0:2]))

    # print(temperature1_data, temperature2_data, humidity1_data, humidity2_data)
    # print(f"Received message on topic {topic}: {decrypted_msg}")


def periodic_update():
    """
    Function that periodically updates the plots with the data received from the MQTT broker.
    :return:
    """
    while True:
        update_plots(temperature1_data, temperature2_data, humidity1_data, humidity2_data)
        time.sleep(5)



update_thread = threading.Thread(target=periodic_update)

update_thread.start()

client = mqtt.Client()

client.username_pw_set("toto", "tata")
client.on_connect = on_connect
client.on_message = on_message

broker_address = "192.168.21.193"
port = 1883

client.connect(broker_address, port, keepalive=60)

client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from MQTT broker")
