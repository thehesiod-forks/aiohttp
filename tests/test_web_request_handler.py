from unittest import mock

from aiohttp import web
from aiohttp.test_utils import make_mocked_coro


def test_repr(loop):
    app = web.Application()
    manager = app.make_handler(loop=loop)
    handler = manager()

    assert '<RequestHandler disconnected>' == repr(handler)

    handler.transport = object()
    assert '<RequestHandler connected>' == repr(handler)


def test_connections(loop):
    app = web.Application()
    manager = app.make_handler(loop=loop)
    assert manager.connections == []

    handler = object()
    transport = object()
    manager.connection_made(handler, transport)
    assert manager.connections == [handler]

    manager.connection_lost(handler, None)
    assert manager.connections == []


async def test_shutdown_no_timeout(loop):
    app = web.Application()
    manager = app.make_handler(loop=loop)

    handler = mock.Mock()
    handler.shutdown = make_mocked_coro(mock.Mock())
    transport = mock.Mock()
    manager.connection_made(handler, transport)

    await manager.shutdown()

    manager.connection_lost(handler, None)
    assert manager.connections == []
    handler.shutdown.assert_called_with(None)


async def test_shutdown_timeout(loop):
    app = web.Application()
    manager = app.make_handler(loop=loop)

    handler = mock.Mock()
    handler.shutdown = make_mocked_coro(mock.Mock())
    transport = mock.Mock()
    manager.connection_made(handler, transport)

    await manager.shutdown(timeout=0.1)

    manager.connection_lost(handler, None)
    assert manager.connections == []
    handler.shutdown.assert_called_with(0.1)
