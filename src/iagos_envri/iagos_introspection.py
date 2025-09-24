"""
ENVRI-ID Token Introspection Demonstration
==========================================

This script demonstrates ENVRI-ID token introspection by the AERIS SSO system.
It shows how ENVRI-ID tokens are validated when accessing protected AERIS resources
through the IAGOS API for IAGOS atmospheric data.

The token introspection process:
1. ENVRI-ID token is obtained (manually or via OAuth2)
2. Token is sent to AERIS-protected IAGOS API
3. AERIS SSO validates the token through introspection
4. Access is granted/denied based on token validity
"""

import requests
import time

SERVICE_URL = "https://api.sedoo.fr/iagos-backend-test/v2.0/downloads"
AUTH_BASE_URL = "https://login.staging.envri.eu/auth/realms/envri/protocol/openid-connect"


def getHeader():
    """
    Manual ENVRI-ID token input for AERIS SSO introspection demo.

    The entered token will be validated by AERIS SSO when making API calls
    to demonstrate the token introspection mechanism.
    """
    token = input("Please fill your ENVRI-ID token :")
    return {'Authorization': 'Bearer ' + token, 'Accept': 'application/octet-stream'}


def getHeaderOAuth():
    """
    OAuth2 Device Authorization Grant flow for ENVRI-ID token introspection demo.

    This function demonstrates the complete OAuth2 flow with ENVRI-ID:
    1. Device authorization request to ENVRI SSO
    2. User authentication via browser
    3. Token acquisition and validation
    4. Token will be introspected by AERIS SSO when accessing protected resources
    """
    # Step 1: Request device authorization
    print("Initiating OAuth2 device flow...")

    device_response = requests.post(
        f"{AUTH_BASE_URL}/auth/device",
        data={
            "client_id": "envri-token-cli",
            "scope": "openid profile email entitlements"
        }
    )

    if device_response.status_code != 200:
        raise Exception(f"Device authorization request failed: {device_response.text}")

    device_data = device_response.json()

    # Display user instructions
    print(f"\nPlease open this URL in your browser:")
    print(f"{device_data['verification_uri_complete']}")
    print(f"\nWaiting for authentication... (expires in {device_data['expires_in']} seconds)")

    # Step 2: Poll for access token
    device_code = device_data['device_code']
    interval = device_data['interval']

    while True:
        token_response = requests.post(
            f"{AUTH_BASE_URL}/token",
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": "envri-token-cli"
            }
        )

        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data['access_token']
            print("✓ Authentication successful!")
            return {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/octet-stream'}

        elif token_response.status_code == 400:
            error_data = token_response.json()
            error_type = error_data.get('error')

            if error_type == 'authorization_pending':
                print("⏳ Still waiting for authorization...")
                time.sleep(interval)
                continue
            elif error_type == 'slow_down':
                interval += 5
                print(f"⏳ Slowing down polling to {interval}s intervals...")
                time.sleep(interval)
                continue
            elif error_type == 'expired_token':
                raise Exception("Device code expired. Please restart the authentication process.")
            elif error_type == 'access_denied':
                raise Exception("Access denied by user.")
            else:
                raise Exception(f"Authentication error: {error_data}")

        else:
            raise Exception(f"Token request failed: {token_response.status_code} - {token_response.text}")


def downloadOneFlight(flight, output_dir, use_oauth=False):
    """
    Download service demonstrating ENVRI-ID token introspection by AERIS SSO.

    This function makes authenticated requests to the AERIS-protected IAGOS API.
    The ENVRI-ID token is introspected by AERIS SSO to validate access rights
    before allowing data download.

    Args:
        flight (str): Flight ID to download
        output_dir (str): Directory to save the NetCDF file
        use_oauth (bool): Use OAuth2 flow instead of manual token input

    The introspection process occurs when the token is validated by AERIS SSO
    during the API request to the protected IAGOS endpoint.
    """
    # Get ENVRI-ID token (manual input or OAuth2 flow)
    headers = getHeaderOAuth() if use_oauth else getHeader()

    # Make authenticated request to AERIS-protected IAGOS API
    # AERIS SSO will perform token introspection to validate the ENVRI-ID token
    response = requests.get(SERVICE_URL + "/" + flight + "?level=2&format=netcdf&type=timeseries", headers=headers, stream=True)
    
    # If request worked read response and write it in output dir.
    output_file = output_dir + "/" + flight + ".nc"
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"File downloaded : {output_file}")
    # Else print error
    else:
        print(f"Error {response.status_code}: {response.text}")


def main():
    """
    Main CLI entry point for the ENVRI-ID token introspection demo.

    This function demonstrates ENVRI-ID token introspection by AERIS SSO through
    OAuth2 device flow and protected API access.
    """
    print("=== OAuth2 Device Flow Demo ===")
    print("This demonstrates ENVRI-ID token acquisition and introspection by AERIS SSO")
    response = downloadOneFlight("2023050203041714", "/tmp/", use_oauth=True)
    return response


if __name__ == '__main__':
    """
    Main execution demonstrating ENVRI-ID token introspection by AERIS SSO.

    This script shows two authentication methods for accessing AERIS-protected resources:
    1. Manual token input - demonstrates direct token introspection
    2. OAuth2 device flow - demonstrates full OAuth2 lifecycle with token introspection

    Both methods result in AERIS SSO performing token introspection to validate
    the ENVRI-ID token before granting access to IAGOS API resources.
    """

    # Example with manual token input (uncomment to test)
    # print("=== Manual Token Input Demo ===")
    # response = downloadOneFlight("2022010112355202", "/tmp/")

    # Example with OAuth2 device flow (demonstrates full token lifecycle)
    main()


