#!/bin/bash
# Links config files to their dotfile equivalent

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
    CONFIG=`dirname $CONFIG`
fi

# Safely symlink two files
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
profile	.profile
Xdefaults.white	.Xdefaults
vimrc	.vimrc
vim	.vim
xinitrc	.xinitrc
Xmodmap	.Xmodmap
screenrc	.screenrc
profile.default	.profile.local
gnuplot	.gnuplot
hgrc	.hgrc
pymolrc	.pymolrc
pymol	.pymol
gitconfig	.gitconfig
END

#select the proper local profile
echo 'Remember to customize or re-link .profile.local for this machine.'

