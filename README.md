# bitclone

### Clone All My bitbucket Repo

Easly select your repo and clone it in your folder, save time.

#### Install:

    pip install bitclone
    
#### Run:
    
    bitclone
    
or
    
    python -m bitclone

#### And uninstall:

    pip uninstall bitclone

----

### Help

bitclone [-h] [--dir [DIR]]

Automatically choice hg or git and clone it your location,

You must have __hg__ or __git__ tool.

Please check your credential cache, it can store your password

UNSET and SET caching passwords:


    unset:  git config --global --unset credential.helper

Set on Linux:

    git config --global credential.helper 'cache --timeout=3600'

Set on Windows:

    set:    git config --global credential.helper wincred
    

optional arguments:

  -h, --help   show this help message and exit
  
  --dir [DIR]  Clone Location (default: where are you run it)

---

### Usage

![bit_image2](https://image.ibb.co/jqJ4YT/bit2.jpg)