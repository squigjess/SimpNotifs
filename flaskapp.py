"""Defines the API endpoints, handles incoming event triggers, sends outgoing webhook triggers."""

from flask import Flask, request, Response
import requests
import json
import api_utils
from api_utils import MSG_ID, MSG_TIMESTAMP, MSG_SIGNATURE, SUBSCRIPTON_TYPE, MSG_TYPE # Constants for different header types.
import secrets # A file declaring strings that match up to secrets, keys, and IDs.

app = Flask(__name__)

@app.route("/callback", methods = ["POST"])
def handleCallback():
    # Serialise request data into a dict for easier access.
    requestData = request.get_json(force=True)

    print(json.dumps(requestData, indent=4))
    print(request.headers)

    # First off, check if the necessary headers are present.
    # TODO: find a clean, neat way to have containsExpectedHeaders() return [bool, missingHeader]
    if not api_utils.containsExpectedHeaders(request.headers):
        return Response("Malformed request, missing expected headers.", status=403)

    # If all necessary headers are present, we can start checking if the signature given in the callback response is valid.
    # https://dev.twitch.tv/docs/eventsub#verify-a-signature
    doesSignatureMatch = api_utils.verifyChallenge(secrets.EVENTSUB_SECRET,
                                         request.headers[MSG_ID]+request.headers[MSG_TIMESTAMP]+request.data.decode("utf-8"),
                                         request.headers[MSG_SIGNATURE])
    # Begin processing the callback request...
    if not doesSignatureMatch:
        return Response("Signature did not match.", status=403)

    # App only handles stream.online / streamup events, anything else will not be able to be processed.
    if request.headers[SUBSCRIPTON_TYPE] != "stream.online":
        return Response("Invalid request type.", status=403)

    # Is this a callback for registering a new stream.online event subscription?
    if request.headers[MSG_TYPE] == "webhook_callback_verification":
        return Response(requestData["challenge"], status=200)

    # Is the response an actual stream.online event?
    if request.headers[MSG_TYPE] == "notification":
        api_utils.postToDiscord(requestData["event"]["broadcaster_user_name"])
        return Response("Stream online", status=200)

if __name__ == "__main__":
    # Most likely will not work with actual live Twitch events, as EventSub only sends to certified HTTPS servers.
    app.run(host='0.0.0.0')
