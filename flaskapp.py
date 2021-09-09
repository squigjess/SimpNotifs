'''Defines the API endpoints, handles incoming event triggers, sends outgoing
webhook triggers '''

from flask import Flask, request, Response
import json
import api_utils
import secrets # A file declaring strings that match up to secrets, keys, and IDs.

app = Flask(__name__)

# Callback URL for subscribing to an event via EventSub.
@app.route("/callbacks/subscribe", methods = ['POST'])
def handleCallback():
    # Put request data into a dict for easier access.
    requestData = request.get_json(force=True)

    # Check if the signature given in the callback response matches.
    # https://dev.twitch.tv/docs/eventsub#verify-a-signature
    doesSignatureMatch = api_utils.verifyChallenge(
        secrets.sub_secret,
        request.headers["Twitch-Eventsub-Message-Id"]+request.headers["Twitch-Eventsub-Message-Timestamp"]+request.data.decode("utf-8"),
        request.headers["Twitch-Eventsub-Message-Signature"]
    )

    # If the calculated signature matches the one sent by EventSub, respond to EventSub.
    # At this point, the subscription is now registered and active!
    if doesSignatureMatch == True:
        return Response(requestData["challenge"], status=200)
    elif doesSignatureMatch == False:
        return Response("Signature did not match :(", status=403)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
