'''Defines the API endpoints, handles incoming event triggers, sends outgoing
webhook triggers '''

from flask import Flask, request, Response
import json
import api_utils
import os
import secrets # A file declaring strings that match up to secrets, keys, and IDs.

app = Flask(__name__)

# Callback URL for subscribing to an event via EventSub.
@app.route("/callback", methods = ['POST'])
def handleCallback():
    # Put request data into a dict for easier access.
    requestData = request.get_json(force=True)

    print(request.headers)
    print(json.dumps(requestData,indent=4))

    # If the response is for subscription verification...
    if request.headers["Twitch-Eventsub-Message-Type"] == "webhook_callback_verification" and request.headers["Twitch-Eventsub-Subscription-Type"] == "stream.online":
        # Check if the signature given in the callback response matches.
        # https://dev.twitch.tv/docs/eventsub#verify-a-signature
        doesSignatureMatch = api_utils.verifyChallenge(
            secrets.EVENTSUB_SECRET,
            request.headers["Twitch-Eventsub-Message-Id"]+request.headers["Twitch-Eventsub-Message-Timestamp"]+request.data.decode("utf-8"),
            request.headers["Twitch-Eventsub-Message-Signature"]
        )
        # If the calculated signature matches the one sent by EventSub, respond to EventSub with the expected response.
        # At this point, the subscription is now registered and active!
        if doesSignatureMatch == True:
            return Response(requestData["challenge"], status=200)
        elif doesSignatureMatch == False: # Signature did not match. EventSub expects a 403
            return Response("Signature did not match :(", status=403)

    # If the response is a stream.online notification...
    elif request.headers["Twitch-Eventsub-Message-Type"] == "notification" and request.headers["Twitch-Eventsub-Subscription-Type"] == "stream.online":
        print("Stream is online")
        # Begin handling the stream.online event.
        return Response("Stream online", status=200)
    else:
        return Response("Invalid", status=403)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
