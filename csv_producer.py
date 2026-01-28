from google.cloud import pubsub_v1      # pip install google-cloud-pubsub  ##to install
import glob                             # for searching for json file 
import json
import os 
import csv

# Search the current directory for the JSON file (including the service account key) 
# to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
files=glob.glob("*.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=files[0];

# Set the project_id and topic name
project_id=""; # Removed for security reasons
topic_name = "sensor-data";

# create a publisher and get the topic path for the publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
print(f"Publishing messages to {topic_path}.")

# Read the CSV file and iterate over the records
with open('Labels.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    for row in csv_reader:
        # Convert each record (row from the CSV file) into a dictionary
        record = {
            'time': row['time'],
            'profileName': row['profileName'],
            'temperature': row['temperature'] if row['temperature'] else None,
            'humidity': row['humidity'] if row['humidity'] else None,
            'pressure': row['pressure'] if row['pressure'] else None
        }
        
        # Serialize the dictionary into a message
        record_value=json.dumps(record).encode('utf-8');
        
        # Publish the message to the topic
        try:    
            future = publisher.publish(topic_path, record_value);
            
            #ensure that the publishing has been completed successfully
            future.result()    
            print("The message {} has been published successfully".format(record))
        except: 
            print("Failed to publish the message")
