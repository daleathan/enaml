#------------------------------------------------------------------------------
# Copyright (c) 2020, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
import pytest

from enaml.signaling import Signal, BoundSignal


class SignalTester:

    signal = Signal()

    def __init__(self):
        self.counter = 0
        self.last_args = None
        self.lastkwargs = None

    def slot(self, *args, **kwargs):
        self.counter += 1
        self.last_args = args
        self.last_kwargs = kwargs


def test_signal_lifetime():
    """Test creating, connecting, emitting and disconnecting a signal.

    """
    s = SignalTester()
    assert isinstance(s.signal, BoundSignal)
    s.signal.connect(s.slot)

    # s.signal.emit(1, 2, 3, a=1, b=2)
    # assert s.counter == 1
    # assert s.last_args == (1, 2, 3)
    # assert s.lastkwargs == dict(a=1, b=2)

    # s.signal(4, 5, c=5, h=6)
    # assert s.counter == 2
    # assert s.last_args == (4, 5)
    # assert s.lastkwargs == dict(c=5, h=6)

    # s.signal.disconnect(s.slot)
    # s.signal(1)
    # assert s.counter == 2


def test_signal_disconnect_all():
    """Test disconnecting all slots connected the bound signals.

    """
    c = 0
    def dummy_slot():
        nonlocal c
        c += 1

    s = SignalTester()
    # s.signal.connect(s.slot)
    # s.signal(4, 5, c=5, h=6)
    # assert s.counter == 1

    # s.signal.connect(dummy_slot)
    # s.emit()
    # assert s.counter == 2
    # assert c == 1

    SignalTester.signal.disconnect_all(s)
    # s.emit()
    # assert s.counter == 2
    # assert c == 1


def test_signal_bad_creation():
    """Test handling bad arguments to Signal.

    """
    with pytest.raises(TypeError):
        Signal(1)

    with pytest.raises(TypeError):
        Signal(a=1)


# def test_signal_set_del():
#     """Test setting/deleting a signal

#     """
#     s = Signal()
#     with pytest.raises(AttributeError):
#         s.signal = 1

#     s = SignalTester()
#     s.signal.connect(s.slot)
#     s.signal(4, 5, c=5, h=6)
#     assert s.counter == 1

#     del s.signal
#     s.emit()
#     assert s.counter == 1


def test_bound_signal_comparison():
    """Test comparing different bound signals.

    """
    s = SignalTester()
    assert s.signal == s.signal


def test_manual_bound_signal_creation():
    """Test creating manually a BoundSignal.

    """
    s = SignalTester()
    with pytest.raises(TypeError):
        sb = BoundSignal(SignalTester.signal, s)

    import weakref
    sb = BoundSignal(SignalTester.signal, weakref.WeakMethod(s.slot))
