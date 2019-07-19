#!/bin/bash
# Links config files to their dotfile equivalent
# I generally check out the repository as ~/.dotfiles, then run this script
# from the home directory as `.dotfiles/install.sh`. However, other repository
# locations should work fine as long as you don't move it after installing.

#dir to put dotfiles in
ROOT="$HOME";

#Print a list of linked files
#export DEBUG_PRINT=${DEBUG_PRINT='T'}

# Try to guess the absolute path for the config scripts. This should work in
# most cases, but it's not foolproof.
if [ "$CONFIG" = "" ]
then
    if [[ "$0" =~ ^/ ]]
    then
        CONFIG="$0"
    else
        CONFIG="$PWD/$0"
    fi
    #assert [ -e $CONFIG ]
    CONFIG="`dirname $CONFIG`"
fi

# catch potential errors
if [ ! -d "$CONFIG" ]; then
    echo "Error: $CONFIG does not exist or is not a directory" >&2
    exit 1;
fi

# Update submodules
(
    cd $CONFIG && git submodule update --init --rebase --recursive
)

# Install externals
$CONFIG/install_externals.sh "$CONFIG"

# Function to safely symlink two files
# If the destintion is already a file, move it out of the way or throw an error
safeLink() {
    local src="$1" dst="$2";

    if [[ -e "$dst" && ! -h "$dst" ]] ; #exists and not a link
    then
        #move old $dst out of the way
        if [ -e "${dst}.old" ]
        then
            echo "ERROR: '$dst' already exists. Please remove it and try again." 1>&2
            return 1
        else
            echo "Moving '$dst' to '${dst}.old'"
            mv "$dst" "${dst}.old"
        fi
    fi
    #assert [[ ! -e "$dst" || -h "$dst" ]]

    #link new dst
    if [[ -n ${DEBUG_PRINT} && ${DEBUG_PRINT} != 'F' ]]; then
        echo "$src->$dst"
    fi
    ln -sf "$src" "$dst"
}
export -f safeLink

cat <<END | awk " { printf( \"safeLink \\\"$CONFIG/%s\\\" \\\"$ROOT/%s\\\";\", \$1, \$2) | \"/bin/bash\";}" ;
bashrc	.bashrc
bash_profile	.bash_profile
profile	.profile
profile.default	.profile.local
bashrc.default	.bashrc.local
Xdefaults.white	.Xdefaults
vimrc	.vimrc
vim	.vim
xinitrc	.xinitrc
Xmodmap	.Xmodmap
screenrc	.screenrc
gnuplot	.gnuplot
hgrc	.hgrc
pymolrc	.pymolrc
pymol	.pymol
gitconfig	.gitconfig
gitconfig.default	.gitconfig.local
MacOSX	.MacOSX
synergy.conf	.synergy.conf
cvsignore	.cvsignore
git-completion.bash	.git-completion.bash
zshrc	.zshrc
bin	bin
END

#select the proper local profile
echo 'Remember to customize or re-link for this machine: .profile.local .bashrc.local .gitconfig.local'

