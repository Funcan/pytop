import random
import time
import curses


class PyTop(object):
    def __init__(self, title, datasource):
        self.title = title
        self.stat_sources = []
        self.running = True

    def run(self):
        curses.wrapper(self._mainloop)

    def _mainloop(self, screen):
        self.screen = screen
        while (self.running):
            y, x = screen.getmaxyx()
            stats_win_height = len(self.stat_sources)+2
            stats_win = screen.subwin(stats_win_height, x, 0, 0)
            stats_win.box()
            stats_win.addstr(0, (x/2)-(len(self.title)/2), str(self.title))
            for i, stat_source in enumerate(self.stat_sources):
                label, value = stat_source()
                stats_win.addstr(i + 1, 1, str(label) + ' ' + str(value)) 

            data_win = screen.subwin(y - stats_win_height, x,
                                     stats_win_height, 0)
            data_win.box()
            data_win.addstr(1, 1, "Hello")
            data_win_y, data_win_x = data_win.getyx()

            screen.refresh()

            self._keyscan()

    def _keyscan(self):
        key = self.screen.getch()
        if key == ord('q'):
            self.running = False

    def add_stat_source(self, source, data=None):
        def wrapper():
            if data:
                return source(data)
            else:
                return source()
        self.stat_sources.append(wrapper)

def dummy_stat_source():
    return "SomeKey", random.randint(1, 5)

if __name__ == "__main__":
	top = PyTop("Test TOP", None)
	top.add_stat_source(dummy_stat_source)
        top.run()

