# -*- coding: utf-8 -*-
import os, sys

from gettext import gettext as _
import gtk
import gobject
import sugar.activity.activity

import logging
import traceback
import helpbutton

from sugar.graphics import style
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.activity.widgets import StopButton
from sugar.graphics.alert import NotifyAlert

from console.interactiveconsole import GTKInterpreterConsole
from fileviewer import FileViewer
from sourceview import SourceView
from fugit import Fugit

class Activity(sugar.activity.activity.Activity):
    def __init__(self, handle):
        super(Activity, self).__init__(handle)

        self.build_toolbar()
        self.build_editor()

        self.p = gtk.VPaned()
        self.set_canvas(self.p)
        self.p.pack2(self.h)
        
        self.console = gtk.Notebook()
        self.init_interpreter()
        self.console.append_page(self.interpreter)
        self.p.pack1(self.console)

        self.fugit = Fugit(".")
        self.console.append_page(self.fugit.widget)
        self.show_all()


    def alert(self, title=None, text=None, delay=5):
        alert = NotifyAlert(delay)
        alert.props.title = title
        alert.props.msg = text
        self.add_alert(alert)
        alert.connect('response', self._alert_ok)
        alert.show()

    def _alert_ok(self, alert, *args):
        self.remove_alert(alert)

    def init_interpreter(self):
        frame = self.get_frame()
        self.interpreter = GTKInterpreterConsole(frame)
        self.interpreter.text.connect('button-press-event', self.focus_interpreter)
        return False

    def focus_interpreter(self, widget, event):
        self.interpreter.text.grab_focus()
        return True

    def get_frame(self):
        # esto es necesario para que la consola funcione
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame
        return frame

    def open_file(self, widget, path):
        if path:
            if not os.path.isdir(path):
                self.editor.open_file(widget, path)

    def save_file(self, widget):
        if self.editor.modificado():
            self.editor.save_file()
            filename = self.editor.current_file()
            self.alert(filename, "Archivo guardado.")

    def build_editor(self):
        self.h = gtk.HPaned()
        self.tree = FileViewer(".") 
        self.tree.connect("file-selected", self.open_file)
        self.tree.show()
        self.h.pack1(self.tree)

        self.editor = SourceView()

        scroller = gtk.ScrolledWindow()
        scroller.set_policy(gtk.POLICY_AUTOMATIC,
                      gtk.POLICY_AUTOMATIC)
        scroller.add(self.editor)
        self.h.pack2(scroller)

        self.h.show_all()

    def build_reader(self):
        self.reader = webkit.WebView()
        curdir = os.getcwd()
        self.reader.load_uri("file://%s/docs/index.html" % curdir)
        self.box.append_page(self.reader, gtk.Label("Lector"))
        self.reader.show()

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        tool_group = None

        self.game_button = RadioToolButton()
        self.game_button.props.icon_name = 'gamecanvas'
        self.game_button.set_tooltip(_('Juego'))
        self.game_button.accelerator = "<Ctrl>1"
        self.game_button.props.group = tool_group
        #self.game_button.connect('clicked', self.show_game)
        toolbar_box.toolbar.insert(self.game_button, -1)
        self.game_button.show()
        tool_group = self.game_button

        button = RadioToolButton()
        button.props.icon_name = 'view-source'
        button.set_tooltip(_('Editor'))
        button.accelerator = "<Ctrl>2"
        button.props.group = tool_group
        #button.connect('clicked', self.show_editor)
        toolbar_box.toolbar.insert(button, -1)
        button.show()

        self.save_button = ToolButton('dialog-ok')
        self.save_button.set_tooltip(_('Guardar'))
        self.save_button.accelerator = "<Ctrl>s"
        self.save_button.connect('clicked', self.save_file)
        toolbar_box.toolbar.insert(self.save_button, -1)
        self.save_button.show()

        separator = gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        self.editor_button = ToolButton('sources')
        self.editor_button.set_tooltip(_('Consola'))
        self.editor_button.accelerator = "<Ctrl>grave"
        self.editor_button.connect('clicked', self.toggle_console)
        toolbar_box.toolbar.insert(self.editor_button, -1)
        self.editor_button.show()

        separator = gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        button = helpbutton.HelpButton(self)
        toolbar_box.toolbar.insert(button, -1)
        button.show()

        # Blank space (separator) and Stop button at the end:

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass

    def can_close(self):
        if self.editor:
            self.editor.close()
        return True

    def toggle_console(self, e):
        if self.console.props.visible:
            self.console.hide()
        else:
            self.p.set_position(160)
            self.console.show()
            self.console.text.grab_focus()
