# SimpNotifs
Listen for when a Twitch channel goes live and notify a Discord channel.

## What it does
1. Wait for a `stream.online` event from Twitch's EventSub API.
2. Once the server receives the event, trigger a Discord webhook.
