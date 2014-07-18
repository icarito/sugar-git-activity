" Remover el menú y la botonera de Vim
set guioptions-=m
set guioptions-=T

" Hace a Vim amigable
set nocompatible               " be iMproved
filetype off                   " required!

" indentation
set autoindent
set softtabstop=4 shiftwidth=4 expandtab

" visual
highlight Normal ctermbg=black
set background=dark
set cursorline
set t_Co=256

" syntax highlighting
syntax on
"filetype on                 " enables filetype detection
"filetype plugin indent on   " enables filetype specific plugins

" colorpack
" colorscheme inkpot
colo desert 

" set guifont=Terminus\ 14

if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$")
    \| exe "normal! g'\"" | endif
endif

" Start in insert mode and
" set escape to switch to
" command mode or back to
" insert.
"set im!
"map <Esc> :set im!<CR><c-o>:echo <CR>
"map i :set im!<CR><c-o>:echo <CR>
"map! <Esc> <c-o>:set im!<CR>:echo <CR>
"map a :set im<CR><c-o>l<c-o>:echo <CR>
"map A :set im<CR><c-o>$<c-o>:echo <CR>
"map o :set im<CR><c-o>$<c-o>:echo <CR><CR>
"map O :set im<CR><c-o>^<c-o>:echo <CR><CR><c-o>k
