import os
import requests
from datetime import datetime, timedelta

# Credentials
USERNAME = "asinraja42@gmail.com"
PASSWORD = "Asinraja123##"

if not USERNAME or not PASSWORD:
    raise Exception("❌ Error: Username or Password is missing! Set them as environment variables.")

# Function to get access token
def get_access_token(username, password):
    url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    payload = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    response = requests.post(url, data=payload)
    
    if response.status_code != 200:
        raise Exception(f"❌ Failed to authenticate: {response.status_code}\n{response.text}")

    return response.json()["access_token"]

# Fetch token
access_token = get_access_token(USERNAME, PASSWORD)
print("✅ Access token obtained successfully!")

# Evalscript for True Color (JPEG Output)
evalscript = """ 
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: {
      bands: 3,
      sampleType: "AUTO"
    }
  };
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
"""

# Bounding box (Ensure the image is not cut)
polygon = {
    "type": "Polygon",
    "coordinates": [[
        [-43.370988, -6.149586],
        [-44.09735, -6.149586],
        [-44.09735, -5.427551],
        [-43.370988, -5.427551],
        [-43.370988, -6.149586]
    ]]
}


# API Request URL
url = "https://sh.dataspace.copernicus.eu/api/v1/process"

# Sentinel Hub resolution limits
MAX_WIDTH = 2500
MAX_HEIGHT = 2500

# Get the latest cloud-free image (searching for the most recent image within the last 3 months)
today = datetime.utcnow()
start_date = (today - timedelta(days=360)).strftime("%Y-%m-%dT00:00:00Z")
end_date = today.strftime("%Y-%m-%dT23:59:59Z")

year = today.strftime("%Y")  # Extracting the year

request_payload = {
    "input": {
        "bounds": {
            "geometry": polygon
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": start_date,
                        "to": end_date
                    },
                    "maxCloudCoverage": 0  # Only 0% cloud images
                }
            }
        ]
    },
    "output": {
        "width": MAX_WIDTH,   # Ensuring full image is captured
        "height": MAX_HEIGHT,
        "responses": [
            {
                "identifier": "default",
                "format": {"type": "image/jpeg"}
            }
        ]
    },
    "evalscript": evalscript
}

# Set headers with Bearer Token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "image/jpeg"
}

print(f"📡 Fetching latest cloud-free image...")

# Send request
response = requests.post(url, json=request_payload, headers=headers)

# Save the image if successful
if response.status_code == 200:
    image_filename = f"{year}_latest.jpg"  # Adding year to filename
    image_path = os.path.join(image_filename)
    with open(image_path, "wb") as file:
        file.write(response.content)
    print(f"✅ Latest cloud-free image saved: {image_path}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
