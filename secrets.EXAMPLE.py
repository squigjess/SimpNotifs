'''Secrets, keys, and IDs that should be concealed.
   See the README for more information.'''

EVENTSUB_SECRET      = "foo"
TWITCH_CLIENT_ID     = "bar"
TWITCH_CLIENT_SECRET = "baz"
TWITCH_ACCESS_KEY    = "qux"
DISCORD_WEBHOOK_URL  = "thud"

if __name__ == "__main__":
    print("EVENTSUB_SECRET      : {}".format(EVENTSUB_SECRET))
    print("TWITCH_CLIENT_ID     : {}".format(TWITCH_CLIENT_ID))
    print("TWITCH_CLIENT_SECRET : {}".format(TWITCH_CLIENT_SECRET))
    print("TWITCH_ACCESS_KEY    : {}".format(TWITCH_ACCESS_KEY))
    print("DISCORD_WEBHOOK_URL  : {}".format(DISCORD_WEBHOOK_URL))
