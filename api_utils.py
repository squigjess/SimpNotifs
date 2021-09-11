"""Utility functions"""
import hmac
import hashlib

def verifyChallenge(secret, digest, sentsignature):
    """Takes a digest, encodes it with HMAC SHA256, then compares it to sentSignature for verification"""
    calculatedSignature = hmac.new(secret.encode("utf-8"), digest.encode("utf-8"), hashlib.sha256).hexdigest()
    calculatedSignatureCheck = "sha256={}".format(calculatedSignature)
    return calculatedSignatureCheck == sentsignature
