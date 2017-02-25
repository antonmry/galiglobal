title=Trying Polymer just for fun
date=2017-02-04
type=post
tags=Frontend
status=draft
~~~~~~

https://www.polymer-project.org/1.0/start/toolbox/set-up

```
sudo dnf install nodejs npm
sudo su -
npm install -g bower
npm install -g polymer-cli
npm install http-server -g
npm install polyserve -g
exit

git clone git@github.com:galidev/galidev-frontend.git
cd galidev-frontend
polymer init starter-kit
polymer serve --open
```

## Add a third-party element

```
bower install --save syntax-highlight
bower install --save paper-checkbox
```

## Publish it

```
polymer build
```

## See available webcomponents

```
polyserve
```
