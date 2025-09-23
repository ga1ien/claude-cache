"""Claude Cache - Memory for your AI coding assistant"""

__version__ = "0.7.0"

from .log_watcher import LogWatcher
from .log_processor import LogProcessor
from .success_detector import SuccessDetector
from .knowledge_base import KnowledgeBase
from .context_injector import ContextInjector
from .agent import CacheAgent

__all__ = [
    "LogWatcher",
    "LogProcessor",
    "SuccessDetector",
    "KnowledgeBase",
    "ContextInjector",
    "CacheAgent",
]