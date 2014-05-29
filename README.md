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
and follow the instructions [here](http://docs.pythonboto.org/en/latest/getting_started.html#configuring-boto-credentials) to get your credentials setup in boto for use. The credentials you use should permit at least these Kinesis actions: ``` CreateStream, DescribeStream, GetRecords, GetShardIterator, ListStreams & 
PutRecord```. Both the ```MergeShards``` and ```SplitShard``` actions are 
unused in this example.

Once boto is configured with your credentials, run: 
````
$ TBD
```` 

Related Resources
-----------------
* [Amazon Kinesis Developer Guide](http://docs.aws.amazon.com/kinesis/latest/dev/introduction.html)  
* [Amazon Kinesis API Reference](http://docs.aws.amazon.com/kinesis/latest/APIReference/Welcome.html)
* [AWS SDK for Python](http://aws.amazon.com/sdkforpython)
