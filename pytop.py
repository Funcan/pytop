import random
import time
import curses
import sys


class PyTop(object):
    def __init__(self, title):
        self.title = title
        self.stat_sources = []
        self.refresh = 5000 # 5 seconds
        self.datasource = None
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
            data_win_y = y - stats_win_height
            data_win_x = x
            data_win.box()
            if self.datasource:
                data = self.datasource()
                column_width = (x - 4) / len(data[0].keys())
                for i, heading in enumerate(data[0].keys()):
                    data_win.addstr(1, i * column_width + 1, str(heading))

                rows = min(data_win_y-2, len(data))
                for row in xrange(0, rows):
                    for i, column in enumerate(data[0].keys()):
                        data_win.addstr(2 + row, i * column_width + 1,
                                        str(data[row][column]))

            self.screen.refresh()

            self.screen.timeout(self.refresh)
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

    def set_data_source(self, source, data=None):
        def wrapper():
            if data:
            	return source(data)
            else:
            	return source()
        self.datasource = wrapper


def dummy_stat_source(name):
    return name, random.randint(1, 5)

def dummy_data_source():
    rows = random.randint(2,30)
    ret = []
    for i in xrange(0,rows):
        item = {}
        item['name'] = random.choice(['something', 'something else', 'a thing',
                                      'some other thing', 'placeholder'])
        item['age'] = random.randint(1, 10)
        item['notes'] = random.choice([None, 'alive', ''])
        ret.append(item)
    return ret


if __name__ == "__main__":
    top = PyTop("Test TOP")
    top.add_stat_source(dummy_stat_source, "foo")
    top.add_stat_source(dummy_stat_source, "bar")
    top.add_stat_source(dummy_stat_source, "baz")
    top.set_data_source(dummy_data_source)
    top.run()
