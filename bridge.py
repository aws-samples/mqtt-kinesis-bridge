# MQTT-to-Kinesis Bridge
from __future__ import print_function

import json
import argparse
import boto
import paho.mqtt.client as paho

from argparse import RawTextHelpFormatter
from boto.kinesis.exceptions import ResourceNotFoundException

# To preclude inclusion of aws keys into this code, you may temporarily add 
# your AWS credentials to the file:
#     ~/.boto
# as follows:
#     [Credentials]
#     aws_access_key_id = <your access key>
#     aws_secret_access_key = <your secret key>

def get_stream(stream_name):
    stream = None
    try:
        stream = kinesis.describe_stream(stream_name)
        print(json.dumps(stream, sort_keys=True, indent=2,
                         separators=(',', ': ')))
    except ResourceNotFoundException as rnfe:
        print('Could not find ACTIVE stream:{0} error:{1}'.format(
            stream_name, rnfe.message))
    return stream


def sum_posts(kinesis_actors):
    """Sum all posts across an array of KinesisPosters
    """
    total_records = 0
    for actor in kinesis_actors:
        total_records += actor.total_records
    return total_records


class MQTTKinesisBridge(object):
    """A Bridge that subscribes to a topic and repeatedly posts messages
    as records to shards in the given Kinesis stream. Each record will post
    to the Kinesis stream with the topic_name as the stream partition key.
    """

    def __init__(self, mqtt_host, kinesis_stream, mqtt_port=1883,
                 mqtt_keepalive=60, mqtt_bind_address='', mqtt_topic_name='#',
                 quiet=False):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_keepalive = mqtt_keepalive
        self.mqtt_bind_address = mqtt_bind_address
        self.mqtt_topic_name = mqtt_topic_name
        self.client = paho.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self._pending_records = []
        self.stream_name = kinesis_stream
        self.quiet = quiet
        self.sleep_interval = 5
        self.total_records = 0

    def add_records(self, records):
        """ Add given records to the Poster's pending records list.
        """
        self._pending_records.extend(records)

    def put_all_records(self, partition_key='mqttkb'):
        """Put all pending records in the Kinesis stream."""
        precs = self._pending_records
        self._pending_records = []
        self.put_records(precs, partition_key)
        self.total_records += len(precs)
        return len(precs)

    def put_records(self, records, partition_key):
        """Put the given records in the Kinesis stream."""
        for record in records:
            response = kinesis.put_record(
                stream_name=self.stream_name,
                data=record, partition_key=partition_key)
            if self.quiet is False:
                print("-= put seqNum:", response['SequenceNumber'])

    def connect(self):
        print("Starting MQTT-to-Kinesis bridge")
        self.client.connect_async(host=self.mqtt_host,
                                  port=self.mqtt_port,
                                  keepalive=self.mqtt_keepalive,
                                  bind_address=self.mqtt_bind_address)

    def on_message(self, mqttc, userdata, msg):
        print('on_message topic: "{0}" msg.payload: "{1}"'.format(
            msg.topic,
            msg.payload)
        )
        self.add_records(records=[msg.payload])
        self.put_all_records(partition_key=msg.topic)

    def on_connect(self, mqttc, userdata,flags, msg):
        rc = mqttc.subscribe(self.mqtt_topic_name, 0)
	print('Connection Msg: '.format(msg))
        print('Subscribe topic: {0} RC: {1}'.format(self.mqtt_topic_name, rc))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Bridge a MQTT Broker to a Kinesis stream. All messages
on a particular topic will be sent downstream as records.''',
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('stream_name',
                        help='''the name of the Kinesis stream to connect''')
    parser.add_argument('--host_name', default='localhost',
                        help='''the name of the MQTT host to connect [default: 'localhost']''')
    parser.add_argument('--topic_name', default='mqttkb/+',
                        help='''the name of the MQTT topic to connect [default: 'mqttkb/+']''')
    parser.add_argument('--region', default='us-east-1',
                        help='''the region of your Kinesis Stream [default: 'us-east-1']''')

    args = parser.parse_args()
    kinesis = boto.kinesis.connect_to_region(args.region)
    kinesis_stream = get_stream(args.stream_name)
    bridge = MQTTKinesisBridge(
        mqtt_host=args.host_name,
        mqtt_topic_name=args.topic_name,
        kinesis_stream=args.stream_name
    )
    bridge.connect()
    print('Bridge Connected, looping...')
    bridge.client.loop_forever()
