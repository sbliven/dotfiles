dotfiles
========

Author
------

Spencer Bliven. spencer@bliven.us


About
-----

These are my config files for bash, vim, git, pymol, etc. They are intended for my personal use and are not intended for redistribution.

Scripts written by me (as indicated in the file header) are public domain unless otherwise specified. I have tried to indicate sources where I've used other people's code or included third-party libraries, but I haven't thoroughly scrutenized the licenses of everything included here. My appologies if anything is misused.

Installation
------------

From your home directory, clone the repository:

    git clone https://github.com/sbliven/dotfiles.git ~/.dotfiles
    
Now run install.sh

    .dotfiles/install.sh

This will rename any existing dot files with a .old suffix and replace them with symbolic links into the .dotfiles directory.

