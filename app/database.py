import sqlite3
from dataclasses import dataclass

import asyncpg


@dataclass
class GEORepository:
    database_url: str

    async def connect(self) -> None:
        self.connection = await asyncpg.connect(self.database_url)
    
    async def disconnect(self) -> None:
        await self.connection.close()