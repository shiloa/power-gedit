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
sudo apt-get install ttf-bitstream-vera ttf-dejavu ttf-dejavu ttf-dejavu-core ttf-dejavu-extra ttf-liberation

cp snippets/* ~/.gnome2/gedit/snippets/
sudo chmod 644 ~/.gnome2/gedit/snippets/*

cp -R plugins/* ~/.gnome2/gedit/plugins/
sudo chmod +x -R ~/.gnome2/gedit/plugins/