# FastAPI MQTT App

This is a FastAPI-based application that integrates with an MQTT broker to publish and subscribe to messages. It provides a simple API for managing events and communicating with the MQTT broker.

## Features

- Publish events to an MQTT broker.
- Subscribe to topics and handle incoming messages.
- Built with FastAPI for high performance and ease of use.

## Requirements

- Python 3.10 or higher
- MQTT broker (e.g., Mosquitto)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SudeeraDilshan/mosquitto_mqtt_app.git
   cd fastapi_mqtt_app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file with your MQTT broker details:
   ```env
   MQTT_BROKER_URL=localhost
   MQTT_BROKER_PORT=1883
   MQTT_USERNAME=your_username
   MQTT_PASSWORD=your_password
   CONTROLLER_TOPIC=your_controller_topic
   ```

## Usage

1. Start the application:
   ```bash
   python src/server.py
   ```

2. Access the API documentation at `http://localhost:8000/docs`.

3. Use the `/event/publish` endpoint to publish events to the MQTT broker.

## Project Structure

- `src/`: Contains the main application code.
  - `controllers/`: Handles API logic.
  - `models/`: Defines data models.
  - `services/`: Contains the MQTT service for broker communication.
- `tests/`: Placeholder for test cases.
- `.env`: Configuration file for environment variables.

## License

This project is licensed under the MIT License.
