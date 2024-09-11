import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import folium
import datetime
import os

# this method will return us our actual coordinates using our ip address
def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
    except Exception as e:
        print(f"An error occurred while retrieving location data: {e}")
        exit()

# this method will fetch our coordinates and create a html file of the map
def gps_locator():
    obj = folium.Map(location=[0, 0], zoom_start=2)
    try:
        lat, long, city, state = locationCoordinates()
        print(f"You Are in {city}, {state}")
        print(f"Your latitude = {lat} and longitude = {long}")
        folium.Marker([lat, long], popup='Current Location').add_to(obj)

        # Ensure directory exists
        directory = 'C:/screengfg/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        fileName = f"{directory}Location{datetime.date.today()}.html"
        
        # Test saving a simple file
        with open(fileName, 'w') as f:
            f.write("<html><body>Test file creation successful.</body></html>")

        obj.save(fileName)
        return fileName
    except Exception as e:
        print(f"An error occurred while creating the map: {e}")
        return False

# Main method
if __name__ == "__main__":
    print("---------------GPS Using Python---------------\n")
    page = gps_locator()
    if page:
        print("\nOpening File.............")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional: Run in headless mode if no GUI available
        dr = webdriver.Chrome(options=chrome_options)
        dr.get(f"file:///{page}")
        dr.quit()
        print("\nBrowser Closed..............")
    else:
        print("Failed to generate the map.")

