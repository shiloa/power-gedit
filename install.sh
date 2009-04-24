#!/bin/sh
set -v

killall gedit

# register rails-related mime types
sudo cp rails.xml /usr/share/mime/packages
sudo chmod 644 /usr/share/mime/packages/*.xml
sudo update-mime-database /usr/share/mime

# install syntax definitions for erb, yaml, haml and sass
sudo cp languages/*.lang /usr/share/gtksourceview-2.0/language-specs/
sudo chmod 644 /usr/share/gtksourceview-2.0/language-specs/*.lang

# install themes
sudo cp themes/*.xml /usr/share/gtksourceview-2.0/styles
sudo chmod 644 /usr/share/gtksourceview-2.0/styles/*.xml

# install some fonts
sudo apt-get install ttf-bitstream-vera ttf-dejavu ttf-dejavu ttf-dejavu-core ttf-dejavu-extra ttf-liberation ttf-mscorefonts-installer

if [ ! -d $HOME/.gnome2/gedit ] 
then
  mkdir -p ~/.gnome2/gedit
  cp -r snippets ~/.gnome2/gedit/
  sudo chmod 644 ~/.gnome2/gedit/snippets/*
fi


if [ ! -d $HOME/.gnome2/gedit/snippets ]
then
  mkdir -p ~/.gnome2/gedit/snippets
fi
cp snippets/* ~/.gnome2/gedit/snippets/
sudo chmod 644 ~/.gnome2/gedit/snippets/*

if [ ! -d $HOME/.gnome2/gedit/plugins ]
then
  mkdir -p ~/.gnome2/gedit/plugins
fi

cp -R plugins/* ~/.gnome2/gedit/plugins/
sudo chmod +x -r ~/.gnome2/gedit/plugins/


