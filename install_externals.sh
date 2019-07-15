#!/bin/bash
# Downloads/updates external tools
# usage: install_externals.sh [.dotfiles]

CONFIG="${1:-}"

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

download () {
    dst="${1}"
    url="${2}"

    echo "downloading $url"
    curl -o "$dst" "$url" || { echo "Error installing $dst"; return 1; }
}

download "$CONFIG/pymol/principal_axes.py" \
    'https://raw.githubusercontent.com/sbliven/principal_axes/master/principal_axes.py'
download "$CONFIG/pymol/ellipsoid.py" \
    'https://raw.githubusercontent.com/sbliven/principal_axes/master/ellipsoid.py'


