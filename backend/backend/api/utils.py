import base64
import hashlib
import hmac
import logging
import os

import requests
from requests.packages.urllib3.util import parse_url

from django.conf import settings

from .ml import predict

log = logging.getLogger(__name__)


def sign_url(input_url=None, key=None, client_secret=None):
    """ Sign a request URL with a Crypto Key.
      Usage:
      from urlsigner import sign_url
      signed_url = sign_url(input_url=my_url,
                            key=key,
                            client_secret=CLIENT_SECRET)
      Args:
      input_url - The URL to sign
      key - Your Client ID
      client_secret - Your Crypto Key
      Returns:
      The signed request URL
  """
    # Return if any parameters aren't given
    if not input_url or not key or not client_secret:
        return None

    # Add the Client ID to the URL
    input_url += "&key=%s" % (key)

    url = parse_url(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(client_secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, url_to_sign.encode(), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()


def get_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        filename = os.path.join(settings.MEDIA_ROOT, "upload.png")
        log.info(f"Google image file: {filename}")
        print(
            f"------------------------------------------------------ Google image file: {filename}"
        )
        with open(filename, "wb") as f:
            f.write(response.content)

        return filename
    except Exception as e:
        log.exception(e)

    return None


def get_image_from_coordinate(lat, long):
    base_url = "".join(
        [
            "https://maps.googleapis.com/maps/api/staticmap?center=",
            str(lat),
            ",",
            str(long),
            "&zoom=13&size=200x200&maptype=satellite&sensor=false&scale=1",
        ]
    )

    url = sign_url(
        base_url,
        "AIzaSyDW6cuT1zime0ZKVjjiPdytH0Zw3Lu-zng",
        "csXUTpXVywdChe162O39li2jKAM=",
    )

    log.info(f"------------------------------------------- {url}")
    print(f"------------------------------------------- {url}")

    return get_image(url)
