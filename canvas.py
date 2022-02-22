import argparse
import datetime
import pprint

import requests

API = 'https://canvas.tamu.edu/api/v1'

# request parameters
PARAMS = {
	'per_page': 20
}

# request headers
HEADERS = {
	'Authorization': 'Bearer 15924~rZnpVtsnjvHvME4y4fLHQa6Tp6i8YjtEcNdc0U9eRs6YQzuV04HWp10Yac9DwAAH',
	'Accept': 'application/json'
}


def get_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description='A tool for interacting with the Canvas LMS API',
		usage='python %(prog)s (mark | delete) [<auth_token>] [<options>...]',
		epilog='See README.md for more information')

	# required args
	parser.add_argument('operation', metavar='mark | delete', choices={'mark', 'delete'}, 
		help='operation to perform on inbox messages')
	parser.add_argument('auth_token', nargs='?',
		help='your unique API access token')

	# options
	parser.add_argument('--all', '-a', action='store_true',
		help='affect all messages')
	parser.add_argument('--keyword', metavar='<keyword>', default='[Recording Available]', 
		help='only affect messages that contain this string')
	parser.add_argument('--before', metavar='<date>',
		type=datetime.datetime.fromisoformat, default=datetime.datetime.max, 
		help='only affect messages sent before this date (YYYY-MM-DD format)')
	parser.add_argument('--after', metavar='<date>',
		type=datetime.datetime.fromisoformat, default=datetime.datetime.min, 
		help='only affect messages sent after this date (YYYY-MM-DD format)')
	parser.add_argument('--course', metavar='<course>',
		help='only affect messages from this course')

	args = parser.parse_args()

	return prepare_args(args)


def prepare_args(args: argparse.Namespace) -> argparse.Namespace:
	if not args.auth_token:
		try:
			with open('token.txt') as file:
				token = next(file).strip()
			args.auth_token = token
		except FileNotFoundError:
			error('Authentication required: auth_token must be supplied')

	# if keyword is empty string
	if args.keyword == '':
		error('Invalid keyword: keyword cannot be empty string')

	# check that dates agree
	if args.after >= args.before:
		error('Invalid date(s): --after date must precede --before date')

	# if course is empty string
	if args.course == '':
		error('Invalid course: course cannot be empty string')

	return args


def confirm(msg: str = 'Confirm?') -> bool:
	print(msg, end=' ', flush=True)
	return input('(Y/n) ') == 'Y'


def error(msg: str, prefix: str = '[ERR!]', **kwargs) -> object:
	print(prefix, msg, **kwargs)
	exit()


def guess_course(course_name: str) -> int:
	res = requests.get(f'{API}/courses', PARAMS, headers=HEADERS)
	courses = res.json()
	
	for c in courses:
		if course_name in (cn := c['name']) or course_name in c['course_code']:
			if confirm(f'Is "{cn}" the correct course?'):
				return c['id']

	raise Exception('No course found for the given name')

	
def main():
	print()
	print(get_args())


if __name__ == '__main__':
	main()
