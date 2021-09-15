"""Utility functions"""
import hmac
import hashlib

headerType = {
    "msgID"        : "Twitch-Eventsub-Message-Id",
    "msgTimestamp" : "Twitch-Eventsub-Message-Timestamp",
    "msgSignature" : "Twitch-Eventsub-Message-Signature",
    "subType"      : "Twitch-Eventsub-Subscription-Type",
    "msgType"      : "Twitch-Eventsub-Message-Type"
}

def verifyChallenge(secret, digest, sentSignature):
    """Takes a digest, encodes it with HMAC SHA256, then compares it to sentSignature for verification"""
    calculatedSignature = hmac.new(secret.encode("utf-8"), digest.encode("utf-8"), hashlib.sha256).hexdigest()
    calculatedSignatureCheck = "sha256={}".format(calculatedSignature)
    return calculatedSignatureCheck == sentSignature

def containsExpectedHeaders(requestHeaders):
    """Checks the incoming request's headers to see if the expected headers are present"""
    for header in headerType:
        if header not in requestHeaders:
			print("Header missing: {}".format(header)) # For grep-ing logs
            return False
    return True
