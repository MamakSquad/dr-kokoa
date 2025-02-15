import geocoder
import googlemaps
import webbrowser
import os

class HealthNavi:
    def __init__(self):
        self.api_key = "AIzaSyC2KPlLyT24z1HObpzeL69_NCSIwC1aU5U"  
        self.gmaps = googlemaps.Client(key=self.api_key)

    def get_location(self):
        """Retrieve the current GPS coordinates using geocoder."""
        g = geocoder.ip('me')  # Fetches current location using IP
        if g.latlng is not None:
            lat, lng = g.latlng
            print(f"User 's Location: Latitude={lat}, Longitude={lng}")
            return lat, lng
        else:
            print("Unable to retrieve GPS coordinates.")
            return None, None  # Return None if location cannot be retrieved

    def find_nearest_healthcare(self):
        """Finds the nearest healthcare providers based on the user's location."""
        lat, lng = self.get_location()
        if lat is None or lng is None:
            print("Cannot find healthcare providers without valid location.")
            return None, None, []

        places_result = self.gmaps.places_nearby(location=(lat, lng), radius=5000, type="hospital")

        places_list = []
        if "results" in places_result:
            print("\nNearest Healthcare Providers:\n")
            for idx, place in enumerate(places_result["results"][:5], start=1):
                name = place["name"]
                address = place.get("vicinity", "No address found")
                place_id = place["place_id"]
                details = self.gmaps.place(place_id=place_id)
                phone_number = details["result"].get("formatted_phone_number", "No phone number")
                rating = details["result"].get("rating", "No rating")
                lat_dest = place["geometry"]["location"]["lat"]
                lng_dest = place["geometry"]["location"]["lng"]

                places_list.append((name, address, lat_dest, lng_dest))
                print(f"{idx}. {name}\n   Address: {address}\n   Phone: {phone_number}\n   Rating: {rating}\n")

            return lat, lng, places_list
        else:
            print("No healthcare providers found nearby.")
            return lat, lng, []

    def launch_navigation(self, user_lat, user_lng, dest_lat, dest_lng):
        """Launches Google Maps navigation to the selected healthcare provider."""
        url = f"https://www.google.com/maps/dir/{user_lat},{user_lng}/{dest_lat},{dest_lng}/"
        print(f"Opening Google Maps: {url}")
        webbrowser.open(url)

    def navigate_to_healthcare(self):
        """Main method to find and navigate to healthcare providers."""
        user_lat, user_lng, healthcare_list = self.find_nearest_healthcare()

        if healthcare_list:
            try:
                choice = int(input("\nEnter the number of the place you want to navigate to: "))
                if 1 <= choice <= len(healthcare_list):
                    selected_place = healthcare_list[choice - 1]
                    print(f"Navigating to {selected_place[0]} at {selected_place[1]}...")
                    self.launch_navigation(user_lat, user_lng, selected_place[2], selected_place[3])
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

# Example usage
if __name__ == "__main__":
    health_navi = HealthNavi()
    health_navi.navigate_to_healthcare()

