import unittest
from unittest.mock import patch, MagicMock
import json
from src.dependencies.sqs import SqsSender, send_create_doc_data

class TestSqsSender(unittest.TestCase):

    @patch('src.dependencies.sqs.boto3.resource')
    @patch('src.config')
    def test_send_message(self, mock_config, mock_boto_resource):
        # Mocking configurations and boto3 resource and response
        mock_config.LOCALSQS = "true"
        mock_queue = MagicMock()
        mock_boto_resource.return_value.get_queue_by_name.return_value = mock_queue
        mock_response = {'MessageId': 'test_id', 'MD5OfMessageBody': 'test_md5'}
        mock_queue.send_message.return_value = mock_response
        
        # Testing
        sqs_sender = SqsSender()
        message = {"key": "value"}
        sqs_sender.send_message(message)
        
        # Assertions
        mock_boto_resource.assert_called_once()
        mock_queue.send_message.assert_called_once_with(MessageBody=json.dumps(message))

    @patch('src.dependencies.sqs.SqsSender.send_message')
    def test_send_create_doc_data(self, mock_send_message):
        # Mocking send_message method from SqsSender class
        message = {"key": "value"}
        
        # Testing
        response = send_create_doc_data(message)
        
        # Assertions
        mock_send_message.assert_called_once_with(message)
        self.assertEqual(response, "sent")


if __name__ == "__main__":
    unittest.main()
