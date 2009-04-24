# -*- coding: utf8 -*-
#  Advanced editing plugin
#
#  Copyright (C) 2007 Shaddy Zeineddine <shaddyz@users.sourceforge.net>
#  Copyright (C) 2005 Marcus Lunzenauer <mlunzena@uos.de>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import gedit
import gtk

adv_edit_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_3">
        <separator name="AdvancedEditingSep1"/>
        <menuitem name="DeleteLine"          action="DeleteLine"/>
        <menuitem name="DeleteLineBackwards" action="DeleteLineBackwards"/>
        <menuitem name="DuplicateLine"       action="DuplicateLine"/>
        <separator name="AdvancedEditingSep2"/>
        <menuitem name="RemoveWhitespace"    action="RemoveWhitespace"/>
        <menuitem name="ReduceWhitespace"    action="ReduceWhitespace"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class AdvancedEditingPlugin(gedit.Plugin):
  def __init__(self):
    gedit.Plugin.__init__(self)

  def delete_line(self, action, window):
    view = window.get_active_view()
    view.do_delete_from_cursor(view, gtk.DELETE_PARAGRAPH_ENDS, 1)

  def delete_line_bw(self, action, window):
    view = window.get_active_view()
    doc  = window.get_active_document()
    doc.begin_user_action()
    view.do_move_cursor(view, gtk.MOVEMENT_PARAGRAPH_ENDS, -1, 0)
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line();
    line = doc.get_slice(itstart, itend, True)
    doc.delete(itstart, itend);
    doc.end_user_action()

  def duplicate_line(self, action, window):
    view = window.get_active_view()
    doc  = window.get_active_document()
    doc.begin_user_action()
    view.do_move_cursor(view, gtk.MOVEMENT_PARAGRAPH_ENDS, -1, 0)
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line();
    line = doc.get_slice(itstart, itend, True)
    doc.insert_at_cursor(line)
    view.do_move_cursor(view, gtk.MOVEMENT_PARAGRAPHS, -1, 0)
    doc.end_user_action()

  def remove_whitespace(self, action, window):
    view = window.get_active_view()
    view.do_delete_from_cursor(view, gtk.DELETE_WHITESPACE, 1)

  def reduce_whitespace(self, action, window):
    view = window.get_active_view()
    view.do_delete_from_cursor(view, gtk.DELETE_WHITESPACE, 1)
    view.do_insert_at_cursor(view, ' ')

  def activate(self, window):
    actions = [
      ('DeleteLine',          None, 'Delete To End Of Line', '<Shift><Control>j', "Delete To End Of Line", self.delete_line),
      ('DeleteLineBackwards', None, 'Kill Line',             '<Control>j',        "Kill Line",             self.delete_line_bw),
      ('DuplicateLine',       None, 'Duplicate Line',        '<Control>d',        "Duplicate Line",        self.duplicate_line),
      ('RemoveWhitespace',    None, 'Remove Whitespace',     '<Shift><Alt>j',     "Remove Whitespace",     self.remove_whitespace),
      ('ReduceWhitespace',    None, 'Reduce Whitespace',     '<Alt>j',            "Reduce Whitespace",     self.reduce_whitespace)
    ]

    # store per window data in the window object
    windowdata = dict()
    window.set_data("AdvancedEditingPluginWindowDataKey", windowdata)

    windowdata["action_group"] = gtk.ActionGroup("GeditAdvancedEditingPluginActions")
    windowdata["action_group"].add_actions(actions, window)

    manager = window.get_ui_manager()
    manager.insert_action_group(windowdata["action_group"], -1)

    windowdata["ui_id"] = manager.add_ui_from_string(adv_edit_str)

    window.set_data("AdvancedEditingPluginInfo", windowdata)

  def deactivate(self, window):
    windowdata = window.get_data("AdvancedEditingPluginWindowDataKey")
    manager = window.get_ui_manager()
    manager.remove_ui(windowdata["ui_id"])
    manager.remove_action_group(windowdata["action_group"])

  def update_ui(self, window):
    view = window.get_active_view()
    windowdata = window.get_data("AdvancedEditingPluginWindowDataKey")
    windowdata["action_group"].set_sensitive(bool(view and view.get_editable()))
