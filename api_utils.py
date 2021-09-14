"""Utility functions"""
import hmac
import hashlib

expectedHeaders = [
    "Twitch-Eventsub-Message-Id",
    "Twitch-Eventsub-Message-Timestamp",
    "Twitch-Eventsub-Message-Signature",
    "Twitch-Eventsub-Subscription-Type",
    "Twitch-Eventsub-Message-Type"
]

def verifyChallenge(secret, digest, sentsignature):
    """Takes a digest, encodes it with HMAC SHA256, then compares it to sentSignature for verification"""
    calculatedSignature = hmac.new(secret.encode("utf-8"), digest.encode("utf-8"), hashlib.sha256).hexdigest()
    calculatedSignatureCheck = "sha256={}".format(calculatedSignature)
    return calculatedSignatureCheck == sentsignature

def containsExpectedHeaders(requestHeaders):
    """Checks the incoming request's headers to see if the expected headers are present"""
    for header in expectedHeaders:
        if header not in requestHeaders:
			print("Header missing: {}".format(header)) # For grep-ing logs
            return False
    return True
