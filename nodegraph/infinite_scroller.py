class InfiniteScroller:
    def __init__(self):
        self.horizontal_callback = None
        self.vertical_callback = None
        self.cursor_callback = None
        self._started = False

    def set_region(self, left: int, right: int, top: int, bottom: int):
        self._left = left
        self._right = right
        self._top = top
        self._bottom = bottom

    def start(self, x, y):
        self._last_x = x
        self._last_y = y
        self._started = True

    def end(self):
        self._started = False

    def solve(self, raw_x: int, raw_y: int):
        if not self._started:
            return

        if self.horizontal_callback:
            diff_x = raw_x - self._last_x
            if abs(diff_x) > 10:
                a = 1
            self.horizontal_callback(diff_x)
        if self.vertical_callback:
            diff_y = raw_y - self._last_y
            self.vertical_callback(diff_y)

        if self.cursor_callback:
            new_x, new_y = raw_x, raw_y
            no_x, no_y = False, False

            if raw_x < self._left:
                new_x = self._right + raw_x - self._left
            elif raw_x > self._right:
                new_x = self._left + raw_x - self._right
            else:
                no_x = True

            if raw_y < self._top:
                new_y = self._bottom + raw_y - self._top
            elif raw_y > self._bottom:
                new_y = self._top + raw_y - self._bottom
            else:
                no_y = True

            if no_x and no_y:
                self._last_x = raw_x
                self._last_y = raw_y
            elif no_x:
                self.cursor_callback(raw_x, new_y)
                self._last_x = raw_x
                self._last_y = new_y
            elif no_y:
                self.cursor_callback(new_x, raw_y)
                self._last_x = new_x
                self._last_y = raw_y
            else:
                self.cursor_callback(new_x, new_y)
                self._last_x = new_x
                self._last_y = new_y
        else:
            self._last_x = raw_x
            self._last_y = raw_y
