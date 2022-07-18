import logging
import tornado.ioloop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line
from .handler import MeltyStateHandler

log = logging.getLogger(__name__)

define('debug', type=bool, default=False, help='Auto Reloads when files are changed.')
define('port', type=int, default=8080, help='Port to listen on.')

class JavascriptFileHandler(StaticFileHandler):
	def get_content_type(self) -> str:
		assert self.absolute_path is not None

		# Quick hack to make sure Javascript files are application/javascript
		if self.absolute_path.endswith('.js'):
			return 'application/javascript'
		
		return super().get_content_type()

def make_app():
	return Application(
		[
			(r'/state', MeltyStateHandler),
			(
				r'/(.*)',
				JavascriptFileHandler,
				{'path': 'static', 'default_filename': 'index.html'},
			)
		],
		debug=options.debug,
	)

def main():
	parse_command_line()
	app = make_app()
	app.listen(options.port)
	log.info('Listening on port: %s', options.port)
	if options.debug:
		log.warning('Running in Debug Mode!')
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()