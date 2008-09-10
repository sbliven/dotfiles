# ~/.profile
# Created by Spencer Bliven
# 
# This is the generic .profile. It contains settings consistent across 
# multiple hosts. Host-specific variables (like PATH) should be set in
# ~/.profile.local, which is called after this script.

if [ -e `which vim` ]; then
	export EDITOR=`which vim`
fi

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8


#Useful IPs
googleIP='72.14.207.99'
comcastIP='164.109.28.3'
function checknet {
    ping -aoi 300 $googleIP && date
}



# SSH connections
alias dante='ssh -X blivens@dante.u.washington.edu'
alias vergil='ssh -X blivens@vergil.u.washington.edu'
alias attu='ssh -X blivens@attu.cs.washington.edu'
alias fdante='sftp blivens@dante.u.washington.edu'
alias fattu='sftp blivens@attu.cs.washington.edu'
alias aria='rdesktop aria.cs.washington.edu'
alias forkbomb='ssh -X blivens@forkbomb.cs.washington.edu'
alias umnak='ssh -X blivens@umnak.cs.washington.edu'
# alias klicklic='ssh blivens@24.18.146.165'
alias klicklic='ssh blivens@redaxed.homelinux.com'

#ls options
export CLICOLOR=TRUE
alias ll='ls -lh'
alias l.='ls -A'
alias la='ls -a'

#process control
alias psa='ps -rcAo user,pid,ppid,%cpu,%mem,rss=MEM,vsz=VMEM,nice,state=STATE,time,command'
alias psu='ps -rcU blivens -o user,pid,%cpu,%mem,rss=MEM,vsz=VMEM,nice,state=STATE,time,command'

export CVS_RSH="ssh"
#export CVSROOT=redaxed.homelinux.com:/proj/CVS
#export CVSROOT=209.90.226.226:/proj/CVS


# PROMPT
# \[ ... \] is nonprinting 
# colors: \e[<fg;bg;...>m
# color black   red     green   yellow  blue    magenta cyan    white
# fg    30      31      32      33      34      35      36      37
# bg    40      41      42      43      44      45      46      47
# attributes: (not supported in prompt)
# 0 normal
# 1 bold/bright
# 2 underline (not supported)

# Interpret the color dynamically to allow .profile.local to change the value
export PS1_COLOR="31"
case $TERM in
    xterm*)
        # titlebar:
        # \e]0;$str\a sets the title to $str
        PS1='\[\e]0;\u@\h[\l] \W\a\]'
        # prompt:
        PS1="${PS1}\[\e[\${PS1_COLOR}m\]\w\[\e[34m\] \\$\[\e[0m\] "
        ;;
    *)
        PS1="\[\e[\${PS1_COLOR}m\]\u@\h \w\[\e[0m\]\\$ "
        ;;
esac
export PS1

#MySQL prompt
export MYSQL_PS1='\U \d> '

#Wait for the any key to be pressed
pause () {
    tput smso
    echo "Press any key to continue"
    tput rmso
    oldstty=`stty -g`
    stty -icanon -echo min 1 time 0
    dd bs=1 count=1 >/dev/null 2>&1
    stty "$oldstty"
    echo
}


# Run host-specific profile
# Running after the generic profile allows variables to be clobbered
source ~/.profile.local

