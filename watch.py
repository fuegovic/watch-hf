# pylint: skip-file
import os
from dotenv import load_dotenv
from flask import Flask, request
from huggingface_hub import HfApi
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")
OWNER = os.getenv("OWNER")
NAME = os.getenv("NAME")

api = HfApi()

app = Flask(__name__)

# Initialize a global variable to store the service state
service_state = 'Unknown'

# Define a function to restart the space if the service state is 'Down'
def restart_space():
    global service_state
    if service_state == 'Down':
        print('Attempting to restart space: 'f"{OWNER}/{NAME}")
        api.restart_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN)

# Create a background scheduler to run the restart_space function every 2 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(restart_space, 'interval', minutes=2)
scheduler.start()


@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the raw data from the request
    raw_data = request.data.decode('utf-8')
    # Check if 'Watchtower' is in the raw data
    if 'Watchtower' in raw_data:
        # Process as watchtower notification
        data = request.json
        print(data)
        message = data['message']
        lines = message.split('\n')
        for line in lines:
            image_name = os.getenv('IMAGE_NAME')
            if image_name in line:
                words = line.split()
                action = words[0]
                container_name = words[-1]
                if action == 'Found':
                    print(f'Container {container_name} is updating with image {image_name}')
                    api.restart_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN, factory_reboot=True)

    else:
        # Print other notifications to the console
        data = request.json
        print(f'Notification: {data}')
        if 'msg' in data:
            # Update the global service_state variable based on the msg field
            global service_state
            if 'Down' in data['msg']:
                service_state = 'Down'
            elif 'Up' in data['msg']:
                service_state = 'Up'
            else:
                service_state = 'Unknown'
            print(f'Service state: {service_state}')
    # Return a success response
    return 'OK', 200

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('SERVER_PORT', '5000'), debug=os.getenv('DEBUG', 'false'))
