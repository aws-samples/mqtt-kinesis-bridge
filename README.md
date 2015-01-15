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
with your credentials, in one Terminal Window or Command Line Shell:
````
$ mosquitto
````
and then in another, run the Kinesis Bridge:
````
$ python bridge.py <stream_name>
````
which will activate the [Mosquitto](http://mosquitto.org/) MQTT Broker and the
MQTT-to-Kinesis Bridge example, respectively. 
The defaults for the bridge is to connect to us-east-1, however you can specify the region with the --region argument
````
$ python bridge.py <stream_name> --region <region>
````

To send an example message to the MQTT endpoint that will then flow to the
Kinesis stream named ```<stream_name>``` you should post a message to
the ```mqttkb``` MQTT topic.<br/>
(Aside: ```mqttkb``` stands for "MQTT Kinesis Bridge")

In a third window you might run the following ```mosquitto_pub``` command to
submit an MQTT message to the ```localhost``` broker:
````
$ mosquitto_pub -h localhost -t "mqttkb/test" -m "howdy world_00”
````
which will result in close to the following being shown in the Kinesis Bridge's
output.
````
$ python bridge.py my-first-stream
{
  "StreamDescription": {
    "HasMoreShards": false,
    "Shards": [
      {
        "HashKeyRange": {
          "EndingHashKey": "340282366920938463463374607431768211455",
          "StartingHashKey": "0"
        },
        "SequenceNumberRange": {
          "StartingSequenceNumber": "49535927568753752356407087005221112966147386710595469313"
        },
        "ShardId": "shardId-000000000000"
      }
    ],
    "StreamARN": "arn:aws:kinesis:us-east-1:123gibberish:stream/my-first-stream",
    "StreamName": "my-first-stream",
    "StreamStatus": "ACTIVE"
  }
}
Starting MQTT-to-Kinesis bridge
Bridge Connected, looping...
Subscribe topic: mqttkb/+ RC: (0, 1)
on_message topic: "mqttkb/test" msg.payload: "howdy world_00"
-= put seqNum: 49535927568753752371147382937418582483315273051544748033
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
