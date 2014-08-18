# -*- coding: utf-8 -*-
import os
import gtk
import gobject
from sugar.graphics import style

try:
    import gtksourceview2
except ImportError:
    import platform
    if platform.machine()=='armv7l':
        from libraries.armv7l import gtksourceview2
    elif platform.machine()=='i686':
        from libraries.i686 import gtksourceview2
    else:
        gtksourceview2 = None
from pango import FontDescription

class SourceView(gtksourceview2.View):
    """
    Visor de código para archivos abiertos.
    Realmente no todos comprenderán las virtudes de VIM.
    """

    def __init__(self):
        gtksourceview2.View.__init__(self)

        self.archivo = False

        self.set_show_line_numbers(True)

        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        self.set_auto_indent(True)

        font = "Monospace " + str(int(10/style.ZOOM_FACTOR))
        self.modify_font(FontDescription(font))

        self.show_all()

    def close(self):
        pass

    def init_syntax(self):
        text_buffer = self.get_buffer()
        lang_manager = gtksourceview2.language_manager_get_default()
        if hasattr(lang_manager, 'list_languages'):
            langs = lang_manager.list_languages()
        else:
            lang_ids = lang_manager.get_language_ids()
            langs = [lang_manager.get_language(lang_id)
                     for lang_id in lang_ids]
        for lang in langs:
            for m in lang.get_mime_types():
                if m == "text/x-python":
                    text_buffer.set_language(lang)

        if hasattr(text_buffer, 'set_highlight'):
            text_buffer.set_highlight(True)
        else:
            text_buffer.set_highlight_syntax(True)

        mgr = gtksourceview2.style_scheme_manager_get_default()
        style_scheme = mgr.get_scheme('oblivion')
        self.get_buffer().set_style_scheme(style_scheme)

    def open_file(self, widget, archivo):
        """
        Setea el archivo cuyo codigo debe mostrarse.
        """

        if archivo:
            if os.path.isfile(archivo):
                self.archivo = archivo
                texto_file = open(self.archivo, 'r')
                texto = texto_file.read()
                texto_file.close()

                self.set_buffer(gtksourceview2.Buffer())
                self.get_buffer().begin_not_undoable_action()
                #self.__set_lenguaje(self.archivo)
                self.get_buffer().set_text(texto)

                nombre = os.path.basename(self.archivo)
                self.control = os.path.getmtime(self.archivo)
        else:
            self.set_buffer(gtksourceview2.Buffer())
            self.get_buffer().begin_not_undoable_action()

        self.get_buffer().end_not_undoable_action()
        self.get_buffer().set_modified(False)

        pos = self.get_iter_at_location(1,1)
        self.get_buffer().place_cursor(pos)
        self.scroll_to_iter(pos, False)

        self.grab_focus()
        self.init_syntax()

    def save_file(self):
        if self.archivo:
            buffer = self.get_buffer()

            if buffer.get_modified() and os.path.exists(self.archivo):

                inicio, fin = buffer.get_bounds()
                texto = buffer.get_text(inicio, fin, 0)

                archivo = open(self.archivo, "w")
                archivo.write(texto)
                archivo.close()

                buffer.set_modified(False)
                self.control = os.path.getmtime(self.archivo)

    def modificado(self):
        return self.get_buffer().get_modified()

    def current_file(self):
        return os.path.realpath(self.archivo)

