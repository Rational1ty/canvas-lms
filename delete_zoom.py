"""
Usage: python delete_zoom.py <auth_token> [--before <date>]
"""


import sys
import pprint
import datetime
from typing import Callable
import time
import requests


Predicate = Callable[[object], bool]


API_ROOT = 'https://canvas.tamu.edu/api/v1'
PER_PAGE = 5
ZOOM_KEYWORD = '[Recording Available]'
BEFORE_DATE = datetime.datetime(2022, 2, 7)


# takes auth token, delete keyword, and other parameters, deletes the matching messages, then
# returns the number of messages deleted
def delete_messages(token: str, keyword: str = ZOOM_KEYWORD, before: datetime.datetime = datetime.datetime.max) -> int:
	auth = {'Authorization': f'Bearer {token}'}

	deletable = get_filter(keyword, before)

	messages = requests.get(f'{API_ROOT}/conversations', {'per_page': PER_PAGE}, headers=auth)
	delete_ids = [msg['id'] for msg in messages.json() if deletable(msg)]
	
	progress_ids = []

	# start all delete batches
	for i in range(0, len(delete_ids), 500):
		delete_res = requests.put(
			f'{API_ROOT}/conversations',
			{'conversation_ids[]': delete_ids[i : i + 500], 'event': 'unstar'},
			headers=auth
		)
		pid = delete_res.json()['id']
		progress_ids.append(pid)

	# check until all batches are complete
	while not all(completed(auth, id_) for id_ in progress_ids):
		print('Waiting for messages to be starred...')
		time.sleep(0.5)

	return len(delete_ids)
		

def completed(auth: dict, progress_id: int) -> bool:
	res = requests.get(f'{API_ROOT}/progress/{progress_id}', headers=auth)
	progress = res.json()
	return progress['workflow_state'] == 'completed'


def get_filter(keyword: str, before: datetime.datetime) -> Predicate:
	def pred(msg: dict) -> bool:
		iso_str = msg['last_message_at'].replace('Z', '')
		msg_date = datetime.datetime.fromisoformat(iso_str)

		return keyword in msg['last_message'] and msg_date < before

	return pred


def main():
	args = sys.argv[1:]

	if len(args) == 0:
		print(__doc__)
		exit()
	
	n = delete_messages(args[0], before=BEFORE_DATE)
	print(f'Starred {n} messages')


if __name__ == '__main__':
	main()
