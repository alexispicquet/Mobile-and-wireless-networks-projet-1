# Add in Conf file

```
per_listener_settings false

listener 1883

allow_anonymous false

password_file C:\Users\cleme\Desktop\mosquitto\passwd

```

# Starting the service

On windows with **powershell** ```net start mosquitto```

# Add password file

## Create new file then add first user with
```
mosquitto_passwd -c <password file> <username>
```

## Add more User
```
mosquitto_passwd <password file> <username>
```