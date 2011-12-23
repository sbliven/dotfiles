set mouse=a
syntax enable

"for programming
set autoindent
set smartindent "indent intelligently around { and such
"do not place comments all the way left:
inoremap # X#
"set cindent "c-style smart indent
"set indentexpr= "custom indent expression
set tabstop=4
set shiftwidth=4
set smarttab "use shiftwidth for tab distance, not tabstop
set expandtab "insert spaces instead of real tabs.
set modeline "settings for vi: at the beginning of files. Ex vi:noet:ts=4:sw=4

set foldmethod=syntax "Automatically detect code folds
set foldmethod=manual "Now allow other folds to be defined

"abbreviations
set shortmess=filnrxtTsI

"use utf-8
set encoding=utf-8 fileencodings=utf-8,latin1

"windowing options
set laststatus=2 "always show status line

"searching
set incsearch
set ignorecase smartcase
set hlsearch

"Don't require brackets to be to the far left
:map [[ ?{<CR>w99[{
:map ][ /}<CR>b99]}
:map ]] j0[[%/{<CR>
:map [] k$][%?}<CR>

set backspace=indent,eol,start
set ruler
"wrap between words
set linebreak
"hardwrap
"set textwidth=80 
set number

set list listchars=trail:`,tab:__
set listchars=tab:›\ ,trail:˙
" Don't use Ex mode or recording mode, use Q for formatting
"map Q gq
"map q gq

map <F1> <Esc>
imap <F1> <Esc>

" man pages
runtime ftplugin/man.vim

" Only do this part when compiled with support for autocommands.
if has("autocmd")
  " Enable file type detection.
  " Use the default filetype settings, so that mail gets 'tw' set to 72,
  " 'cindent' is on in C files, etc.
  " Also load indent files, to automatically do language-dependent indenting.
  filetype plugin indent on

  "autocmd FileType code set number
  autocmd BufEnter,BufRead *.py set smartindent foldmethod=indent foldlevel=99 cinwords=if,elif,else,for,while,try,except,finally,def,class

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!
  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal g`\"" |
    \ endif
  augroup END
else
  set autoindent		" always set autoindenting on
endif " has("autocmd")

if has("gui_running")
    "set editor window size
    set lines=45 columns=96
    "Change GUI: disable toolbar, reduce dialog boxes
    "set guioptions=acegimrLt
    set guioptions+=c
    set guioptions-=T
endif

"if ctags.vim is installed:
let g:ctags_statusline=1
let g:ctags_regenerate=1
let g:ctags_title=1
"    let g:ctags_path='/path/to/ctags'
"    let g:ctags_args='-I __declspec+'
"if a ctags file already exists:
"CTAGS
