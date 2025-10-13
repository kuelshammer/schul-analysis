"""
Advanced Performance Caching System for Schul-Analysis Framework.

This module implements a comprehensive caching system with:
- Smart cache invalidation based on parameter changes
- Cache statistics and monitoring
- Domain-specific caching for different mathematical operations
- Memory management and optimization
"""

import time
import hashlib
import json
from functools import wraps, lru_cache
from typing import Any, Dict, Optional, Union, Callable, TypeVar, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from sympy import Expr, Symbol, simplify, expand, factor, diff, solve, integrate
from .config_enhanced import config

T = TypeVar("T")
R = TypeVar("R")


class CacheOperation(Enum):
    """Types of cached mathematical operations."""

    SIMPLIFICATION = "simplification"
    EXPANSION = "expansion"
    FACTORIZATION = "factorization"
    DIFFERENTIATION = "differentiation"
    INTEGRATION = "integration"
    SOLVING = "solving"
    EVALUATION = "evaluation"
    NULLSTELLEN = "nullstellen"
    EXTREMA = "extrema"
    WENDEPUNKTE = "wendepunkte"


class CachePriority(Enum):
    """Priority levels for cache entries."""

    HIGH = 3  # Frequently used operations
    MEDIUM = 2  # Normal operations
    LOW = 1  # Rarely used operations


@dataclass
class CacheEntry:
    """A single cache entry with metadata."""

    key: str
    value: Any
    operation: CacheOperation
    priority: CachePriority
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    size_in_bytes: int = 0

    def __post_init__(self):
        """Calculate size in bytes after initialization."""
        self.size_in_bytes = self._calculate_size()

    def _calculate_size(self) -> int:
        """Estimate memory usage in bytes."""
        try:
            return len(json.dumps(self.key, default=str)) + len(str(self.value))
        except:
            return len(str(self.key)) + len(str(self.value))


