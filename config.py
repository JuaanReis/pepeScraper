import httpx

debug = False   
max_threads = 150
logo = True
output_print = True

client = httpx.Client(
    http2=True,
    timeout=httpx.Timeout(5.0, connect=2.5),
    limits=httpx.Limits(
        max_keepalive_connections=100,
        max_connections=250
    ),
    headers={
        "Connection": "keep-alive",
        "Accept-Encoding": "br, gzip"
    }
)