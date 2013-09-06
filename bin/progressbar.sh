#!/bin/bash
# based on http://www.unix.com/shell-programming-scripting/26542-shell-script-animation.html

b=0
p=0
for (( i=1; i <= 100 ; i+=1 ))
do
    # back up $b characters
    while (( $b >= 0 ))
    do
        echo -n $'\b'
        (( b -= 1 ))
    done

    # print $i characters
    for (( o=1 ; o <= i ; o++ ))
    do
        echo -n $'='
    done

    b=$(( o + 3 ))

    [ $p -eq 0 ] && CAR='|'
    [ $p -eq 1 ] && CAR='/'
    [ $p -eq 2 ] && CAR='-'
    [ $p -eq 3 ] && CAR='\'
    (( p = (p+1)%4 ))

    echo -n " ${CAR} $i%"
    #sleep 1
done
echo
