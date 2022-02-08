import argparse
import datetime


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description='A tool that helps you clean your Canvas inbox',
		usage='%(prog)s (mark | delete) <auth_token> [options...]',
		epilog='See README.md for more information')

	parser.add_argument('operation', choices={'mark', 'delete'}, metavar='(mark | delete)',
		help='operation to perform on inbox messages')
	parser.add_argument('auth_token', metavar='<auth_token>',
		help='your unique API access token')

	parser.add_argument('--keyword', default='[Recording Available]', metavar='<keyword>',
		help='only affect messages that contain certain keywords')
	parser.add_argument('--before',
		type=datetime.datetime.fromisoformat, default=datetime.datetime.max, metavar='<date>',
		help='only affect messages from before a certain date (YYYY-MM-DD format)')
	parser.add_argument('--course', metavar='<course>',
		help='only affect messages from a specific course')

	return parser.parse_args()


def guess_course(course_name: str) -> int:
	...	# TODO: use GET request to search for course that includes course_name, then return id

	
def main():
	print()
	args = parse_args()


if __name__ == '__main__':
	main()