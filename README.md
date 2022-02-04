# Canvas - Mark All Messages as Read

A way to easily clear unread notifications using the Canvas LMS API

## Usage

After downloading this repo (go to Code > Download Zip), run the program with `python`:
```sh
python mark_as_read.py <auth_token>
```

You can also just do it yourself using `curl` (no need to download):

```sh
curl -X POST -H "Authorization: Bearer <auth_token>" \
https://canvas.tamu.edu/api/v1/conversations/mark_all_as_read
```

The Python program has better output and some error checking, but besides that these two methods are basically the same

## How to get an auth token

- Log in to [Canvas](https://canvas.tamu.edu)
- Click on Account > Settings
- Scroll down to "Approved Integrations"
- Click "New Access Token"
- Enter "API Access" or something similar for Purpose
- Click "Generate Token", then copy the string that is returned
- Remember to save the token somewhere in case you need it again