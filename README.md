
# Environment Management Tool 😎
- Welcome to the ultimate Environment Management Tool! 🎉 This tool lets you create, manage, and manipulate partial user spaces (environments) with custom directories and command logging on Windows. Plus, you get to encrypt your environments with a password for that extra layer of security! 🔒

## Table of Contents 📚
- ```Prerequisites```
- ```Installation```
- ```Usage  ``` 
- ```Creating an Environment```
- ```Running Commands in an Environment```
- ```Removing an Environment```
- ```Cloning an Environment```
- ```Backing Up an Environment```
- ```Cleaning the Command Log```
  
## Prerequisites 🛠️
    
- Python 3.6 or higher 🐍
- ```argparse``` module
- ```os``` module
- ```shutil``` module
- ```subprocess``` module
- ```getpass``` module
- ```colorama``` module
- ```cryptography``` module
- ```base64``` module
- ```glob``` module
    

    ## Installation 💾
    
- Clone the repository or download the script file. 🛠️
- Install the required dependencies:
    ```pip install colorama cryptography```

    

 ## Usage 🚀

### Creating an Environment 🌱
  - Ready to create a new environment? Use the ```mkenv``` command:
    ```python script.py mkenv name password [-loc location] [-temp] [-run]```
    
    - ```name```: Name of the environment. 🎨
      - ```password```: Password for encryption. 🔒
      - ```-loc```: Optional location to create the environment. Defaults to the current working directory. 📁
      - ```-temp```: Optional flag to create a temporary environment that will be moved to ```TrashENVs``` upon exit. 🚮
     - ```-run```: Optional flag to create and immediately run the environment. 🏃
    

### Running Commands in an Environment 💻
  - Run commands in your super cool environment with the ```run``` command:
    ```python script.py run name password [-loc location]```
    
- ```name```: Name of the environment. 🎨
- ```password```: Password for encryption. 🔒
- ```-loc```: Optional location of the environment. Defaults to the current working directory. 📁
    

### Removing an Environment 🗑️
  - Say goodbye to an environment and move it to ```TrashENVs``` with the ```rmenv``` command:
    ```python script.py rmenv name password [-loc location]```
    
- ```name```: Name of the environment. 🎨
- ```password```: Password for encryption. 🔒
- ```-loc```: Optional location of the environment. Defaults to the current working directory. 📁
    

### Cloning an Environment 🧬
  - Clone your environment like a mad scientist with the ```clenv``` command:
    ```python script.py clenv target_name new_name password [-loc location]```
    
- ```target_name```: Name of the environment to clone. 🧬
- ```new_name```: Name for the new cloned environment. 🆕
- ```password```: Password for encryption. 🔒
- ```-loc```: Optional location to create the new environment. Defaults to the current working directory. 📁
    

### Backing Up an Environment 💾
  - Never lose your hard work! Back up your environment with the ```backup``` command:
    ```python script.py backup name password [-loc location]```
    
- ```name```: Name of the environment. 🎨
- ```password```: Password for encryption. 🔒
- ```-loc```: Optional location of the environment. Defaults to the current working directory. 📁
    

### Cleaning the Command Log 🧹
  - Keep things tidy! Clean the command log with the ```clean``` command:
```python script.py clean name password [-loc location]```
    
- ```name```: Name of the environment. 🎨
- ```password```: Password for encryption. 🔒
- ```-loc```: Optional location of the environment. Defaults to the current working directory. 📁
    

### Command Line Arguments 📝
  - Here's a quick overview of all the commands and their arguments:
    
- ```mkenv name password [-loc location] [-temp] [-run]``` — Create a new environment. 🌱
- ```run name password [-loc location]``` — Run commands in an existing environment. 💻
- ```rmenv name password [-loc location]``` — Remove an environment. 🗑️
- ```clenv target_name new_name password [-loc location]``` — Clone an environment. 🧬
- ```backup name password [-loc location]``` — Back up an environment. 💾
- ```clean name password [-loc location]``` — Clean the command log of an environment. 🧹
    

- And there you have it! Enjoy managing your environments like a pro! 😎

