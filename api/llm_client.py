"""
LLM客户端封装 - 支持OpenAI兼容API调用
提供流式输出、错误重试、超时控制和优雅降级
"""

import os
import json
import time
from typing import Optional, Generator, AsyncIterator
import requests
from loguru import logger

# 尝试导入dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("dotenv未安装，将从环境变量读取配置")


class LLMConfig:
    """LLM配置"""

    def __init__(self):
        self.api_key: str = os.getenv("LLM_API_KEY", "")
        self.base_url: str = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
        self.model: str = os.getenv("LLM_MODEL", "deepseek-chat")
        self.timeout: int = 60  # 超时秒数
        self.max_retries: int = 3  # 最大重试次数

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.api_key and self.base_url)

    def __repr__(self) -> str:
        return f"LLMConfig(base_url={self.base_url}, model={self.model})"


class LLMClient:
    """
    LLM客户端封装

    支持：
    - OpenAI兼容API调用
    - 流式输出（SSE）
    - 错误处理和重试
    - 超时控制
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> str | Generator[str, None, None]:
        """
        发送对话请求

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成token数
            stream: 是否使用流式输出

        Returns:
            如果stream=False，返回完整响应字符串
            如果stream=True，返回生成器
        """
        if not self.config.is_configured():
            raise LLMNotConfiguredError("LLM未配置，请设置LLM_API_KEY、LLM_BASE_URL等环境变量")

        # 构建请求
        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if stream:
            payload["stream"] = True
            return self._stream_request(url, headers, payload)

        return self._request_with_retry(url, headers, payload)

    def _request_with_retry(
        self,
        url: str,
        headers: dict,
        payload: dict,
    ) -> str:
        """
        带重试的请求

        Args:
            url: 请求URL
            headers: 请求头
            payload: 请求体

        Returns:
            响应内容
        """
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=self.config.timeout,
                )
                response.raise_for_status()

                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise LLMResponseError(f"无效的响应格式: {data}")

            except requests.exceptions.Timeout as e:
                last_error = e
                logger.warning(f"请求超时（第{attempt + 1}次尝试）")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避

            except requests.exceptions.RequestException as e:
                last_error = e
                logger.warning(f"请求失败（第{attempt + 1}次尝试）: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)

            except (KeyError, ValueError, json.JSONDecodeError) as e:
                last_error = LLMResponseError(f"响应解析失败: {e}")
                logger.error(f"响应解析失败: {e}")
                break

        raise LLMRequestError(f"请求失败，已重试{self.config.max_retries}次: {last_error}")

    def _stream_request(
        self,
        url: str,
        headers: dict,
        payload: dict,
    ) -> Generator[str, None, None]:
        """
        流式请求

        Args:
            url: 请求URL
            headers: 请求头
            payload: 请求体

        Yields:
            逐个返回生成的文本片段
        """
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.config.timeout,
                stream=True,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue

        except requests.exceptions.RequestException as e:
            logger.error(f"流式请求失败: {e}")
            raise LLMRequestError(f"流式请求失败: {e}")


class LLMError(Exception):
    """LLM相关错误基类"""
    pass


class LLMNotConfiguredError(LLMError):
    """LLM未配置错误"""
    pass


class LLMRequestError(LLMError):
    """LLM请求错误"""
    pass


class LLMResponseError(LLMError):
    """LLM响应解析错误"""
    pass


# 全局客户端实例
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """获取全局LLM客户端"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def check_llm_status() -> dict:
    """
    检查LLM配置状态

    Returns:
        状态信息字典
    """
    config = LLMConfig()
    return {
        "configured": config.is_configured(),
        "base_url": config.base_url,
        "model": config.model,
        "has_api_key": bool(config.api_key),
    }
