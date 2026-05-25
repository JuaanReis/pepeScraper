from httpx import Client, Timeout, Limits
from .ip_creator import get_ip
from input import parse_args
args = parse_args()
clients_number = 2      # Number of simultaneous customers.
proxies = args.proxy
ip = get_ip()   # Create a random IP
client_kwargs = {
    "http2": True,
    "timeout": Timeout(4.0, connect=1.5),
    "limits": Limits(
        max_keepalive_connections=70,
        max_connections=70,
    ),
    "headers": {
        "Accept-Encoding": "gzip, deflate",
        "X-Forwarded-For": ip,
        "X-Real-IP": ip,
    }
}

if args.proxy:
    client_kwargs["proxy"] = args.proxy

clients = [
    Client(**client_kwargs)
    for _ in range(clients_number)
]