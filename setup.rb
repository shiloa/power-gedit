#!/usr/bin/env ruby

require 'rubygems'
require 'fileutils'

#----------------------------------------------------------
# basically, all this does is create folders, copy files
# and give propper permissions so gedit will be able to 
# access them.
#----------------------------------------------------------

def main
  # force close gedit process if open
  system('killall', 'gedit')
  
  # ***** uncomment the line below to install soothing fonts *****
  # system('sudo apt-get install ttf-bitstream-vera ttf-dejavu ttf-dejavu ttf-dejavu-core ttf-dejavu-extra ttf-liberation')
  
  # copy mime files
  FileUtils.cp_r('mime/.','usr/share/mime/packages')
  FileUtils.chmod_R(0644, '/usr/share/mime/packages/*.xml')
  system('update-mime-database', '/usr/share/mime')
  
  # copy language files
  print "copying language files..."
  FileUtils.cp_r('languages/.', '/usr/share/gtksourceview-2.0/language-specs/')
  system('sudo chmod 644', '/usr/share/gtksourceview-2.0/language-specs/*.lang')
  print "done.\n"
  
  # copy theme files
  print "copying theme files..."
  FileUtils.cp_r('themes/.', '/usr/share/gtksourceview-2.0/styles')
  system('sudo chmod 644', '/usr/share/gtksourceview-2.0/styles/*.xml')
  print "done.\n"
  
  # specify folders  
  gedit_dir = "#{ENV['HOME']}/.gnome2/gedit"
  snippets_dir = "#{gedit_dir}/snippets"
  plugins_dir = "#{gedit_dir}/plugins"

  # create necessary folders for plugins and snippets if they don't exists
  FileUtils.mkdir_p(snippets_dir) unless File.directory?(snippets_dir)
  FileUtils.mkdir_p(plugins_dir) unless File.directory?(plugins_dir)
  
  # copy snippets and plugins
  print "copying snippets and plugins..."
  FileUtils.cp_r('snippets/.', snippets_dir)
  FileUtils.cp_r('plugins/.', plugins_dir)
  print "done.\n"
  
  # give proper permissions to these files (otherwise gedit wont read them)
  system('sudo -R chmod 644', snippets_dir)
  system('sudo -R chmod +x', plugins_dir)
  
  puts "power-gedit setup complete - enjoy!"
  
end

if $FILE == $0
  main
end
