"""
Usage: python mark_as_read.py <auth_token>

To get an auth token for API access:
 - Log in to Canvas (https://canvas.tamu.edu)
 - Click on Account > Settings
 - Scroll down to "Approved Integrations"
 - Click "New Access Token"
 - Enter "API Access" or something similar for Purpose
 - Click "Generate Token", then copy the string that is returned
 - Remember to save the token somewhere in case you need it again
"""

import sys
import inspect

# import with fallback
try:
	import requests
except ModuleNotFoundError:
	print()
	print(inspect.cleandoc('''
		Missing required dependency "requests"
		  Please install the requests module:
		    python -m pip install requests
		                or
		    conda install -c anaconda requests
	'''))
	exit()


API_ROOT = 'https://canvas.tamu.edu/api/v1'


def main():
	args = sys.argv[1:]

	if len(args) == 0:
		print(__doc__)
		exit()
	
	auth = {'Authorization': f'Bearer {args[0]}'}

	unread = requests.get(f'{API_ROOT}/conversations/unread_count', headers=auth)
	res = requests.post(f'{API_ROOT}/conversations/mark_all_as_read', headers=auth)

	if not (unread.ok and res.ok):
		print()
		print(inspect.cleandoc(f'''
			ERR! Request(s) failed
			ERR!   unread_count: {unread.status_code} {unread.reason}
			ERR!   mark_all_as_read: {res.status_code} {res.reason}
		'''))
		exit()

	ms = res.elapsed.microseconds // 1000

	print(f'\nMarked {unread.json()["unread_count"]} unread notifications as read ({ms} ms)')


if __name__ == '__main__':
	main()
