from __future__ import unicode_literals, absolute_import
import click, os, ConfigParser, getpass

@click.command('setup-custom-app')
def setup_custom_app():
	"""Generate config for supervisor, nginx and Procfile"""
	try:
		if click.confirm('This will add custom node to existing supervisor config file. Continue?'):
			setup_supervisor()

		if click.confirm('This will add custom node to existing Procfile. Continue?'):
			setup_procfile()

	except Exception as e:
		print(e)

def get_bench_dir():
	if os.getcwd().split('/')[-1] == 'sites':
		return os.path.split(os.getcwd())[0]
	else:
		return os.path.abspath('.')

def setup_supervisor():
	conf_file = get_bench_dir() + '/config/supervisor.conf'

	if not os.path.isfile(conf_file):
		raise IOError(conf_file + " does not exist.")

	bench_dir = get_bench_dir().split('/')[-1]
	new_section = "program:" + bench_dir + "-" + get_app_name(slug=False)

	node_command = get_node_command()
	
	node_stdout_logfile = get_bench_dir() + "/logs/" + get_app_name(slug=True) + ".log"
	node_stderr_logfile = get_bench_dir() + "/logs/" + get_app_name(slug=True) + ".error.log"

	config_parser = ConfigParser.ConfigParser()
	config_parser.read(conf_file)

	config_parser.add_section(new_section)
	config_parser.set(new_section, 'command', node_command)
	config_parser.set(new_section, 'priority', 4)
	config_parser.set(new_section, 'autostart', "true")
	config_parser.set(new_section, 'autorestart', "true")
	config_parser.set(new_section, 'stdout_logfile', node_stdout_logfile)
	config_parser.set(new_section, 'stderr_logfile', node_stderr_logfile)
	config_parser.set(new_section, 'user', getpass.getuser())
	config_parser.set(new_section, 'directory', get_bench_dir())
	
	# add group
	config_parser.add_section("group:" + bench_dir + "-" + get_app_name(slug=False))
	config_parser.set("group:" + bench_dir + "-" + get_app_name(slug=False),
						"programs", bench_dir + "-" + get_app_name(slug=False))

	with open(conf_file, 'ab') as f:
		config_parser.write(f)

def setup_procfile():
	found = False
	procfile = get_bench_dir() + "/Procfile"
	node_command = get_node_command()

	if not os.path.isfile(procfile):
		raise IOError(procfile + " does not exist.")

	with open(procfile) as f:
		l = list(f)

	with open(procfile, 'w') as output:
		for line in l:
			if line.startswith(get_app_name(slug=True)):
				found = True
				output.write(get_app_name(slug=True) + ': ' + node_command + "\n")
			elif not found:
				output.write(line)

	if not found:
		with open(procfile, 'ab') as f:
			f.write(get_app_name(slug=True) + ': ' + node_command + "\n")

def get_app_name(slug=False):
	if slug:
		return "custom_node"
	else:
		return "custom-node"

def get_node_command():
	# node_command = "/usr/bin/node /home/user/bench/apps/custom_app/custom_app.js"
	node_command = "/usr/bin/node " + get_bench_dir()
	node_command += "/apps/" + get_app_name(slug=True) + "/" + get_app_name(slug=True) + ".js"
	return node_command

commands = [setup_custom_app]
