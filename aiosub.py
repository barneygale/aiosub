import asyncio
import dataclasses
import functools
import inspect


@dataclasses.dataclass
class Event:
    name: str
    args: dict


def subscribe(obj, events=None):
    if events is None:
        events = asyncio.Queue()
    for name in dir(obj):
        fn = getattr(obj, name)
        if inspect.ismethod(fn):
            fn = _wrap(events, name, fn)
            setattr(obj, name, fn)
    return events


def _wrap(events, name, fn):
    sig = inspect.signature(fn)

    @functools.wraps(fn)
    def new_fn(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        event = Event(name, dict(bound.arguments))
        events.put_nowait(event)
        return fn(*args, **kwargs)

    return new_fn
