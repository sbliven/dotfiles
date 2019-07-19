" Install vim-plug plugin manager
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" Load plugins
" Run :PlugInstall after modifying
call plug#begin('~/.vim/plugged')
" Sensible defaults
Plug 'tpope/vim-sensible'

" Colorschemes
Plug 'altercation/vim-colors-solarized'

" Auto-detect tab spacing
Plug 'tpope/vim-sleuth'

" statusline
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" Languages
Plug 'tpope/vim-rails',          { 'for': 'ruby'       }
Plug 'pangloss/vim-javascript',  { 'for': 'javascript' }
Plug 'plasticboy/vim-markdown',  { 'for': 'markdown'   }
Plug 'davidhalter/jedi-vim',     { 'for': 'python'     }

" Programming
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
Plug 'tpope/vim-fugitive'
Plug 'tpope/vim-rhubarb'
Plug 'gregsexton/gitv'
if v:version >= 703
  Plug 'airblade/vim-gitgutter'
else
  Plug 'mhinz/vim-signify'
endif
if v:version >= 703
  Plug 'Yggdroot/indentLine'
endif

" Editing
Plug 'dhruvasagar/vim-table-mode'
Plug 'junegunn/vim-emoji'

call plug#end()

" -------------------------------------------------------------------------




"" Colorscheme
syntax enable
"set background=light "defaults to autodetect
let g:solarized_visibility="normal" " low|normal|high
let g:airline_theme='solarized'
colorscheme solarized

"locallize all the .un~ files
set undodir^=~/.vim/undo

set mouse=a

"for programming
set autoindent
set smartindent "indent intelligently around { and such
"do not place comments all the way left:
inoremap # X#
"set cindent "c-style smart indent
"set indentexpr= "custom indent expression
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

" Custom foldcommand
"set foldmethod=expr foldexpr=CountDepth(v:lnum)
so ~/.vim/misc/CountDepth.vim

" Enable spellchecking
" setlocal spell spelllang=en_us


" ----------------------------------------------------------------------
" Plugin configuration
" ----------------------------------------------------------------------


" TableMode shortcuts
if &runtimepath =~ 'vim-table-mode'
  " Use || for TableModeEnable and __ for TableModeDisable
  function! s:isAtStartOfLine(mapping)
    let text_before_cursor = getline('.')[0 : col('.')-1]
    let mapping_pattern = '\V' . escape(a:mapping, '\')
    let comment_pattern = '\V' . escape(substitute(&l:commentstring, '%s.*$', '', ''), '\')
    return (text_before_cursor =~? '^' . ('\v(' . comment_pattern . '\v)?') . '\s*\v' . mapping_pattern . '\v$')
  endfunction

  inoreabbrev <expr> <bar><bar>
            \ <SID>isAtStartOfLine('\|\|') ?
            \ '<c-o>:TableModeEnable<cr><bar><space><bar><left><left>' : '<bar><bar>'
  inoreabbrev <expr> __
            \ <SID>isAtStartOfLine('__') ?
            \ '<c-o>:silent! TableModeDisable<cr>' : '__'
endif


" IndentLine
"let g:indentLine_color_term = 239
let g:indentLine_char_list = ['|', '¦', '┆', '┊']

" Emoji 🐶 🐱
" Unfortunately these don't work well on older terminals with bad utf-16
" support
"if &runtimepath =~ 'vim-emoji' && &runtimepath =~ 'vim-gitgutter'
"if emoji#available()
"  let g:gitgutter_sign_added = emoji#for('small_blue_diamond')
"  let g:gitgutter_sign_modified = emoji#for('small_orange_diamond')
"  let g:gitgutter_sign_removed = emoji#for('small_red_triangle')
"  let g:gitgutter_sign_modified_removed = emoji#for('collision')
"  set completefunc=emoji#complete
"endif


""" PLUGIN-SPECIFIC OPTIONS
" Options to run after plugins are loaded
" These are "supposed to be" set in after/plugin directory, but then
" cross-platform synchronization would get even messier. So, au VimEnter it is. 
" https://superuser.com/a/931316/55943
function! SetPluginOptionsNow()

  " Delayed code

endfunction

au VimEnter * call SetPluginOptionsNow()
""" END OF PLUGIN-SPECIFIC OPTIONS
