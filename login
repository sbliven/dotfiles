echo "Running .login"
if [ -e /usr/local/lib/std.login ]; then
    source /usr/local/lib/std.login
fi
stty erase '^h'
exec /usr/local/bin/bash
