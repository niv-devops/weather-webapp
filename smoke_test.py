# Approved by: Arin
import requests
import sys

TIMEOUT = 5

def availability_check(url):
    try:
        response = requests.get(url, verify=False, timeout=5)
        if 200 <= response.status_code < 300:
            print(f"The website in {url} is reachable.")
            return True
        else:
            print(f"The website in {url} is unreachable, status code {response.status_code}.")
            return False
     
    except requests.ConnectionError as e:
        print(f"The website in {url} is unreachable, Error: {str(e)}")
        return False

    except requests.exceptions.Timeout as e:
        print(f"Website in {url} is uneachable, connection timed out after {TIMEOUT} seconds.")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"The website in {url} is unreachable, Error: {str(e)}")
        return False


if __name__ == "__main__":  
    if availability_check("https://54.93.99.66:9090"):
        sys.exit(0)
    else:
        sys.exit(1)
