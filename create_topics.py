from confluent_kafka import admin
from typing import Union

consumer_config = {
    'bootstrap.servers': 'localhost:9092'
}

# Admin client instantiation 
client = admin.AdminClient(consumer_config)

# Function for creating topics
def create_new_topics(names: Union[str, list], partitions: int = 1, replication: int = 1):
    if isinstance(names, str):
        names = names.split(',')
    new_topics = [admin.NewTopic(name, partitions, replication) for name in names]
    
    # Accessing admin create_topics via admin client 
    
    fs = client.create_topics(new_topics, validate_only=False)

    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

#Calling the above utils function for topic creation 

topics=["sqs"]
create_new_topics(topics)  