class PerformanceCache:
    """
    Advanced performance cache with smart management.

    Features:
    - Priority-based eviction
    - Memory management
    - Statistics tracking
    - Domain-specific caching
    - Smart invalidation
    """

    def __init__(self, max_size_mb: int = 50, max_entries: int = 1000):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_entries = max_entries
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_size_bytes": 0,
            "creation_time": time.time(),
        }
        self._operation_stats = {
            op.value: {"hits": 0, "misses": 0} for op in CacheOperation
        }

    def _generate_key(
        self, operation: CacheOperation, expression: Expr, *args, **kwargs
    ) -> str:
        """Generate a unique cache key based on expression and parameters."""
        # Create a deterministic string representation
        expr_str = str(expression)
        args_str = str(args)
        kwargs_str = str(sorted(kwargs.items()))

        # Combine all components
        combined = f"{operation.value}:{expr_str}:{args_str}:{kwargs_str}"

        # Use hash for consistent key length
        return hashlib.md5(combined.encode()).hexdigest()

    def _should_evict(self) -> bool:
        """Check if we should evict entries based on size or count."""
        return (
            len(self._cache) >= self.max_entries
            or self._stats["total_size_bytes"] >= self.max_size_bytes
        )

    def _evict_entries(self):
        """Evict entries based on LRU with priority consideration."""
        if not self._should_evict():
            return

        # Sort by: priority (low first), then last_accessed (oldest first)
        entries = sorted(
            self._cache.values(), key=lambda x: (x.priority.value, x.last_accessed)
        )

        # Calculate how many entries to remove
        remove_count = max(
            int(len(self._cache) * 0.2),  # Remove 20% of entries
            len(self._cache) - self.max_entries + 1,
        )

        # Remove entries
        for entry in entries[:remove_count]:
            del self._cache[entry.key]
            self._stats["total_size_bytes"] -= entry.size_in_bytes
            self._stats["evictions"] += 1

    def get(
        self, operation: CacheOperation, expression: Expr, *args, **kwargs
    ) -> Optional[Any]:
        """Get a value from cache."""
        key = self._generate_key(operation, expression, *args, **kwargs)

        if key in self._cache:
            entry = self._cache[key]
            entry.last_accessed = time.time()
            entry.access_count += 1

            self._stats["hits"] += 1
            self._operation_stats[operation.value]["hits"] += 1

            if config.debug.cache_statistiken:
                config.cache_hit()

            return entry.value

        self._stats["misses"] += 1
        self._operation_stats[operation.value]["misses"] += 1

        if config.debug.cache_statistiken:
            config.cache_miss()

        return None

    def set(
        self,
        operation: CacheOperation,
        expression: Expr,
        value: Any,
        priority: CachePriority = CachePriority.MEDIUM,
        *args,
        **kwargs,
    ):
        """Set a value in cache."""
        key = self._generate_key(operation, expression, *args, **kwargs)

        # Remove existing entry if it exists
        if key in self._cache:
            self._stats["total_size_bytes"] -= self._cache[key].size_in_bytes
            del self._cache[key]

        # Create new entry
        entry = CacheEntry(key=key, value=value, operation=operation, priority=priority)

        # Check if we need to evict entries
        self._evict_entries()

        # Add new entry
        self._cache[key] = entry
        self._stats["total_size_bytes"] += entry.size_in_bytes

    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._stats["total_size_bytes"] = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total_requests if total_requests > 0 else 0

        # Calculate operation-specific hit rates
        operation_hit_rates = {}
        for op_name, stats in self._operation_stats.items():
            op_total = stats["hits"] + stats["misses"]
            op_hit_rate = stats["hits"] / op_total if op_total > 0 else 0
            operation_hit_rates[op_name] = {
                "hit_rate": op_hit_rate,
                "hits": stats["hits"],
                "misses": stats["misses"],
                "total": op_total,
            }

        return {
            "overall": {
                "hit_rate": hit_rate,
                "hits": self._stats["hits"],
                "misses": self._stats["misses"],
                "total_requests": total_requests,
                "evictions": self._stats["evictions"],
                "entries_count": len(self._cache),
                "total_size_mb": self._stats["total_size_bytes"] / (1024 * 1024),
                "max_size_mb": self.max_size_bytes / (1024 * 1024),
                "uptime_seconds": time.time() - self._stats["creation_time"],
            },
            "by_operation": operation_hit_rates,
        }

    def get_top_entries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most frequently accessed cache entries."""
        entries = sorted(
            self._cache.values(), key=lambda x: x.access_count, reverse=True
        )

        return [
            {
                "operation": entry.operation.value,
                "access_count": entry.access_count,
                "last_accessed": entry.last_accessed,
                "created_at": entry.created_at,
                "size_kb": entry.size_in_bytes / 1024,
                "priority": entry.priority.name,
            }
            for entry in entries[:limit]
        ]


# Global cache instance
_global_cache = PerformanceCache()


def cached_operation(
    operation: CacheOperation, priority: CachePriority = CachePriority.MEDIUM
):
    """
    Decorator for caching mathematical operations.

    Args:
        operation: Type of operation being cached
        priority: Priority level for this operation
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract expression from first argument (usually self or the expression)
            expression = args[0] if args else None

            # Check if we have a cached result
            cached_result = _global_cache.get(
                operation, expression, *args[1:], **kwargs
            )
            if cached_result is not None:
                return cached_result

            # Compute result
            result = func(*args, **kwargs)

            # Cache the result
            _global_cache.set(
                operation, expression, result, priority, *args[1:], **kwargs
            )

            return result

        return wrapper

    return decorator


# Specialized decorators for common operations
def cached_simplification(func: Callable[..., Expr]) -> Callable[..., Expr]:
    """Decorator for caching simplification operations."""
    return cached_operation(CacheOperation.SIMPLIFICATION, CachePriority.HIGH)(func)


def cached_differentiation(func: Callable[..., Expr]) -> Callable[..., Expr]:
    """Decorator for caching differentiation operations."""
    return cached_operation(CacheOperation.DIFFERENTIATION, CachePriority.HIGH)(func)


