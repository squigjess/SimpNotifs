# SimpNotifs
Listen for when a Twitch channel goes live and notify a Discord channel.

## What it does
1. Wait for a `stream.online` event from Twitch's EventSub API.
2. Once the server receives the event, trigger a Discord webhook to send a message to a specified channel.

## Preamble
I'm in the process of rewriting this app using FastAPI instead of Flask over at [squigjess/SimpNotifs2](https://github.com/squigjess/SimpNotifs2). Keep an eye there for any future updates.

## Installation
### Install Python dependencies
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Getting the app running
Installation is quite involved: due to EventSub requiring HTTPS and the fact that "subscribing" to an event isn't exactly straightforward, you won't be able to just run the script and get it working.

[This post by Kathleen Juell and Mark Drake on setting up Flask + uWSGI to serve over HTTPS](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04) as well as [this post by Kirk Haines on how to subscribe to an event via EventSub](https://www.therelicans.com/wyhaines/twitch-eventsub-the-direct-approach-to-getting-started-with-it-3pia) were my bibles in writing SimpNotifs. Rather than repeat what they've all written, I'm going to suggest following the tutorials in the above articles to set up a Flask + uWSGI + Nginx stack, replacing the content of the files in these tutorials with those from this repository.

### Setting up your secrets
Between the Twitch API and the Discord webhook, there's a few things in here that should remain secret. I've provided the template for you to fill in yourself, but the comments in there don't go into much depth:

* `EVENTSUB_SECRET` is a string that you yourself will define. It's used to encode the verification challenge when subscribing to the event via EventSub.
* `TWITCH_CLIENT_ID` is the Client ID found in the Twitch dev portal under **Client ID**.
* `TWITCH_CLIENT_SECRET` is also found in the Twitch dev portal, instead under **Client Secret**.
* `TWITCH_ACCESS_KEY` is an OAuth key that you need to authenticate to the Twitch EventSub API; without it, you will not be able to make any requests to the API. [You can find out how to generate one here.](https://www.therelicans.com/wyhaines/twitch-eventsub-the-direct-approach-to-getting-started-with-it-3pia#:~:text=To%20get%20your%20very%20own%20shiny%2C%20new%20Application%20Access%20Token%2C%20you%20need%20to%20make%20a%20POST%20request%20to%20the%20Twitch%20API.%20The%20documentation%20detailing%20what%20is%20needed%20is%20in%20the%20link%20above%2C%20but%20it%20has%20the%20potential%20to%20be%20a%20little%20bit%20confusing.)
* `DISCORD_WEBHOOK_URL` is what it says on the tin. SimpNotifs will use this URL when it sees the channel go online. You can set this up in your Discord server under **Server Settings > Integrations > Webhooks**.

### Other considerations
* EventSub doesn't actually trigger the `stream.online` webhook until the stream has been online for around a minute, sometimes more. Keep this in mind when testing!
* ~~While setting up this application (if you're gutsy enough to do so), consider setting up the Twitch CLI tool for testing. It's a little unwieldy, but saved my life a few times.~~
  - Due to the Twitch CLI tool not sending a signature with its requests, SimpNotifs treats it as having a missing header and will refuse to process the request.
  - I'm trying to think of a safe way to allow the test requests through _only if they're from the actual official Twitch CLI tool_, but it potentially opens up the ability for fake, unsigned requests to come through. 
* `config.ini` is set up to save logs to `/var/log/uwsgi/`; ensure this directory is created and that you have ownership of the directory with sudo `chown -R $USER:$USER /var/log/uwsgi` (assuming you're following the above articles and allowing the Flask app to run under your user account).
* Twitch's EventSub API will only work over HTTPS. Save yourself the trouble and don't bother running this without Nginx and a HTTPS certificate.

## Roast me
I still consider myself pretty green when it comes to developing anything more than a Linux one-liner, so PRs and comments are always welcomed and appreciated!
