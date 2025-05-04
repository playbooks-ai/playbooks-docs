# Installation

This guide will walk you through the process of installing Playbooks AI and setting up your development environment.

## Prerequisites

Before installing Playbooks AI, ensure you have:

- Python 3.10 or higher
- pip (Python package installer)
- A virtual environment tool (optional but recommended)

## Installing Playbooks AI

### Basic Installation

The simplest way to install Playbooks AI is using pip:

```bash
pip install playbooks
```

This will install the core Playbooks AI package with all the essential dependencies.

### Installation in a Virtual Environment

For a cleaner installation that doesn't affect your global Python environment, we recommend using a virtual environment:

#### Using venv (built into Python)

```bash
# Create a virtual environment
python -m venv playbooks-env

# Activate the virtual environment
# On Windows
playbooks-env\Scripts\activate
# On macOS/Linux
source playbooks-env/bin/activate

# Install Playbooks AI
pip install playbooks
```

#### Using Poetry

If you're using Poetry for dependency management:

```bash
# Create a new project with Poetry
poetry new my-playbooks-project
cd my-playbooks-project

# Add Playbooks AI as a dependency
poetry add playbooks

# Activate the virtual environment
poetry shell
```

## Verifying Installation

You can verify that Playbooks AI is installed correctly by running:

```bash
python -c "import playbooks; print(playbooks.__version__)"
```

This should print the version number of the installed Playbooks AI package.

## Optional Dependencies
No optional dependencies are required for Playbooks AI.
<!-- Depending on your use case, you might want to install additional dependencies:

```bash
# For development tools
pip install playbooks[dev]

# For testing tools
pip install playbooks[test]

# For documentation tools
pip install playbooks[docs]
``` -->

## Troubleshooting

### Common Issues

- **ImportError: No module named 'playbooks'**: The package isn't installed correctly. Try reinstalling.
- **Version conflicts**: If you have dependency conflicts, try installing in a fresh virtual environment.
- **Permission errors**: You might need administrator privileges. Try using `sudo pip install playbooks` on Unix systems or run as administrator on Windows.

### Getting Help

If you encounter any issues during installation:

- Check the [GitHub repository](https://github.com/playbooks-ai/playbooks) for known issues
- Join our community on [Discord](https://discord.gg/playbooks-ai) to get help from other users
- File an issue on [GitHub](https://github.com/playbooks-ai/playbooks/issues) if you've found a bug

## Next Steps

Now that you have Playbooks AI installed, you can:

- Follow the [Quickstart Guide](quickstart.md) to create your first playbook
- Explore the [Playbooks Language](../playbooks-language/index.md) documentation to learn about the syntax
