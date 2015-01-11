#!/usr/bin/env python
import argparse
import subprocess

class DatabaseExporter(object):
	args = None
	def __init__(self, args):
		self.args = args
	def postgres(self):
		if not self.args.database:
			raise AttributeError('No database selected to backup')
		port = args.port or '5432'
		postfix = ' {}'.format(self.args.additional)
		command = 'pg_dump -Fc -U {user} {database} -f {output} -h {host} -p {port}'
		command += postfix
		self(command.format(
			user=self.args.user, database=self.args.database, output=self.args.output + '.sql',
			host=self.args.host, port=port)
		)

	def mongo(self):
		port = args.port or '27017'
		postfix = ' {}'.format(self.args.additional)
		postfix += ' --db {}'.format(self.args.database) if self.args.database else ''
		command = 'mongodump --host {host} --port {port} -out {output}'
		command += postfix
		self(command.format(
			host=self.args.host, port=port, output=self.args.output
		))

	def __call__(self, command):
		if self.args.generate:
			print(command)
		else:
			subprocess.call(command, shell=True)

if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--database_engine', '-e', type=str, default='postgres')
	arg_parser.add_argument('--user', '-u', type=str, default='postgres')
	arg_parser.add_argument('--database', '-db', type=str, default=None)
	arg_parser.add_argument('--output', '-o', type=str, default='output.backup')
	arg_parser.add_argument('--host', '-ho', type=str, default='localhost')
	arg_parser.add_argument('--port', '-p', type=str, default=None)
	arg_parser.add_argument('--generate', '-g', type=bool, default=False, 
		help='generate command to execute and just print to console')
	arg_parser.add_argument('--additional', '-a', type=str, default='',
		help='''additional arguments use this flag with double quote. Example -a "--test true". 
		If you need only one flag "-t" without argument use space before: -a " -t"''')
	args = arg_parser.parse_args()
	exporter = DatabaseExporter(args)
	for database in args.database_engine.split(','):
		getattr(exporter, database)()


