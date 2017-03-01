# pip-download-manylinux-wrapper
A wrapper around pip download that gets manylinux wheels even if they don't exist yet.

This downloader works by fetching manylinux wheels if they exist, and if they don't, it compiles them in a docker container running CentOS 5 (more details here https://github.com/pypa/manylinux).

Installation
------------
First, install [Docker](https://docs.docker.com/docker-for-mac/install/), and install the official Docker python library with `pip install docker`.

You can either run the script directly, or add it to your path.

If you would like to add it to your path, `cd` into the directory you want to install the wrapper (possibly `/usr/local/bin`), and then:
```bash
git clone git@github.palantir.build:rfidler/pip-download-manylinux-wrapper.git
cd pip-download-manylinux-wrapper
echo "export PATH=\$PATH:`pwd`" >> ~/.bashrc
```

Usage
-----
```bash
pip-download-manylinux -r <pip requirements file> -d <output directory> -c <command> --python-tag <tag> --abi-tag <tag>
```

The command passed to `-c` gets run in the docker container before the download/compilation step (if you would like to issue multiple commands, separate them with a semicolon).

The `--python-tag` and `--abi-tag` arguments specify the targeted python distribution according to (https://www.python.org/dev/peps/pep-0425/).  Skylab/Houston use cp27 and cp27m, respectively (and thus these are the default arguments).
