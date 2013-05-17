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
shopt -s nullglob
shopt -s histappend
shopt -s hostcomplete
shopt -s interactive_comments
shopt -s no_empty_cmd_completion
shopt -s nullglob
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
ulimit -Su 128

if [[ "$-" =~ i ]]; then
    #allow chats
    mesg y
    echo interactive
fi

if [[ -x "$(which autojump 2>/dev/null)" ]]; then
    #autojump
    #This shell snippet sets the prompt command and the necessary aliases

    #Copyright Joel Schaerer 2008, 2009
    #This file is part of autojump

    #autojump is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.
    #
    #autojump is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.
    #
    #You should have received a copy of the GNU General Public License
    #along with autojump.  If not, see <http://www.gnu.org/licenses/>.
    _autojump() {
        local cur
        cur=${COMP_WORDS[*]:1}
        while read i
        do
            COMPREPLY=("${COMPREPLY[@]}" "${i}")
        done  < <(autojump --bash --completion $cur)
    }
    complete -F _autojump j

    AUTOJUMP='{ (autojump -a "$(pwd -P)"&)>/dev/null 2>>${HOME}/.autojump_errors;} 2>/dev/null'
    if [[ ! $PROMPT_COMMAND =~ autojump ]]; then
        PROMPT_COMMAND="${PROMPT_COMMAND%;}"
        PROMPT_COMMAND="${PROMPT_COMMAND%; }"
        export PROMPT_COMMAND="${PROMPT_COMMAND:-:} && $AUTOJUMP"
    fi 
    alias jumpstat="autojump --stat"
    function j {
        new_path="$(autojump $@)";
        if [ -n "$new_path" ]; then
            echo -e "\\033[31m${new_path}\\033[0m";
            cd "$new_path";
        fi
    }
fi

