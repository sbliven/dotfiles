echo "`date`  Running .profile" #>> /Users/blivens/startup_scripts.log
/sw/bin/fortune


# This file doesn't get called when starting an X11 terminal, so set
# a variable to allow later scripts (.bashrc) to determine if it has been run
# export PROFILE='~/.profile'
# Problem: ENV transfered to new terms, but other changes (ie alias) need to be rerun

# Include fink paths
test -r /sw/bin/init.sh && . /sw/bin/init.sh
export PATH=".:/usr/local/bin:/usr/local/sbin:/usr/local/mysql/bin/:/Applications/MPlayer\ OSX.app/Contents/Resources/External_Binaries/mplayer.app/Contents/MacOS/:/usr/local/arm-uclinux-tools/bin/:/usr/local/glassfish/bin:$PATH"
export MANPATH="/usr/share/man:/usr/local/man/:/usr/local/share/man:/sw/local/sage-1.2.4/local/share/man:/usr/local/ch5.5.0/docs/man:$MANPATH"
# Setting PATH for MacPython 2.5
# The orginal version is saved in .profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/Current/bin:${PATH}"
export PATH
#export PYTHONPATH=/sw/lib/python2.4/site-packages:$PYTHONPATH
PYTHONPATH="/Library/Frameworks/Python.framework/Versions/Current/"


if [ -e `which vim` ]; then
	export EDITOR=`which vim`
fi

#tomcat settings
CATALINA_HOME=/usr/local/tomcat
export JAVA_HOME=/usr
export JRE_HOME=/System/Library/Frameworks/JavaVM.framework/Versions/1.5.0/
alias tomcat_startup="$CATALINA_HOME/bin/startup.sh"
alias tomcat_shutdown="$CATALINA_HOME/bin/shutdown.sh"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8


#Useful IPs
# 72.14.207.99	google.com
# 164.109.28.3	comcast.com
alias netprobe='ping -aoi 300 72.14.207.99 && date'

# SSH connections
alias dante='ssh -X blivens@dante.u.washington.edu'
alias vergil='ssh -X blivens@vergil.u.washington.edu'
alias attu='ssh -X blivens@attu.cs.washington.edu'
alias fdante='sftp blivens@dante.u.washington.edu'
alias fattu='sftp blivens@attu.cs.washington.edu'
alias aria='rdesktop aria.cs.washington.edu'
alias forkbomb='ssh -X blivens@forkbomb.cs.washington.edu'
alias umnak='ssh -X blivens@umnak.cs.washington.edu'
alias valknut='valknut --disable-tray'
# alias klicklic='ssh blivens@24.18.146.165'
alias klicklic='ssh blivens@redaxed.homelinux.com'
if [[ -e `which links` ]]; then
    alias links='elinks'
fi

#ls options
export CLICOLOR=TRUE
alias ll='ls -l'
alias l.='ls -A'
alias la='ls -a'

alias dosbox='dosbox "/Applications (DOS)/" &'
alias chips='cat "/Applications (DOS)/chips/levels.txt"; dosbox'
alias basilisk='BasiliskII &'

alias psa='ps -rcAo user,pid,ppid,%cpu,%mem,rss=MEM,vsz=VMEM,nice,state=STATE,time,command'
alias psu='ps -rcU blivens -o user,pid,%cpu,%mem,rss=MEM,vsz=VMEM,nice,state=STATE,time,command'

# media
alias qtpresent="osascript -e 'tell application \"QuickTime Player\" to present movie 1.0'"
function mp_nice {
    for p in `psa|grep -i mplayer|awk '{print $2}'`
    do
        sudo renice -10 "$p"
    done
}

# Locates music files outside your music library
function consolidateITunesLibrary {
	local XML="$HOME/Music/iTunes/iTunes Music Library.xml";
	local FILES='file://localhost/Users/blivens/Music/iTunes/iTunes%20Music/';
	sed 's/<[^>]*>/\
/g' "$XML" |
		grep 'file:' |
		grep -v "$FILES";
}

export CVS_RSH="ssh"
#export CVSROOT=redaxed.homelinux.com:/proj/CVS
#export CVSROOT=209.90.226.226:/proj/CVS



#ssh-agent start
SSH_ENV=$HOME/.ssh/environment

function start_agent {
    echo "Initialising new SSH agent..."
    /usr/bin/ssh-agent | sed 's/^echo/#echo/' > ${SSH_ENV}
    echo succeeded
    chmod 600 ${SSH_ENV}
    . ${SSH_ENV} > /dev/null
    /usr/bin/ssh-add;
}

# Source SSH settings, if applicable

if [ -f "${SSH_ENV}" ]; then
    . ${SSH_ENV} > /dev/null
    ps -ecA | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
        start_agent;
    }
else
    start_agent;
fi
#alias com='cvs com'
#alias up='pushd ~/Sites/; cvs up -Pd klicklic > cvs.klicklic.log; egrep -v "templates_c|/test.php|/templates/test.tpl|klicklic/0000|/whoami.php|/TODO|/\..*\.swp" cvs.klicklic.log; popd'
#alias mplayer='"/Applications/MPlayer OSX.app/Contents/Resources/External_Binaries/mplayer.app/Contents/MacOS/mplayer"'
alias showHiddenFiles='defaults write com.apple.finder AppleShowAllFiles TRUE; killall Finder'
alias hideHiddenFiles='defaults write com.apple.finder AppleShowAllFiles FALSE; killall Finder'

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

echo "TERM=$TERM"
case $TERM in
    xterm*)
        # titlebar:
        # \e]0;$str\a sets the title to $str
        PS1='\[\e]0;\u@\h[\l] \W\a\]'
        # prompt:
        PS1="$PS1\[\e[32m\]\w\[\e[34m\]\$\[\e[0m\] "
        echo "PS1=$PS1"
        ;;
    *)
        PS1='\u@\h \wzz\$ '
        echo "default PS1=$PS1"
        ;;
esac
export PS1

