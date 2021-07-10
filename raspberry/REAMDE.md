# Installation

- Place Unipharm.py and Unipharm_config.json on the raspberry pi's desktop
- Edit Unipharm_config.json
  - "identifier"- Used to identify the forklift
  - "side" - side w.r.t. the fortlift
  - "server_url" - server IP address or URL
  - "username" - server username (configurable)
  - "password" - passwoerd for the server
  - "port" - sever code port
  - "video_length" - length of video to be sent to the server (recommended 10 seconds)
  - "framerate" - camera frame rate (recommended 30)
- Edit the rc.local and add there the following line:
  `sudo python3 /home/pi/Desktop/Unipharm.py`
  This will make the code run on startup.

# Usage

- If properly configured, once the module powers up it should connect to the server, take videos and send them to the server for processing until shutdown.
