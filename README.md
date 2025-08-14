# :rocket: a2a-agent-bootstrapping

Bootstrapping some useful agents for a2a registry

## Setup Dev Environment

Installation is using [UV](https://docs.astral.sh/uv/) to manage everything.

**Step 1**: Create a virtual environment

```
uv venv
```

**Step 2**: Activate your new environment

```
# on windows
.venv\Scripts\activate

# on mac / linux
source .venv/bin/activate
```

**Step 3**: Install all the cool dependencies

```
uv sync
```

## Github Repo Setup

To add your new project to its Github repository, firstly make sure you have created a project named **a2a-agent-bootstrapping** on Github.
Follow these steps to push your new project.

```
git remote add origin git@github.com:prassanna-ravishankar/a2a-agent-bootstrapping.git
git branch -M main
git push -u origin main
```

## Built-in CLI Commands

We've included a bunch of useful CLI commands for common project tasks using [taskipy](https://github.com/taskipy/taskipy).

```
# run src/a2a_agents/a2a_agents.py
task run

# run all tests
task tests



# run test coverage and generate report
task coverage

# typechecking with Ty or Mypy
task type

# ruff linting
task lint

# format with ruff
task format
```

## References

- [Cookiecutter Python Project](https://github.com/wyattferguson/pattern) - A modern cookiecutter template for your next Python project.

## License

MIT

## Contact

Created by [Prass, The Nomadic Coder](https://github.com/prassanna-ravishankar)
