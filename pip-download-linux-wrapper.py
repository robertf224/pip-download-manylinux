#!/usr/bin/env python
import argparse, sys, tempfile, shutil, os, subprocess, stat
import docker

def main(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', help='Output directory.', default='.')
	parser.add_argument('-r', help='Requirements file.', required=True)
	parser.add_argument('-c', help='Command to run before downloading packages.')
	parser.add_argument('--python-tag', help='Python tag according to: https://www.python.org/dev/peps/pep-0425/', default='cp27')
	parser.add_argument('--abi-tag', help='ABI tag according to: https://www.python.org/dev/peps/pep-0425/', default='cp27m')

	parsed = parser.parse_args(args)

	output_dir = os.path.realpath(parsed.d)
	requirements_file = parsed.r

	# Make directory supplied with -d if it doesn't exist.
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# Make sure it's actually a directory.
	if not os.path.isdir(output_dir):
		raise Exception('Argument supplied with -d is not actually a directory.')

	# Make a temporary directory to mount requirements.txt and download.sh, and for docker to operate in.
	temp_dir = os.path.realpath(tempfile.mkdtemp())
	shutil.copy(requirements_file, temp_dir + '/requirements.txt')
	download_script = os.path.dirname(os.path.realpath(__file__)) + '/download.sh'
	shutil.copy(download_script, temp_dir + '/download.sh')

	# Make download.sh executable.
	st = os.stat(temp_dir + '/download.sh')
	os.chmod(temp_dir + '/download.sh', st.st_mode | stat.S_IEXEC)

	# Build command for docker to run.
	command = '/io/temp/download.sh'
	if parsed.c:
		command = parsed.c.rstrip(';') + ';' + command

	# Run docker container and download packages.
	client = docker.from_env()
	container = client.containers.create(
		image='quay.io/pypa/manylinux1_x86_64',
		volumes={
			output_dir: {'bind': '/io/packages'},
			temp_dir: {'bind': '/io/temp'}
		},
		command='/bin/bash -c "%s"' % command,
		environment={
			'PYTHON_TAG': parsed.python_tag,
			'ABI_TAG': parsed.abi_tag
		}
	)
	try:
		container.start()
		for line in container.logs(stream=True):
			sys.stdout.write(line)
	except KeyboardInterrupt:
		container.kill()
		shutil.rmtree(output_dir)

	# Clean up temporary directory.
	shutil.rmtree(temp_dir)

if __name__ == '__main__':
	main(sys.argv[1:])
	

