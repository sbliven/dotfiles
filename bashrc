echo "Running 	~/.bashrc"

# run the profile, if it hasn't yet
if [[ ! $PROFILE ]]; then
    . ~/.profile
else
    echo "$PROFILE already run"
fi

# history
export HISTIGNORE="fg:bg:exit"
set cmdhist
set show-all-if-ambiguous on

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


#export PS1='\[\e]0;\u@\h \w\a\]\n\[\e[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]\n\$ '
export PS1='\[\e[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]\$ '

