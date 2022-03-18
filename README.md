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
virtualenv ornithoScope_virtualenv
source ornithoScope_virtualenv/bin/activate
pip install -r requirements.txt
```

## Create input data

1. Change data location in src/modules/generate_input/variables_generate_input.py
2. In the current directory of the MakeFile:  ```make input```







## MISC:


La base de données qui nous est fournie regroupe 11 espèces d'animaux, majoritairement des oiseaux, désignés par un code : 

1. Mésange charbonnière (**MESCHA**)
2. Verdier d'Europe (**VEREUR**)
3. Écureuil roux (**ECUROU**)
4. Pie bavarde (**PIEBAV**)
5. Sittelle torchepot (**SITTOR**)
6. Pinson des arbres (**PINARB**)
7. Mésange noire (**MESNOI**)
8. Mésange nonnette (**MESNON**)
9. Mésange bleue (**MESBLE**)
10. Rouge-gorge (**ROUGOR**)
11. Accenteur mouchet (**ACCMOU**)