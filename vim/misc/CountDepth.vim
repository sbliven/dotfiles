"so CountDepth.vim
"set foldexpr=CountDepth(v:lnum)
fun! CountDepth(lineNr)
    let depth = len(substitute(getline(a:lineNr),'[^/]','','g'))
    let prev = substitute(getline(a:lineNr-1),'^\v(.*)/[^/]*$','\1','')
    let curr = substitute(getline(a:lineNr),'^\v(.*)/[^/]*$','\1','')
    return curr==prev ? depth : ('>'.depth)
    "let curr = substitute(getline(a:lineNr),'^'.prev.'.*$','','')
    "return len(curr)>0 ? depth : ('>'.depth)
endfun

"Custom foldexpr for viewing svneverever files
fun! CountDepthEverEver(lineNr)
    let line = getline(a:lineNr)
    let depth = len(substitute(line,'\v\([^)]*\)( *).*','\1','g'))
    return depth < len(line) ? depth/4 : '='
endfun
