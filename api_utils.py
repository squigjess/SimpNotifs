"""Utility functions"""
import hmac
import hashlib
import secrets
import requests

BOT_NAME         = "SimpNotifs"
MSG_ID           = "Twitch-Eventsub-Message-Id"
MSG_TIMESTAMP    = "Twitch-Eventsub-Message-Timestamp"
MSG_SIGNATURE    = "Twitch-Eventsub-Message-Signature"
SUBSCRIPTON_TYPE = "Twitch-Eventsub-Subscription-Type"
MSG_TYPE         = "Twitch-Eventsub-Message-Type"
expectedHeaders  = [MSG_ID, MSG_TIMESTAMP, MSG_SIGNATURE, SUBSCRIPTON_TYPE, MSG_TYPE]

# Accepts "\@here", "\@everyone", or a role ID as a string (looks like "<@&00000000>", which you can get by mentioning \@ROLENAME in your server).
# Also accepts "" if you want nobody at all to be pinged
roleToPing = ""

def verifyChallenge(secret, digest, sentSignature):
    """Takes a digest, encodes it with HMAC SHA256, then compares it to sentSignature for verification"""
    calculatedSignature = hmac.new(secret.encode("utf-8"), digest.encode("utf-8"), hashlib.sha256).hexdigest()
    calculatedSignatureCheck = "sha256={}".format(calculatedSignature)
    return calculatedSignatureCheck == sentSignature

def containsExpectedHeaders(requestHeaders):
    """Checks the incoming request's headers to see if the expected headers are present"""
    for header in expectedHeaders:
        if header not in requestHeaders:
            print("Header missing: {}".format(header)) # For grep-ing logs
            return False
    return True

def postToDiscord(streamerName):
    print("Stream online: {}".format(streamerName)) # For grep-ing logs
    botMessage   = ":red_circle: **{name} is online!**\n{url}\n{role}".format(name=streamerName,
                                                                              url=("https://twitch.tv/{}\n".format(streamerName))*3,
                                                                              role=roleToPing)
    r = requests.post(secrets.DISCORD_WEBHOOK_URL,
                      data = {"username" : BOT_NAME,
                              "content"  : botMessage})
