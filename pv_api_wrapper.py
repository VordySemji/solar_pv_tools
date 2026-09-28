import requests
import os
def get_solar_production(lat, lon, system_capacity, tilt=20, azimuth=180):
    """Fetch PVWatts production estimate for a given location and system size."""
    api_key = os.environ.get("NREL_API_KEY")
    url = "https://developer.nlr.gov/api/pvwatts/v8.json"
    params = {
        "api_key": api_key,
        "lat": lat,
        "lon": lon,
        "system_capacity": system_capacity,
        "azimuth": azimuth,
        "tilt": tilt,
        "array_type": 1,
        "module_type": 0,
        "losses": 14,
    }
    
    response = requests.get(url, params=params)
    result = response.json()
    if result['errors']:
        raise ValueError(result['errors'])
    return result


result = get_solar_production(lat=17.9712, lon=-76.7936, system_capacity=5)
print(f"Jamaica's annual production: {result['outputs']['ac_annual']:.2f} kWh")

result2 = get_solar_production(lat=40.7128, lon=-74.0060, system_capacity=8)
print(f"New York's annual production: {result2['outputs']['ac_annual']:.2f} kWh")

try:
    bad_result = get_solar_production(lat=999, lon=-76.7936, system_capacity=5)
    print(f"Bad location production: {bad_result['outputs']['ac_annual']:.2f} kWh")
except ValueError as e:
    print(f"An error occurred: {e}")