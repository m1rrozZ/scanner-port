# src/porscanner/scanner.py - Made by Alex M.

from __future__ import annotations
import asyncio
import socket
from dataclasses import dataclass
from typing import Iterable, Optional

@dataclass
class ScanResult:
    port: int
    is_open: bool
    service: Optional[str] = None

# A simple synchronous port scanner function
def _lookup_service(port: int) -> Optional[str]:
    # Best-effort lookup of the well-known service name for a port.
    try:
        return socket.getservbyport(port, "tcp")
    except (socket.error, OSError):
        return None 

# An asynchronous port scanner function
async def scan_port(host: str, port: int, timeout: float = 1.0) -> ScanResult:
    # Try to open a TCP connection to (host, port).
 
    # Returns a ScanResult describing whether the port is open, and the
    # guessed service name if it is.
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
    except (asyncio.TimeoutError, OSError):
        return ScanResult(port=port, is_open=False)
    
    writer.close()
    try:
        await writer.wait_closed()
    except OSError:
        pass
    
    return ScanResult(port=port, is_open=True, service=_lookup_service(port))


# An asynchronous function to scan multiple ports concurrently
async def scan_ports(
        host: str, 
        ports: Iterable[int], 
        concurrency: int = 100, 
        timeout: float = 1.0
        ) -> list[ScanResult]:
    # Scan multiple ports concurrently using asyncio.
    semaphore = asyncio.Semaphore(concurrency)

    async def _bounded_scan(port: int) -> ScanResult:
        async with semaphore:
            return await scan_port(host, port, timeout)
        
        tasks = [_bounded_scan(port) for port in ports]
        return await asyncio.gather(*tasks)


# A function to parse a port range string and return a range object
def parse_port_range(port_range: str) -> range:
    # Parse a port range string like "1-1024" and return a range object.
    try:
        start_port, end_port = port_range.split("-")
        start, end = int(start_port), int(end_port)
    except ValueError as exs:
        raise ValueError(f"Invalid port range: {port_range}") from exs
    
    if not (1 <= start <= end <= 65535):
        raise ValueError(f"Port range must be between 1 and 65535: {port_range}")
    
    return range(start, end + 1)