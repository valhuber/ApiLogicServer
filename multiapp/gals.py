from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from admin_api import create_app as create_admin_api_app, User, Api
from flask import Flask
import multiprocessing
import gunicorn.app.base
from multiapp import get_args


class ServerApp(gunicorn.app.base.BaseApplication):
    application = None

    def __init__(self, args, options=None):
        self.args = args
        self.options = options or {}
        if not hasattr(self, "application"):
            self.application = self.load_multiapp()
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.load_multiapp()
    
    def load_multiapp(self):
        print("\n\n  # Loading MA\n\n")
        from multiapp import create_app
        return create_app(self.args)
    
    def post_response(worker, req, environ, resp):
        fdsqfdsq
        worker.log.debug("%s", worker.pid)


if __name__ == '__main__':
    
    args = get_args()
    
    options = {
        'bind': '%s:%s' % (args.interface, args.port),
        'workers': args.workers,
        'threads' : args.threads,
        'error-logfile' : args.error_log,
        'access-logfile' : args.access_log,
        'reload' : True
    }
    #args.application = create_app(args)
    server = ServerApp(args, options)
    server.run()


