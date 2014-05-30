mqtt-kinesis-bridge
=====================

A simple Python-based MQTT-to-Kinesis Bridge example

* * *
Getting Started
---------------
To get this example working with Python 2.7+, first install boto 2.23+ 
and paho-mqtt 0.4.91+ using: 
````
$ pip install boto
$ pip install paho-mqtt
````
and follow the instructions [here](http://docs.pythonboto.org/en/latest/getting_started.html#configuring-boto-credentials) to
get your credentials setup in the AWS SDK for Python (aka. boto) for use. The
credentials you use should permit at least these Kinesis actions:
``` CreateStream, DescribeStream, GetRecords, GetShardIterator, ListStreams &
PutRecord```. Both the ```MergeShards``` and ```SplitShard``` actions are
unused in this example.

Then install the Mosquitto MQTT Broker by following the instructions [here](http://mosquitto.org/download/), for
your OS of choice.

Once the Mosquitto broker is installed and the AWS SDK for Python is configured
with your credentials, in one Terminal Window or Command Line Shell run:
````
$ mosquitto
````
and then in another, run:
````
$ python bridge.py <stream_name>
````
which will activate the [Mosquitto](http://mosquitto.org/) MQTT Broker and the MQTT-to-Kinesis Bridge
example, respectively.

To send an example message to the MQTT endpoint that will then flow to the
Kinesis stream named ```<stream_name>``` you should post a message to
the ```mqttkb``` MQTT topic.<br/>
(Aside: ```mqttkb``` stands for "MQTT Kinesis Bridge")

Here’s an example command using ```mosquitto_pub```:
````
$ mosquitto_pub -h localhost -t "mqttkb/test" -m "howdy world_00”
````

For detailed help and configuration options, enter: ```python bridge.py --help```

Related Resources
-----------------
* [Amazon Kinesis Developer Guide](http://docs.aws.amazon.com/kinesis/latest/dev/introduction.html)  
* [Amazon Kinesis API Reference](http://docs.aws.amazon.com/kinesis/latest/APIReference/Welcome.html)
* [AWS SDK for Python](http://aws.amazon.com/sdkforpython)
* [Paho MQTT](http://eclipse.org/paho/)
* [Mosquitto Broker](http://mosquitto.org/)
* [Apache 2.0 License](http://aws.amazon.com/apache2.0)
