# Add in Conf file

```
per_listener_settings false

listener 1883

allow_anonymous false

password_file C:\Users\cleme\Desktop\mosquitto\passwd

```

# Starting the service

**Not via cmd** + **open the port 1883**

# Add password file

## Create file and first user
```
mosquitto_passwd -c <password file> <username>
```

## Add more User
```
mosquitto_passwd <password file> <username>
```