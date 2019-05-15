class RollingAverage(object):
    # from https://www.quora.com/What-is-the-best-way-of-finding-mean-of-a-stream-at-any-point/answer/Mark-Harrison-2
    def __init__(self):
        self.reset()
    def reset(self):
        self.total = 0
        self.avg = 0.
    def update(self, item):
        self.total += 1
        self.avg += (item-self.avg)/self.total

def _get_still_ranges(x, y, z, thresh=None, minrangesize=None):
    # x, y, z should be of the same length
    results = []
    curr_st = 0
    xavg = RollingAverage()
    yavg = RollingAverage()
    zavg = RollingAverage()

    def _reset_group(idx):
        xavg.reset();xavg.update(x[idx])
        yavg.reset();yavg.update(y[idx])
        zavg.reset();zavg.update(z[idx])

    def _try_save_group(mismatch_idx):
        # we only try saving with indices that don't match, or are
        # out of bounds. So we don't want to include them in our length.
        curr_group_len = mismatch_idx-curr_st
        # we see if our group is longer than minrangesize to keep it.
        if curr_group_len >= minrangesize:
            results.append((curr_st, curr_group_len))

    _reset_group(0) # initialize state properly to first item.

    for idx in range(1, len(x)):
        # should we include this point in current?
        if (
            abs(x[idx]-xavg.avg)<thresh and
            abs(y[idx]-yavg.avg)<thresh and
            abs(z[idx]-zavg.avg)<thresh
        ):
            # since difference from average is within threshold, we keep this point.
            continue
        else:
            _try_save_group(idx)

            # we reset averages and start a new group.
            _reset_group(idx)
            curr_st = idx

    _try_save_group(idx+1)
    return results

if __name__ == '__main__':
    fake_len = 20
    y = z = np.zeros((fake_len, 1))
    x = np.zeros((fake_len, 1))
    x[10] = 10
    x[11:] = 20

    assert _get_still_ranges(x, y, z, thresh=5, minrangesize=2) == [(0, 10), (11, 9)]
    assert _get_still_ranges(x, y, z, thresh=5, minrangesize=1) == [(0, 10), (10, 1), (11, 9)]
    assert _get_still_ranges(x, y, z, thresh=50, minrangesize=1) == [(0, 20)]
