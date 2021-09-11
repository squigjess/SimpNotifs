"""Defines the API endpoints, handles incoming event triggers, sends outgoing
webhook triggers.
"""

from flask import Flask, request, Response
import requests
import json
import api_utils
import secrets # A file declaring strings that match up to secrets, keys, and IDs.

# Accepts "\@here", "\@everyone", or a role ID as a string (looks like "<@&00000000>", which you can get by mentioning \@ROLENAME in your server).
# Also accepts "" if you want nobody at all to be pinged
roleToPing = ""

app = Flask(__name__)
@app.route("/callback", methods = ["POST"])
def handleCallback():
    # Serialise request data into a dict for easier access.
    requestData = request.get_json(force=True)

    # Check if the signature given in the callback response checks out.
    # https://dev.twitch.tv/docs/eventsub#verify-a-signature
    doesSignatureMatch = api_utils.verifyChallenge(
        secrets.EVENTSUB_SECRET,
        request.headers["Twitch-Eventsub-Message-Id"]+request.headers["Twitch-Eventsub-Message-Timestamp"]+request.data.decode("utf-8"),
        request.headers["Twitch-Eventsub-Message-Signature"]
    )
    # If the calculated signature matches the one sent by EventSub, continue processing the callback request.
    if doesSignatureMatch:
        # If the response is for subscription verification, return the challenge to activate the subscription.
        if request.headers["Twitch-Eventsub-Message-Type"] == "webhook_callback_verification" and request.headers["Twitch-Eventsub-Subscription-Type"] == "stream.online":
            return Response(requestData["challenge"], status=200)

        # If the response is a stream.online notification...
        elif request.headers["Twitch-Eventsub-Message-Type"] == "notification" and request.headers["Twitch-Eventsub-Subscription-Type"] == "stream.online":
            # These will be logged for debugging/troubleshooting purposes.
            print(request.headers)
            print(json.dumps(requestData,indent=4))

            # ...Set up paramters for the webhook "bot"...
            print("Stream is online") # For grep-ing logs
            streamerName = requestData["event"]["broadcaster_user_name"]
            streamURL    = "https://twitch.tv/{}".format(streamerName)
            botName      = "SimpNotifs"
            botMessage   = ":red_circle: **{name} is online!**\n{url}\n{role}".format(name=streamerName,
                                                                                      url=(streamURL+"\n")*3,
                                                                                      role=roleToPing)
            # ...Then send a request to a Discord Webhook.
            r = requests.post(secrets.DISCORD_WEBHOOK_URL, data = {
                "username" : botName,
                "content"  : botMessage})
            return Response("Stream online", status=200)

        else: # Return a 403 if we get a message type + subscription type combo we can't handle.
            return Response("Invalid/unhandled request type", status=403)

    elif not doesSignatureMatch: # Signature did not match. EventSub expects a 403.
        return Response("Signature did not match :(", status=403)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
