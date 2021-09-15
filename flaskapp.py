"""Defines the API endpoints, handles incoming event triggers, sends outgoing webhook triggers."""

from flask import Flask, request, Response
import requests
import json
from api_utils import containsExpectedHeaders, verifyChallenge, headers
import secrets # A file declaring strings that match up to secrets, keys, and IDs.

# Accepts "\@here", "\@everyone", or a role ID as a string (looks like "<@&00000000>", which you can get by mentioning \@ROLENAME in your server).
# Also accepts "" if you want nobody at all to be pinged
roleToPing = ""

app = Flask(__name__)
@app.route("/callback", methods = ["POST"])
def handleCallback():
    # Serialise request data into a dict for easier access.
    requestData = request.get_json(force=True)

	print(json.dumps(requestData, indent=4))
    print(request.headers)

    # First off, check if the necessary headers are present.
    # TODO: find a clean, neat way to have containsExpectedHeaders() return [bool, missingHeader]
    if not containsExpectedHeaders(request.headers):
        return Response("Malformed request, missing expected headers.", status=403)

    # If all necessary headers are present, we can start checking if the signature given in the callback response is valid.
    # https://dev.twitch.tv/docs/eventsub#verify-a-signature
    doesSignatureMatch = verifyChallenge(secrets.EVENTSUB_SECRET,
                                         request.headers[headerType["msgID"]]+request.headers[headerType["msgTimestamp"]]+request.data.decode("utf-8"),
                                         request.headers[headerType["msgSignature"]])
    # Begin processing the callback request...
    if not doesSignatureMatch:
        return Response("Signature did not match.", status=403)

    if request.headers[headerType["subType"]] != "stream.online":
        return Response("Invalid request type.", status=403)

    # Is this a callback for registering a new stream.online event subscription?
    if request.headers[headerType["msgType"]] == "webhook_callback_verification":
        return Response(requestData["challenge"], status=200)

    # Is the response an actual stream.online event?
    if request.headers[headerType["msgType"]] == "notification":
        # Paramters for the webhook "bot".
        streamerName = requestData["event"]["broadcaster_user_name"]
        streamURL    = "https://twitch.tv/{}".format(streamerName)
        botName      = "SimpNotifs"
        botMessage   = ":red_circle: **{name} is online!**\n{url}\n{role}".format(name=streamerName,
                                                                                  url=(streamURL+"\n")*3,
                                                                                  role=roleToPing
        print("Stream online: {}".format(streamerName)) # For grep-ing logs
        # Send a request to a Discord Webhook.
        r = requests.post(secrets.DISCORD_WEBHOOK_URL,
                          data = {"username" : botName,
                                  "content"  : botMessage})
        return Response("Stream online", status=200)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
