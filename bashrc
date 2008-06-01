echo "`date`  Running .bashrc" #|tee -a /Users/blivens/startup_scripts.log

# history
export HISTIGNORE="fg:bg:exit"
set cmdhist
set show-all-if-ambiguous on

#set some bash settings
shopt -s checkwinsize
shopt -s cdspell
shopt -s hostcomplete
shopt -s extglob
shopt -s hostcomplete
# report completed jobs immediately
# set -b

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
