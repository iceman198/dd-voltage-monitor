# dd-voltage-monitor
Monitor two voltage inputs

# Using Raspberry Pi as Hotspot
More info found here: https://www.theusabilitypeople.com/article/raspberry-pi-zero-hotspot-control-leds#:~:text=Raspberry%20Pi%20Zero%20as%20Hotspot%20to%20control%20LEDs,Access%20Point%20using%20Hostapd.%20...%20More%20items...%20

# Install pip3 on your Raspberry Pi
```
sudo apt-get install python3-pip
```

## Install serial py
```
pip3 install pyserial
```


# Other info
To be able to shutdown as pi users via python: https://peppe8o.com/shutdown-button-with-raspberry-pi-and-python/

## Run on pi on reboot
Setup crontab to run at boot.  Run
```
crontab -e
```

Add the following to the bottom of the file (update the path as needed!)
```
@reboot sudo python3 /home/pi/YOUR_CLONE_PATH/raspberryPi/src/main.py > /dev/null 2>&1 &
```