# Fake but Realistic Data

A simple commandline tool to generate mock data for databases.

## Usage

To use the tool, python3 and `make` is required on the system.

Run `make build` to set up the python environment and install dependencies automatically.

Then use the `run.sh` script to run the tool. An example input file is included in the `example` folder. (Remember to `chmod +x run.sh`)

```
./run.sh -i example/input.txt
```

Use `run.sh -h` to see all the flags available. Check the example input file for all the customization options available.

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
