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
# taken from Mark Liyange <www.entropy.ch>
SSHHOSTNAMES=~/.known_ssh_hostnames
if [[ ! -e $SSHHOSTNAMES || $SSHHOSTNAMES -ot ~/.ssh/known_hosts ]]; then
    cut -f 1 -d ' ' ~/.ssh/known_hosts |
        perl -p -e 's#,#\n#' |
        sort -u |
        perl -e 'chomp(@x = <>); print map {"$x[$_]\n"} grep {$x[$_ + 1] !~ /^$x[$_]\..+$/m} (0 .. $#x);' > $SSHHOSTNAMES
fi
alias list_all_hostnames='cat ~/.known_ssh_hostnames'
#might be tcsh format?
complete scp 'p/*/`scp_completions`/'

#Set process limit to keep recursion from going out of control
ulimit -Su 64

if [[ "$-" =~ i ]]; then
    #allow chats
    mesg y
    echo interactive
fi
