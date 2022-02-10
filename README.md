# DEPRECATED

No longer maintained. 

<hr>


# Hubitat Tools

## Overview
This is my personal playspace for Hubitat Elevation support tools. You are welcome to use it. Right now all it has is a better logging page.  

If you are not a developer or willing to mess with installing software on the command line, this probably isn't for you.

## Installation 
* Clone / copy the repository 
* Set up a python 3.7 virtual environment for it
    * I really like [direnv](https://direnv.net/). If you set up direnv and set up the direnv python layout, .envrc will automatically create the virtual environment for you
    * But if that's too difficult, just get this directory working wth python 3.7
* Then install via pip with -e (editable):
```
mkdir htools
git clone xxx .
pip install -e .
```
* Run
```
echo From within the root (htools) directory
./bin/htools run
echo "In your browser, open http://127.0.0.1:8027"
echo "Then in the page that opens, enter the IP Address of your Hubitat Elevation"
echo "EG: 192.168.1.155"
```
* Log Page Parameters  
You can do something like:
```
http://127.0.0.1:8027/?ipaddress=192.168.1.155&maxPastLogLines=500
```


