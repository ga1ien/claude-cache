"""
Animations and visual feedback for Claude Cache
Makes the terminal feel alive and thinking
"""

import asyncio
import time
from typing import List, Optional, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
import random

console = Console()


class ThinkingSpinner:
    """Contextual spinner that shows what's being analyzed"""

    THINKING_STATES = [
        "🔍 Scanning patterns...",
        "🧠 Analyzing complexity...",
        "⚡ Detecting anti-patterns...",
        "🔗 Correlating solutions...",
        "📊 Building knowledge graph...",
        "✨ Finding insights...",
        "🎯 Matching patterns...",
        "💡 Learning from failures...",
    ]

    def __init__(self):
        self.current_state = 0

    def get_next_state(self) -> str:
        """Get next thinking state message"""
        state = self.THINKING_STATES[self.current_state % len(self.THINKING_STATES)]
        self.current_state += 1
        return state

    async def run(self, duration: float = 3.0):
        """Run thinking animation for specified duration"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            task = progress.add_task(self.get_next_state(), total=None)

            start_time = time.time()
            while time.time() - start_time < duration:
                await asyncio.sleep(0.5)
                progress.update(task, description=self.get_next_state())


class PatternDiscoveryFeed:
    """Live streaming feed of pattern discoveries"""

    def __init__(self):
        self.patterns = []
        self.max_visible = 5

    def add_pattern(self, pattern_type: str, description: str, project: str):
        """Add a new pattern to the feed"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Choose emoji based on type
        if pattern_type == "gold":
            emoji = "🥇"
            color = "green"
        elif pattern_type == "silver":
            emoji = "🥈"
            color = "yellow"
        elif pattern_type == "bronze":
            emoji = "🥉"
            color = "dim"
        elif pattern_type == "anti":
            emoji = "⚠️"
            color = "red"
        elif pattern_type == "journey":
            emoji = "🛤️"
            color = "blue"
        else:
            emoji = "📝"
            color = "white"

        self.patterns.append({
            "timestamp": timestamp,
            "emoji": emoji,
            "color": color,
            "description": description[:60] + "..." if len(description) > 60 else description,
            "project": project,
            "age": 0
        })

        # Keep only recent patterns
        if len(self.patterns) > self.max_visible:
            self.patterns = self.patterns[-self.max_visible:]

    def render(self) -> Panel:
        """Render the pattern feed as a panel"""
        lines = []

        for pattern in self.patterns:
            # Create fading effect based on age
            opacity = max(0.3, 1.0 - (pattern["age"] * 0.2))

            if opacity > 0.7:
                style = f"bold {pattern['color']}"
            elif opacity > 0.4:
                style = pattern["color"]
            else:
                style = "dim"

            line = Text()
            line.append(f"[{pattern['timestamp']}] ", style="dim")
            line.append(f"{pattern['emoji']} ", style=style)
            line.append(pattern["description"], style=style)
            line.append(f" [{pattern['project']}]", style="dim cyan")

            lines.append(line)

            # Age patterns for fading effect
            pattern["age"] += 1

        # Add empty lines if needed
        while len(lines) < self.max_visible:
            lines.insert(0, Text(""))

        content = "\n".join(str(line) for line in lines)

        return Panel(
            content,
            title="🔄 Pattern Discovery Feed",
            border_style="cyan",
            height=self.max_visible + 2
        )

    async def animate(self, patterns_to_add: List[Dict], delay: float = 0.5):
        """Animate pattern discoveries with delays"""
        with Live(self.render(), refresh_per_second=4, console=console) as live:
            for pattern in patterns_to_add:
                self.add_pattern(
                    pattern["type"],
                    pattern["description"],
                    pattern["project"]
                )
                live.update(self.render())
                await asyncio.sleep(delay)

            # Keep showing for a bit then fade
            for _ in range(5):
                await asyncio.sleep(0.5)
                live.update(self.render())


class NotificationToast:
    """Pop-up style notifications that appear and fade"""

    @staticmethod
    async def show(message: str, type: str = "info", duration: float = 3.0):
        """Show a notification toast"""

        # Choose style based on type
        if type == "success":
            icon = "✅"
            border_style = "green"
        elif type == "warning":
            icon = "⚠️"
            border_style = "yellow"
        elif type == "error":
            icon = "❌"
            border_style = "red"
        elif type == "discovery":
            icon = "✨"
            border_style = "cyan"
        else:
            icon = "ℹ️"
            border_style = "blue"

        # Create notification panel
        notification = Panel(
            Align.center(f"{icon} {message}"),
            border_style=border_style,
            expand=False,
            padding=(0, 2)
        )

        # Show with fade effect
        with Live(notification, refresh_per_second=4, console=console, transient=True) as live:
            await asyncio.sleep(duration)


