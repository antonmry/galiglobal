title=Vim as Java and Groovy IDE (again) but now with Neovim
date=2017-02-26
type=post
tags=java,vim,neovim,groovy,gradle
status=published
---------

I've tried so many times change Intellij or Eclipse by vim.. But when it's related to Java is really hard to find a real alternative to those IDEs. And when we speak about Groovy, it's even worse. Yet I use vim a lot: edit files, write blog posts, etc. Also my Chrome and Thunderbird configuration uses Vim shortcuts, so I keep myself more or less trained.

Some weeks ago I've discovered this blog post [Use Vim as a Java IDE](https://spacevim.org/use-vim-as-a-java-ide/) and I want to give it another opportunity. Let's start.

## Neovim in Fedora

This is straight-forward:

```
sudo dnf -y copr enable dperson/neovim
sudo dnf -y install neovim
sudo dnf -y install python3-neovim python3-neovim-gui
```

For Fedora 25 is even easier:

```
sudo dnf -y install neovim
sudo dnf -y install python2-neovim python3-neovim
```

For other systems, just check [the official Neovim documentation](https://github.com/neovim/neovim/wiki/Installing-Neovim).

We'll need some other plugins:

```
sudo dnf -y install astyle
```

## Install vim-plug

Again, this is straight-forward following [the official instructions](https://github.com/junegunn/vim-plug):

```
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

## Install plugins

This is when things become messy. Start editing `~/.config/nvim/init.vim` to add the plugins:

```
"""""""""""""""""""""""""
""""    vim-plug     """"
"""""""""""""""""""""""""
call plug#begin('~/.local/share/nvim/plugged')

" Others

Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'majutsushi/tagbar'

" Java development

Plug 'sbdchd/neoformat'
Plug 'artur-shaik/vim-javacomplete2'
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'neomake/neomake'

" Initialize plugin system
call plug#end()

"""""""""""""""""""""""""
""""    deoplete     """"
"""""""""""""""""""""""""
let g:deoplete#enable_at_startup = 1
let g:deoplete#omni_patterns = {}
let g:deoplete#omni_patterns.java = '[^. *\t]\.\w*'
let g:deoplete#sources = {}
let g:deoplete#sources._ = []
let g:deoplete#file#enable_buffer_path = 1


"""""""""""""""""""""""""
""""  Java Complete  """"
"""""""""""""""""""""""""
autocmd FileType java setlocal omnifunc=javacomplete#Complete

"""""""""""""""""""""""""
""""     neomake     """"
"""""""""""""""""""""""""
autocmd! BufWritePost,BufEnter * Neomake

"""""""""""""""""""""""""
""""     neoformat   """"
"""""""""""""""""""""""""
augroup astyle
  autocmd!
  autocmd BufWritePre * Neoformat
augroup END
```

Open `nvim` and type `:PlugInstall`.

## Done!

Now, if you open a Java project, you should have auto completion, auto format and lint capabilities.

I will update this blog post with new things as soon as I have them.

## TODO

- [ ] Add Groovy support.
- [ ] Add some screenshots or recording.

