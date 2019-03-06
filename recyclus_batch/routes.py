from flask import Blueprint, request, current_app as app
from flask_restplus import Api, Resource
from webargs.flaskparser import use_args

from .schema import run_args, cancel_args
from . import jobs

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Recyclus simulation service',
          version='1.0',
          description='Remote cyclus simulation services api',
          doc='/doc/')


@api.route('/run')
class Run(Resource):
    @use_args(run_args)
    def post(self, args):
        identity = args.pop('identity')
        if args.get('user') is None:
            args['user'] = identity['user']
        return jobs.create(args)


@api.route('/cancel/<jobid>')
class Cancel(Resource):

    @use_args(cancel_args)
    def delete(self, args, jobid):
        return jobs.cancel(jobid, args['identity']['user'])


@api.route('/status/<jobid>')
class Status(Resource):

    # @use_kwargs(StatusSchema())
    def get(self, jobid):
        return jobs.status(jobid)