class SparklineDashboard:
    """Live dashboard with sparkline graphs"""

    def __init__(self):
        self.pattern_history = []
        self.quality_history = []
        self.max_history = 20

    def add_data_point(self, patterns_count: int, quality: str):
        """Add a new data point"""
        self.pattern_history.append(patterns_count)
        if len(self.pattern_history) > self.max_history:
            self.pattern_history.pop(0)

        quality_map = {"gold": 3, "silver": 2, "bronze": 1}
        self.quality_history.append(quality_map.get(quality, 0))
        if len(self.quality_history) > self.max_history:
            self.quality_history.pop(0)

    def create_sparkline(self, data: List[int]) -> str:
        """Create a sparkline from data"""
        if not data:
            return ""

        spark_chars = "▁▂▃▄▅▆▇█"
        max_val = max(data) if max(data) > 0 else 1
        min_val = min(data)

        sparkline = ""
        for val in data:
            normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
            index = int(normalized * (len(spark_chars) - 1))
            sparkline += spark_chars[index]

        return sparkline

    def render(self) -> Panel:
        """Render the dashboard"""
        # Create sparklines
        pattern_spark = self.create_sparkline(self.pattern_history)
        quality_spark = ""

        for q in self.quality_history:
            if q == 3:
                quality_spark += "🥇"
            elif q == 2:
                quality_spark += "🥈"
            elif q == 1:
                quality_spark += "🥉"
            else:
                quality_spark += "·"

        # Calculate current rate
        if len(self.pattern_history) > 1:
            current_rate = self.pattern_history[-1]
            trend = "📈" if self.pattern_history[-1] > self.pattern_history[-2] else "📉"
        else:
            current_rate = 0
            trend = "📊"

        content = f"""
[bold cyan]📊 Live Learning Dashboard[/bold cyan]

Patterns/hour: {pattern_spark} ({current_rate}) {trend}
Quality trend: {quality_spark}
Active scanning: [green]●●●●●[/green]
        """.strip()

        return Panel(
            content,
            border_style="blue",
            expand=False
        )


class ProgressAnimation:
    """Smooth progress animations for batch operations"""

    @staticmethod
    async def scan_animation(total_items: int, operation: str = "Scanning"):
        """Animated progress bar for scanning operations"""

        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TextColumn("[cyan]{task.fields[status]}"),
            console=console,
            transient=True
        ) as progress:

            task = progress.add_task(
                f"{operation}...",
                total=total_items,
                status="Initializing..."
            )

            statuses = [
                "Finding patterns...",
                "Analyzing complexity...",
                "Detecting anti-patterns...",
                "Building connections...",
                "Learning insights..."
            ]

            for i in range(total_items):
                # Update with random status
                status = random.choice(statuses)
                progress.update(task, advance=1, status=status)

                # Simulate work with small delay
                await asyncio.sleep(random.uniform(0.05, 0.15))

            progress.update(task, status="✅ Complete!")
            await asyncio.sleep(0.5)


class LivePatternMonitor:
    """Live monitoring display for pattern discovery"""

    def __init__(self):
        self.feed = PatternDiscoveryFeed()
        self.dashboard = SparklineDashboard()

    async def monitor(self, duration: float = 30.0):
        """Run live monitoring display"""

        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(self.dashboard.render(), size=8),
            Layout(self.feed.render(), size=8)
        )

        with Live(layout, refresh_per_second=2, console=console) as live:
            start_time = time.time()

            while time.time() - start_time < duration:
                # Simulate pattern discoveries
                if random.random() > 0.7:
                    pattern_types = ["gold", "silver", "bronze", "anti", "journey"]
                    descriptions = [
                        "Fixed authentication flow",
                        "Optimized database query",
                        "Resolved CORS issue",
                        "Improved error handling",
                        "Refactored component structure"
                    ]
                    projects = ["lollipop-supa", "cache", "mcp-test"]

                    self.feed.add_pattern(
                        random.choice(pattern_types),
                        random.choice(descriptions),
                        random.choice(projects)
                    )

                    self.dashboard.add_data_point(
                        random.randint(5, 15),
                        random.choice(["gold", "silver", "bronze"])
                    )

                # Update display
                layout.split_column(
                    Layout(self.dashboard.render(), size=8),
                    Layout(self.feed.render(), size=8)
                )
                live.update(layout)

                await asyncio.sleep(0.5)


# Convenience functions for CLI integration
async def show_thinking(message: str = None, duration: float = 2.0):
    """Show thinking animation"""
    spinner = ThinkingSpinner()
    if message:
        console.print(f"[cyan]{message}[/cyan]")
    await spinner.run(duration)


async def show_discovery_feed(patterns: List[Dict]):
    """Show pattern discovery feed"""
    feed = PatternDiscoveryFeed()
    await feed.animate(patterns)


async def show_toast(message: str, type: str = "info"):
    """Show notification toast"""
    await NotificationToast.show(message, type)


async def show_progress(total: int, operation: str = "Processing"):
    """Show progress animation"""
    await ProgressAnimation.scan_animation(total, operation)


async def start_live_monitor(duration: float = 30.0):
    """Start live monitoring display"""
    monitor = LivePatternMonitor()
    await monitor.monitor(duration)