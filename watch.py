# pylint: skip-file
import os
from dotenv import load_dotenv
from flask import Flask, request
from huggingface_hub import HfApi

load_dotenv()

USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")
OWNER = os.getenv("OWNER")
NAME = os.getenv("NAME")

api = HfApi()

app = Flask(__name__)

# Define a route to handle webhook requests
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    data = request.json
    print (data)
    # Parse the message from the data
    message = data['message']
    # Split the message by newline characters
    lines = message.split('\n')
    # Loop through the lines
    for line in lines:
        image_name = os.getenv('IMAGE_NAME')
        # Check if the line contains the image name
        if image_name in line:
            # Split the line by spaces
            words = line.split()
            # Get the action and the container name
            action = words[0]
            container_name = words[-1]
            # Check if the action is update
            if action == 'Found':
                # Print some information about the event
                print(f'Container {container_name} is updating with image {image_name}')
                api.restart_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN, factory_reboot=True)
    # Return a success response
    return 'OK', 200

port=os.getenv('SERVER_PORT')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('SERVER_PORT'), debug=True)
