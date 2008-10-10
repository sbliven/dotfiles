echo "`date`  Running .profile"

#configure paths
PATH="~/bin/:$PATH"
MANPATH="~/man/:$MANPATH"
PATH=".:/projects/cse/courses/cse481f/bin/:$PATH:/uns/bin"
CDPATH="/projects/instr/07sp/cse451/o/:/projects/instr/07sp/cse481f:$CDPATH"
CDPATH="~/Rosetta/blivens:$CDPATH"
CDPATH=".:$CDPATH:~"
export PATH
export MANPATH
export CDPATH

#CSE481f shortcuts
alias mfp='/projects/cse/courses/cse481f/bin/default/microfootprinter'
alias parse-motifs='/projects/cse/courses/cse481f/bin/parse-motifs.csh'

#CSE shortcuts
alias csepclab='/cse/lab/bin/csepclab-smbclient'

#Always enable x11 forwarding in ssh
alias ssh='ssh -X'

#Use a blue prompt color
export PS1_COLOR='34'

#alias la='ls -A --color=tty'
