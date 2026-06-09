"""
查询缓存模块
使用SQLite缓存查询结果，避免频繁请求12306
"""

import sqlite3
import json
import time
from pathlib import Path
from loguru import logger


class QueryCache:
    """查询缓存"""

    def __init__(self, db_path: str = "cache/train_cache.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_cache (
                    cache_key TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    ttl INTEGER NOT NULL DEFAULT 300
                )
            """)

    def get(self, key: str) -> list | None:
        """获取缓存"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                row = conn.execute(
                    "SELECT data, created_at, ttl FROM query_cache WHERE cache_key = ?",
                    (key,),
                ).fetchone()

                if row is None:
                    return None

                data, created_at, ttl = row
                if time.time() - created_at > ttl:
                    # 缓存过期
                    conn.execute("DELETE FROM query_cache WHERE cache_key = ?", (key,))
                    return None

                return json.loads(data)

        except Exception as e:
            logger.warning(f"读取缓存失败: {e}")
            return None

    def set(self, key: str, data: list, ttl: int = 300):
        """
        写入缓存

        Args:
            key: 缓存键
            data: 缓存数据
            ttl: 有效期（秒），默认5分钟
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO query_cache (cache_key, data, created_at, ttl) VALUES (?, ?, ?, ?)",
                    (key, json.dumps(data, ensure_ascii=False), time.time(), ttl),
                )
        except Exception as e:
            logger.warning(f"写入缓存失败: {e}")

    def clear(self):
        """清空缓存"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM query_cache")
            logger.info("缓存已清空")
        except Exception as e:
            logger.warning(f"清空缓存失败: {e}")
