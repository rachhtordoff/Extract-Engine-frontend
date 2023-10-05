from src import config
import boto3
import json

class SqsSender(object):

    def __init__(self):
        if config.LOCALSQS == "true":
            self.sqs = boto3.resource('sqs',
                            endpoint_url='http://sqs:9324',
                            region_name='elasticmq',
                            aws_secret_access_key=config.aws_access_key_id,
                            aws_access_key_id=config.aws_secret_access_key,
                            use_ssl=False)
        else:
            self.sqs = boto3.resource('sqs',
                            region_name='eu-west-2',
                            aws_access_key_id= config.aws_access_key_id,
                            aws_secret_access_key= config.aws_secret_access_key)

    def __open_sqs_connection(self):
        self.queue = self.sqs.get_queue_by_name(QueueName= config.SQS_QUEUE_NAME)

    def send_message(self, message):
        self.__open_sqs_connection()

        response = self.queue.send_message(
            MessageBody=json.dumps(message),
        )

        # The response is NOT a resource, but gives you a message ID and MD5
        print(response.get('MessageId'))
        print(response.get('MD5OfMessageBody'))


def send_create_doc_data(json_data):
    SqsSender().send_message(json_data)
    return "sent"
