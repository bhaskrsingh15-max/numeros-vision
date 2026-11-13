import asyncio
from starlette.requests import Request

async def dummy_receive():
    return {'type': 'http.request', 'body': b'{"hello": "world"}', 'more_body': False}

scope = {'type': 'http', 'method': 'POST', 'path': '/test', 'headers': []}
req = Request(scope, dummy_receive)

async def test():
    b1 = await req.body()
    b2 = await req.body()
    assert b1 == b2 == b'{"hello": "world"}'
    print("SUCCESS: Body cached properly in Starlette Request!")

if __name__ == "__main__":
    asyncio.run(test())
