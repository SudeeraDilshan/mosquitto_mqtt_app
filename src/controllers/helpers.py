import requests

async def fetch_services_data():
    """
    Fetch data from the Consul agent services endpoint.
    """
    url = "http://159.65.15.16:8500/v1/agent/services"
    
    try:
        response = await requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}