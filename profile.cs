echo "`date`  Running .profile"

#configure paths
PATH=".:/projects/cse/courses/cse481f/bin/:/uns/bin:$PATH"
export PATH
CDPATH=".:~:/projects/instr/07sp/cse451/o/:/projects/instr/07sp/cse481f"
export CDPATH

#CSE481f shortcuts
alias mfp='/projects/cse/courses/cse481f/bin/default/microfootprinter'
alias parse-motifs='/projects/cse/courses/cse481f/bin/parse-motifs.csh'

#CSE shortcuts
alias csepclab='/cse/lab/bin/csepclab-smbclient'

#Always enable x11 forwarding in ssh
alias ssh='ssh -X'

#Set process limit to keep recursion from going out of control
ulimit -Su 64

#allow chats
mesg y

#Use a blue prompt color
export PS1_COLOR='34'

#alias la='ls -A --color=tty'
