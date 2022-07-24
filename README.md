# sensehat-mqtt-python
Python script to upload the Raspi Sense Hat data to an MQTT Broker.

# ENV Vars
This project uses `dotenv`.  Create a file named `.env` next to `main.py` and add these properties/values to it.

- `DEVICE_ID=`
- `UPDATE_SECONDS=`
- `MQTT_HOST=`
- `MQTT_USERNAME=`
- `MQTT_PASSWORD=`

The `DEVICE_ID` will also be the `topic` the MQTT Client will publish it's updates to.

# General Use
* Install python dependencies with:
  * `pip install -r requirements.txt`
* Run the script with:
  * `python main.py`
  
# Run as a System Service
To run this script as a system service and there by control it with `systemctl ` commands, follow these steps:

_Note: This assumes the project code has been copied to `/home/pi/sensehat-mqtt-python` if it has been copied elsewhere, adjust the service file accordingly!_

* Copy the `sensehat-mqtt-python.service` file to `/lib/systemd/system/sensehat-mqtt-python.service`
* Set the Permissions on the Service File:
  * `sudo chmod 644 /lib/systemd/system/sensehat-mqtt-python.service`
* Reload the Systemd daemon:
  * `sudo systemctl daemon-reload`
* Add the Systemd Service to run at Startup:
  * `sudo systemctl enable sensehat-mqtt-python.service`
* Start the Systemd Service:
  * `sudo systemctl start sensehat-mqtt-python.service`
* Check the Service Status (As needed):
  * `sudo systemctl status sensehat-mqtt-python.service`