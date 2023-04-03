# Fake but Realistic Data

A simple commandline tool to generate mock data for databases.

## Usage

To use the tool, `python3` and `make` is required on the system. Python version 3.8 is the minimum requirement. The tool will also make use of python's built-in `venv` tool.

1. Run `make build`. This will do all the setup.

2. Use `run.sh` to run the tool. An example input file is included in the `example` folder.
    - (if run.sh is not executable remember to run `chmod +x run.sh`)

```
./run.sh -i example/input.txt
```

Use `./run.sh -h` to see all the flags available. Check the example input file for all the customization options available.

## Input syntax

This program requires the user to provide a mandatory input txt file, in a custom-made input format, declaring all the schemas and requirements for data generation. Example input files are provided in the `example` folder.

For comprehensive documentation on input file, refer to [this README file](./example/README.md)

## Development

For developers: To set up the development environment:

- Make sure `python3` is available on your system
- Make sure `make` is available on your system (check using `make -version`)
    - Ubuntu: `sudo apt install make`
    - Macos: `xcode-select --install`
    - Windows: I'm really sorry but you're on your own
- Run `make setup_env`
- Run `make install`
- Test run using `./run.sh -i example/input.txt` 
    - (if run.sh is not executable remember to run `chmod +x run.sh`)

*Important:* Remember to activate the python virtual environment on the commandline when you do dev work:

```
source ./venv/bin/activate
```

You can then use `deactivate` to exit the virtual environment.

To install new dependencies or package:

- Make sure you activated venv
- `pip install whatever`
- `pip freeze > requirements.txt`

So that the dependencies are recorded and committed to version control.
