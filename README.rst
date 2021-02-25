aiosub
======

aiosub makes an ``asyncio.Protocol`` push events to an ``asyncio.Queue``.
This lets you write a protocol implementation in a single async coroutine.

It is an alternative to the ``asyncio.Reader`` and ``asyncio.Writer`` classes;
it differs by providing a general-purpose patcher for ``asyncio.Protocol`` objects,
thereby retaining support for UDP and user-defined methods.

``aiosub.subscribe()`` accepts a ``asyncio.Protocol`` object and returns an
``asyncio.Queue`` object. Each of the protocol's methods is augmented to put
an ``aiosub.Event`` object on the queue. Events have ``name`` and ``args``
attributes.

See the ``examples/`` directory for example TCP/UDP servers and clients.
