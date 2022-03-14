# OrnithoScope
## Setup
### Setup your local repo as a collaborator in your directory of choice
Using [GitHub CLI](https://github.com/cli/cli)
```
gh auth login
gh repo clone deva-sou/OrnithoScope

```

## Clean installation nvidia drivers and cuDNN
Need : CUDA Version: 11.6

Following [this](https://gist.github.com/cuongtvee/738fe439598c38c18835aa581c90e5de) tuto for a clean install.

This project contains its own virtual environment. 

```
source ornithoScope_virtualenv/bin/activate
pip install -r requirements.txt
```