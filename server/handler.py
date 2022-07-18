import logging
import json
from tornado.web import RequestHandler
from tornado.options import options
from .proc import read, look_for_melty

MELTY_HEADER = 0x400000

log = logging.getLogger(__name__)
with open('config.json') as file:
	config = json.loads(file.read())

class MeltyStateHandler(RequestHandler):
	async def get(self):
		# If the header for Melty does not exist, try to find Melty Blood.
		if read(MELTY_HEADER, 1) is None:
			# If Melty is not found, return a waiting for melty statement.
			if look_for_melty() is False:
				return json.dumps({'waiting': True})

		state_info = {
			'waiting': False
		}

		for item in config['stateInfo']:
			state_info[item['key']] = read(item['location'], item['size'])  # type: ignore

		if options.debug:
			self.add_header('Access-Control-Allow-Origin', '*')
		self.write(json.dumps(state_info))