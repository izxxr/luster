# luster
Python library for Revolt.chat API.

> :warning: **Acknowledgement**
>
> This library is not yet complete and is currently in it's early development stage.
> Do not use this for production yet. Expect bugs and other issues. The library is
> is in active development and will be complete and production ready soon.

## Features
- Modern and easy to use interface
- Supports both bots and users API
- Provides full control over low level API
- Up-to-date type definitions for Revolt API

## Installation
You can install this library using the Python's traditional package manager, `pip`.
```sh
$ pip install luster
```
Note that **Python 3.8 or higher** is required.

The only required dependency for this library is `aiohttp`. There are certain dependencies
that you can install in order to enhance the speed of the library.

- `msgpack` (Faster websocket packets parsing)
- `ujson` (Faster JSON parsing)
- `aiohttp[speed]` (Speed ups for `aiohttp`)

These dependencies can be installed by:
```sh
$ pip install luster[speed]
```

## Basic Usage
> :information_source: Type annotations are not required.

```py
import luster

client = luster.Client(token="...")

@client.listen(luster.WebsocketEvent.AUTHENTICATED)
async def handle_authenticated(event: luster.events.Authenticated):
    print("Client has connected!")

client.launch()
```

## Contributing
This library is still in it's alpha (0.x) phase and is undergoing active development to
provide 100% coverage of Revolt API. Any kind of contribution is welcomed. 
See [Contribution guidelines](https://github.com/nerdguyhmad/luster/blob/main/CONTRIBUTING.MD) for
more information.
