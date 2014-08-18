import os
import gtk
import gobject
from sugar.graphics import style

_EXCLUDE_EXTENSIONS = ('.pyc', '.pyo', '.so', '.o', '.a', '.la', '.mo', '~',
                       '.xo', '.tar', '.bz2', '.zip', '.gz', '.swp')
_EXCLUDE_NAMES = ['.deps', '.libs', '.git']

class FileViewer(gtk.ScrolledWindow):
    __gtype_name__ = 'SugarFileViewer'

    __gsignals__ = {
        'file-selected': (gobject.SIGNAL_RUN_FIRST,
                           gobject.TYPE_NONE,
                           ([str])),
    }

    def __init__(self, path, initial_filename=None):
        gtk.ScrolledWindow.__init__(self)

        self.props.hscrollbar_policy = gtk.POLICY_AUTOMATIC
        self.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
        self.set_size_request(style.GRID_CELL_SIZE * 3, -1)

        self._path = None
        self._initial_filename = initial_filename

        self._tree_view = gtk.TreeView()
        self.add(self._tree_view)
        self._tree_view.show()

        self._tree_view.props.headers_visible = False
        selection = self._tree_view.get_selection()
        selection.connect('changed', self.__selection_changed_cb)

        #renderer = gtk.CellRendererPixbuf()
        #renderer.set_property('stock-id', gtk.STOCK_DIRECTORY)

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn()
        #column.pack_start(renderer, True)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 0)
        self._tree_view.append_column(column)
        self._tree_view.set_search_column(0)

        self.set_path(path)

    def set_path(self, path):
        self.emit('file-selected', None)
        if self._path == path:
            return

        self._path = path
        self._tree_view.set_model(gtk.TreeStore(str, str))
        self._model = self._tree_view.get_model()
        self._add_dir_to_model(path)

    def _add_dir_to_model(self, dir_path, parent=None):
        dir_list = sorted(os.listdir(dir_path))
        #file_list = sorted([f for f in os.listdir(dir_path) if os.path.isfile(f)])
        for f in dir_list:
            if f.endswith(_EXCLUDE_EXTENSIONS) or f in _EXCLUDE_NAMES:
                continue

            full_path = os.path.join(dir_path, f)
            if os.path.isdir(full_path):
                new_iter = self._model.append(parent, [f, full_path])
                self._add_dir_to_model(full_path, new_iter)
            else:
                current_iter = self._model.append(parent, [f, full_path])
                if f == self._initial_filename:
                    if parent:
                        treepath = self._model.get_path(current_iter)
                        self._tree_view.expand_to_path(treepath)
                    selection = self._tree_view.get_selection()
                    selection.select_iter(current_iter)
                    self.thisisit = current_iter

    def __selection_changed_cb(self, selection):
        model, tree_iter = selection.get_selected()
        if tree_iter is None:
            file_path = None
        else:
            file_path = model.get_value(tree_iter, 1)
        self.emit('file-selected', file_path)