def cached_solving(func: Callable[..., list]) -> Callable[..., list]:
    """Decorator for caching equation solving."""
    return cached_operation(CacheOperation.SOLVING, CachePriority.MEDIUM)(func)


def cached_evaluation(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for caching function evaluation."""
    return cached_operation(CacheOperation.EVALUATION, CachePriority.LOW)(func)


# Advanced caching functions with smart invalidation
def smart_cached_simplify(expr: Expr, force: bool = False) -> Expr:
    """
    Smart simplification with caching and parameter awareness.

    Args:
        expr: Expression to simplify
        force: Force re-computation ignoring cache
    """
    if force:
        return simplify(expr)

    # Check cache first
    cached = _global_cache.get(CacheOperation.SIMPLIFICATION, expr)
    if cached is not None:
        return cached

    # Compute and cache result
    result = simplify(expr)
    _global_cache.set(CacheOperation.SIMPLIFICATION, expr, result, CachePriority.HIGH)

    return result


def smart_cached_diff(
    expr: Expr, variable: Symbol, order: int = 1, force: bool = False
) -> Expr:
    """
    Smart differentiation with caching.

    Args:
        expr: Expression to differentiate
        variable: Variable to differentiate with respect to
        order: Order of differentiation
        force: Force re-computation ignoring cache
    """
    if force:
        return diff(expr, variable, order)

    # Check cache first
    cached = _global_cache.get(CacheOperation.DIFFERENTIATION, expr, variable, order)
    if cached is not None:
        return cached

    # Compute and cache result
    result = diff(expr, variable, order)
    _global_cache.set(
        CacheOperation.DIFFERENTIATION,
        expr,
        result,
        CachePriority.HIGH,
        variable,
        order,
    )

    return result


def smart_cached_solve(equation: Expr, variable: Symbol, force: bool = False) -> list:
    """
    Smart equation solving with caching.

    Args:
        equation: Equation to solve
        variable: Variable to solve for
        force: Force re-computation ignoring cache
    """
    if force:
        return solve(equation, variable)

    # Check cache first
    cached = _global_cache.get(CacheOperation.SOLVING, equation, variable)
    if cached is not None:
        return cached

    # Compute and cache result
    result = solve(equation, variable)
    _global_cache.set(
        CacheOperation.SOLVING, equation, result, CachePriority.MEDIUM, variable
    )

    return result


# Cache management functions
def get_cache_stats() -> Dict[str, Any]:
    """Get comprehensive cache statistics."""
    return _global_cache.get_stats()


def clear_cache():
    """Clear all cached entries."""
    _global_cache.clear()


def get_cache_report() -> str:
    """Generate a human-readable cache report."""
    stats = get_cache_stats()

    report = [
        "=== Schul-Analysis Cache Report ===",
        f"Overall Hit Rate: {stats['overall']['hit_rate']:.2%}",
        f"Total Requests: {stats['overall']['total_requests']}",
        f"Cache Entries: {stats['overall']['entries_count']}",
        f"Memory Usage: {stats['overall']['total_size_mb']:.2f} MB / {stats['overall']['max_size_mb']:.2f} MB",
        f"Evictions: {stats['overall']['evictions']}",
        "",
        "Operation Statistics:",
    ]

    for op_name, op_stats in stats["by_operation"].items():
        if op_stats["total"] > 0:
            report.append(
                f"  {op_name}: {op_stats['hit_rate']:.2%} ({op_stats['hits']}/{op_stats['total']})"
            )

    # Add top entries
    top_entries = _global_cache.get_top_entries(5)
    if top_entries:
        report.append("", "Top Cache Entries:")
        for entry in top_entries:
            report.append(f"  {entry['operation']}: {entry['access_count']} accesses")

    return "\n".join(report)


# Legacy compatibility
def cache_hit():
    """Legacy function for cache hit tracking."""
    config.cache_hit()


def cache_miss():
    """Legacy function for cache miss tracking."""
    config.cache_miss()


# Export cache instance for advanced usage
cache_instance = _global_cache
