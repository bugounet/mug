# mug

display text after a sip

# setup

```shell
# install system libs
sudo apt install python3-pip python3-virtualenv p7zip-full libopenjp2-7 -y
# create your venv
virtualenv venv
source venv/bin/activate
# add the libs
pip install -r requirements.txt
```

# run

```
$ JOKES_SELECTION_INTERVAL=5 AIRTABLE_API_KEY={YOUR_AIRTABLE_API_KEY} python jokes.py
```