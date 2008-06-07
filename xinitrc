#!/bin/sh
# $Id: xinitrc,v 1.3 2004/06/11 04:37:23 jharper Exp $
echo "`date`  Running .xinitrc" >> /Users/blivens/startup_scripts.log

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f "$sysresources" ]; then
    xrdb -merge "$sysresources"
fi

if [ -f "$sysmodmap" ]; then
    xmodmap "$sysmodmap"
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs

xterm -ls -u8 -geometry 100x55+0+0 &
xterm -ls -u8 -geometry 100x28-1+0 &
xterm -ls -u8 -geometry 100x28-1+420 &

# start the window manager

exec quartz-wm
