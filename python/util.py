import math


def read(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text


def pairwise(list):
    for i in xrange(0, len(list) - 1):
        yield list[i], list[i + 1]


def both(a, b):
    assert len(a) == len(b)
    for i in xrange(len(a)):
        yield a[i], b[i], i


def collect_between(list, a, b):
    res = []
    it = iter(list)
    x = it.next()
    while not a(x):
        x = it.next()
    while not b(x):
        res.append(x)
        x = it.next()
    res.append(x)
    return res


def point_distance(a, b):
    return math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)


def point_line_segment_distance(a, b, p):
    (x1, y1) = a
    (x2, y2) = b
    (x3, y3) = p
    px = x2 - x1
    py = y2 - y1
    q = px * px + py * py
    u = ((x3 - x1) * px + (y3 - y1) * py) / float(q)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    dist = math.sqrt(dx * dx + dy * dy)
    return dist


def point_line_distance(a, b, l):
    num = abs((b[1] - a[1]) * l[0] - (b[0] - a[0])
              * l[1] + b[0] * a[1] - b[1] * a[0])
    denom = point_distance(a, b)
    return float(num) / denom


def fancy_time_diff(this, that=None):
    def test_same_t(this, that, t):
        if not this or not that:
            return False
        if len(this) != len(that):
            return False
        return this[t] == that[t]
    time_diffs = []
    instr = []
    same_t = True
    diff_start_t = 0
    for i in xrange(len(this)):
        if test_same_t(this, that, i):
            if same_t:
                # Still the same
                continue
            else:
                # Now the same
                same_t = True
                time_diffs.append(
                    (diff_start_t, i - 1)
                )
        else:
            if same_t:
                # No longer the same
                same_t = False
                diff_start_t = i
            else:
                # Still not the same
                continue
    if not same_t:
        time_diffs.append((diff_start_t, len(this) - 1))
    for (start, end) in time_diffs:
        color = this[start]
        last_switch = start
        for i in xrange(start + 1, end + 1):
            if this[i] != this[i - 1]:
                instr.append((
                    last_switch,
                    i - 1,
                    this[last_switch]
                ))
                last_switch = i
                color = this[i]
        instr.append((last_switch, end, color))
    return instr


def snap_to(x, n):
    q = math.floor(float(x) / n)
    r = x % n
    return n * (int(r >= float(n) / 2) + q)
