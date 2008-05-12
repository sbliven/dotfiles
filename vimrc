set mouse=a
syntax enable

"for programming
set autoindent
set smartindent "indent intelligently around { and such
"inoremap # X# 
"do not place comments all the way left:
"set cindent "c-style smart indent
"set indentexpr= "custom indent expression
set tabstop=4
set shiftwidth=4
set smarttab "use shiftwidth for tab distance, not tabstop
set expandtab "insert spaces instead of real tabs.


"windowing options
set laststatus=2 "always show status line

"Don't require brackets to be to the far left
:map [[ ?{<CR>w99[{
:map ][ /}<CR>b99]}
:map ]] j0[[%/{<CR>
:map [] k$][%?}<CR>
