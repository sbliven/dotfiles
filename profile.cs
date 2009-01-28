#echo "`date`  Running .profile"

#configure paths
PATH="~/bin/:$PATH"
MANPATH="~/man/:$MANPATH"
PATH=".:/projects/cse/courses/cse481f/bin/:$PATH:/uns/bin"
CDPATH="/projects/instr/07sp/cse451/o/:/projects/instr/07sp/cse481f:$CDPATH"
CDPATH="~/Rosetta/blivens:$CDPATH"
CDPATH=".:$CDPATH:~"
#current classes
PATH="/projects/instr/09wi/cse401/g/bin:$PATH"
MANPATH="/projects/instr/09wi/cse401/g/man:$MANPATH"
#mercurial
PATH="/projects/instr/09wi/cse401/g/hg:$PATH"
export GIT_EXEC_PATH
export PATH
export MANPATH
export CDPATH

#CSE481f shortcuts
#alias mfp='/projects/cse/courses/cse481f/bin/default/microfootprinter'
#alias parse-motifs='/projects/cse/courses/cse481f/bin/parse-motifs.csh'

#cdargs
source ~/.cdargs-bash.sh

#CSE shortcuts
alias csepclab='/cse/lab/bin/csepclab-smbclient'

#Use a blue prompt color
export PS1_COLOR='34'

#alias la='ls -A --color=tty'
