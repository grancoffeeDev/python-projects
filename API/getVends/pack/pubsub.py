import json
import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from google.api_core import retry

class pubsub:
    def __init__(self,credentials=None) -> None:
        self.credentials = credentials
        self.r = None
        if self.credentials != None:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= self.credentials    

    def set(self, project,topic):
        self.project = project
        self.topic = topic
        return

    def send(self, message):
        project_id = self.project 
        #self_topic_id = topic_id
        self.message = message

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, self.topic)
        data_str = json.dumps(self.message)
        data = data_str.encode("utf-8")
        future = publisher.publish(topic_path, data)
        return future.result()
        #print(future.result())

        #print(f"Mensagens publicadas no topico: {topic_path}.")

    def callback(self,message):
        resultado = message.data
        r = resultado.decode()
        #print("Received message: {}".format(r))
        self.r = r
        message.ack()
        return r
        #if message.attributes:
        #    print("Attributes:")
        #    for key in message.attributes:
        #        value = message.attributes.get(key)
        #        print("{}: {}".format(key, value))
        #message.ack()
        
        
    def get(self, sub):
        timeout = 5.0
        subscriber = pubsub_v1.SubscriberClient()
        #topic_name = subscriber.topic_path(self.project, self.topic)
        subscription_path = subscriber.subscription_path(self.project,sub)
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=self.callback)
        with subscriber:
            try:
                streaming_pull_future.result(timeout=timeout)
            except TimeoutError:
                streaming_pull_future.cancel()  
                streaming_pull_future.result()
                #print("Deu Erro no pull da mensagem!!")
        return self.r  


    def pull(self , subscription_id):
        project_id = self.project

        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)

        NUM_MESSAGES = 20

        with subscriber:
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
                retry=retry.Retry(deadline=300),)
            
            if len(response.received_messages) == 0:
                #print("Sem Mensagens")
                return "Sem Mensagens"

            ack_ids = []
            resultado = ""
            for received_message in response.received_messages:
                resultado = received_message.message.data
                #print("Received: {}".format(received_message.message.data))
                ack_ids.append(received_message.ack_id)

            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
            r = resultado.decode()
            print("Received message: {}".format(r))
            return r




#ps = pubsub("../vmgc-pubsub.json")
#ps.set("vmgc-e-commerce","lastid")
#ps.send(399999)

#r=ps.get("lastid")
#r=ps.r
#print(r)