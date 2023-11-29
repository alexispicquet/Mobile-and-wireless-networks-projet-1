# Add in Conf file

```
listener 1883 0.0.0.0
```
```
password_file <path to the configuration file>
```
```
allow_anonymous true
```

# To start the service

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