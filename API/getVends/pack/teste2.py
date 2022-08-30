from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os

# TODO(developer)
project_id = "vmgc-e-commerce"
subscription_id = "lastid"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "../vmgc-pubsub.json"
timeout = 2.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    retorno = message.data
    print(f"Received {retorno.decode()}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.