import sys
import gtk
import git
import time

class GitModel:

    def __init__(self, place="."):
        self.repo = git.Repo(place)
        assert self.repo.bare == False

        branch = self.repo.heads.master

        self.log = [branch.commit]
        for commit in branch.commit.iter_parents():
            self.log.append(commit)
        self.log.reverse()
        self.steps = len(self.log)

    def format_value(self, scale, value):
        commit = self.log[int(value)]
        return time.asctime(time.gmtime(commit.committed_date))


class Fugit:

    def __init__(self, place):
        self.model = GitModel(place)

        vbox = gtk.VBox()

        self.label = gtk.Label()
        self.infobar = gtk.InfoBar()
        content = self.infobar.get_content_area()
        content.add(self.label)

        adjustment = gtk.Adjustment( self.model.steps, 0, self.model.steps-1)
        adjustment.set_step_increment(1)
        self.timeline = gtk.HScale(adjustment=adjustment)
        self.timeline.set_digits(0)
        self.timeline.set_value_pos(gtk.POS_BOTTOM)
        for i in range(0, self.model.steps):
            self.timeline.add_mark(i, gtk.POS_TOP, None)
        self.timeline.connect("format-value", self.model.format_value)
        self.timeline.connect("value-changed", self.update_infobar)
        self.timeline.connect("value-changed", self.update_browser)

        vbox.pack_start(self.infobar)
        vbox.pack_end(self.timeline)

        hbox = gtk.HBox()
        hbox.pack_start(vbox)

        Arrow = gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_IN)
        Button = gtk.Button()
        Button.connect("clicked", self.prev_node)
        Button.add(Arrow)

        hbox.pack_start(Button, expand=False, fill=False)

        Arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_IN)
        Button = gtk.Button()
        Button.connect("clicked", self.next_node)
        Button.add(Arrow)

        hbox.pack_end(Button, expand=False, fill=False)

        self.update_infobar(self.timeline)

        self.widget = hbox

    def update_infobar(self, timeline):
        value = int(timeline.get_value())
        label = self.model.log[value].message.strip()
        self.label.set_text(label)

    def update_browser(self, timeline):
        index = int(timeline.get_value())
        commit = self.model.log[index]
        index = git.base.IndexFile.from_tree(self.model.repo, commit.tree)
        for (path, stage), entry in index.entries.iteritems():
            print stage,path

    def prev_node(self, button):
        cur = self.timeline.get_value()
        if cur>0:
            self.timeline.set_value(cur-1)

    def next_node(self, button):
        cur = self.timeline.get_value()
        if cur<self.model.steps:
            self.timeline.set_value(cur+1)

if __name__ == "__main__":
    try:
        place = sys.argv[1]
    except IndexError:
        place = "."
    fugit = Fugit(place)

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.add(fugit.widget)
    window.show_all()

    gtk.main()
