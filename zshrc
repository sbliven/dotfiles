# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/Users/bliven_s/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="agnoster"
PRIMARY_FG="white"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
  #bundler # not compatible with rvm
  autojump
  rvm
  #autoenv
)

#homebrew anaconda
#if [ -d /usr/local/anaconda3 ]; then
#    #add last so that the normal versions come first
#    export PATH="$PATH:/usr/local/anaconda3/bin"
#
#    # mimic virtualenvwrapper
#    alias workon='source activate'
#elif [[ -d /usr/local/miniconda3 ]]; then
#    #add last so that the normal versions come first
#    export PATH="$PATH:/usr/local/miniconda3/bin"
#
#    # mimic virtualenvwrapper
#    alias workon='source activate'
#fi

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/usr/local/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/usr/local/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/usr/local/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/usr/local/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# mimic virtualenvwrapper
alias workon='source activate'

# MacTex
if [ -d /Library/TeX/texbin ]; then
    PATH="/Library/TeX/texbin:$PATH"
fi

path+=("$HOME/bin" "/usr/local/bin" "/usr/local/sbin")

# Make Homebrew’s completions available in zsh.
# Get the Homebrew-managed zsh site-functions on your FPATH before initialising
# zsh’s completion facility. This must be done before compinit is called, so
# this must be done before you call oh-my-zsh.sh.

if type brew &>/dev/null; then
  FPATH=$(brew --prefix)/share/zsh/site-functions:$FPATH
fi



source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'
else
  export EDITOR='mvim'
  export GIT_EDITOR='mvim -f'
fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

alias showHiddenFiles='defaults write com.apple.finder AppleShowAllFiles TRUE; killall Finder'
alias hideHiddenFiles='defaults write com.apple.finder AppleShowAllFiles FALSE; killall Finder'

# Main user (omitted by theme for shorter prompts)
DEFAULT_USER=bliven_s

WORDCHARS='*?_-.[]~=&;!#$%^(){}<>/'

export PDB_DIR="$HOME/pdb"
export PDB_CACHE_DIR="$PDB_DIR"

# jenv for java version management
if [[ -d "$HOME/.jenv" ]]; then
    export PATH="$HOME/.jenv/bin:$PATH"
    eval "$(jenv init -)"
fi

# Prefer GNU variants over mac utilities
# brew install coreutils findutils gnu-tar gnu-sed gawk gnutls gnu-indent gnu-getopt grep
# Update list:
#for d in /usr/local/opt/*/libexec/gnubin; do echo -n "$(basename "$(realpath "$d/../../..")") "; done | pbcopy
for gnuutil in coreutils findutils gawk gnu-indent gnu-sed gnu-tar grep; do
    if [[ -d "/usr/local/opt/$gnuutil" ]]; then
        PATH="/usr/local/opt/$gnuutil/libexec/gnubin:$PATH"
        MANPATH="/usr/local/opt/$gnuutil/libexec/gnuman:${MANPATH:-/usr/share/man}"
    fi
done

## Export the proper java version
#if [[ ! -d "$JAVA_HOME" && -x /usr/libexec/java_home ]]; then
#    export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
#fi


# iTerm2 shell integration
[[ -f ~/.iterm2_shell_integration.zsh ]] && source ~/.iterm2_shell_integration.zsh

# SPARK configuration
#export SPARK_HOME=/usr/local/spark-2.3.0-bin-hadoop2.7
#export PATH="${SPARK_HOME}/bin:$PATH"
#export PYTHONPATH="${SPARK_HOME}/python:$PYTHONPATH"

export MMTF_REDUCED=$PDB_DIR/reduced/
export MMTF_FULL=$PDB_DIR/full/


function pdbNumber {
    sed -nE 's/^ATOM.{9}CA  (...) (.) *([^ ]+).*$/\1  \2      \3/p;/^ENDMDL/q' "$@"
}

# number headers
function nh {
    #echo "$# params:"
    #for p in "$@"; do echo "'$p'"; done

    local multiHeader=$(( $# > 1 ))
    while (( $# > 0 )); do 
        if (( $multiHeader )); then
            echo "$1:"
        fi
        head  -1 "$1" | tr $'\t' $'\n' | nl

        shift #|| { echo break && break; }
    done
}

# Count entries in a FASTA file
function wcfasta {
    egrep '^>' "$@" | wc -l
}

# Remove zsh safety net
setopt rm_star_silent

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

#nix
if [ -e /Users/bliven_s/.nix-profile/etc/profile.d/nix.sh ]; then . /Users/bliven_s/.nix-profile/etc/profile.d/nix.sh; fi # added by Nix installer

# direnv
eval "$(direnv hook zsh)"

## Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
if [[ -d "$HOME/.rvm" ]]; then
    export PATH="$PATH:$HOME/.rvm/bin"

    [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
fi




