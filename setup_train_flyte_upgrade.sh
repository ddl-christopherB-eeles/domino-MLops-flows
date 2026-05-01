# Install train-flyte-library 0.17.4, which supports the resolving a SHA for floating branch references
sudo apt update && sudo apt install gh

# Requires user input (recommend HTTPS to avoid making new SSH key )
gh auth login

# Install the library
/opt/conda/bin/pip3 install --no-deps --no-cache-dir --force-reinstall \
  'git+https://github.com/cerebrotech/train-flyte-library.git@ddl-ceeles.DOM-69440.flows-reproducibility-gitref-resolution'