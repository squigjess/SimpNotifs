'''Utility functions'''
import hmac
import hashlib

def verifyChallenge(secret, digest, sentsignature):
    calculatedSignature = hmac.new(secret.encode("utf-8"), digest.encode("utf-8"), hashlib.sha256).hexdigest()
    calculatedSignatureCheck = "sha256={}".format(calculatedSignature)
    if calculatedSignatureCheck == sentsignature:
        return True
    elif calculatedSignatureCheck != sentsignature:
        return False
