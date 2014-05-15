#echo "`date`  Running .bashrc" #|tee -a /Users/blivens/startup_scripts.log

# history
export HISTIGNORE="fg:bg:exit"
export HISTCONTROL="ignoredups:ignorespace:erasedups"
set show-all-if-ambiguous on

#set some bash settings
shopt -s cdspell
shopt -s checkwinsize
shopt -s cmdhist
shopt -s extglob
shopt -s histappend
shopt -s hostcomplete
shopt -s interactive_comments
shopt -s no_empty_cmd_completion
shopt -s failglob
# report completed jobs immediately
set -b

# hostname autocompletion
if [ -d /opt/local/etc/bash_completion ]; then
    . /opt/local/etc/bash_completion
else
    # bash-completion isn't installed, so manually add some completions
    function _complete_ssh_hosts {
        COMPREPLY=()
        cur="${COMP_WORDS[COMP_CWORD]}"
        comp_ssh_hosts=$(
            sed -e 's/^  *//' -e '/^#/d' -e 's/[, ].*//' -e '/\[/d' ~/.ssh/known_hosts | sort -u
            if [ -f ~/.ssh/config ]; then
                sed -En "s/\*.*$//;s/^Host (.)/\1/p" ~/.ssh/config|tr ' ' "\n"
            fi
        )
        COMPREPLY=( $(compgen -W "${comp_ssh_hosts}" -- $cur))
        return 0
    }
    complete -F _complete_ssh_hosts ssh sftp scp
    complete -c -f command sudo
fi


#Set process limit to keep recursion from going out of control
#ulimit -Su 128

if [[ "$-" =~ i ]]; then
    #allow chats
    mesg y
    echo interactive
fi

if [[ -x "$(which autojump 2>/dev/null)" ]]; then
    if [ -e /usr/share/autojump/autojump.bash ]; then
        source /usr/share/autojump/autojump.bash
    elif [ -e /opt/local/etc/profile.d/autojump.bash ]; then
        source /opt/local/etc/profile.d/autojump.bash
    fi
fi

