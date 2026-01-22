#!/usr/bin/env python3
"""
CLI Testing Tool for AI Film Studio API
Usage: python tests/cli_test_tool.py [command] [options]
"""
import argparse
import asyncio
import json
import sys
import time
from typing import Dict, Any, Optional
import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


class AIFilmStudioCLI:
    """CLI tool for testing AI Film Studio API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.headers["Content-Type"] = "application/json"
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)
    
    def health_check(self):
        """Check API health status"""
        console.print("[cyan]Checking API health...[/cyan]")
        response = self._make_request("GET", "/health")
        
        if response.status_code == 200:
            console.print("[green]✓ API is healthy![/green]")
            console.print_json(response.text)
        else:
            console.print(f"[red]✗ API health check failed: {response.status_code}[/red]")
    
    def generate_video(self, script: str, duration: int = 30, voice: str = "professional-female-1"):
        """Generate a video from script"""
        console.print(Panel(f"[cyan]Generating video...[/cyan]\n\nScript: {script}\nDuration: {duration}s\nVoice: {voice}"))
        
        payload = {
            "script": script,
            "duration": duration,
            "voice": voice,
            "style": "cinematic"
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Submitting job...", total=None)
            response = self._make_request("POST", "/v1/generate", json=payload)
        
        if response.status_code in [200, 202]:
            data = response.json()
            job_id = data.get("job_id")
            
            console.print(f"[green]✓ Job submitted successfully![/green]")
            console.print(f"Job ID: [yellow]{job_id}[/yellow]")
            
            if "--wait" in sys.argv:
                self.wait_for_job(job_id)
            else:
                console.print("\n[dim]Use --wait flag to wait for completion or check status with:[/dim]")
                console.print(f"[dim]python tests/cli_test_tool.py status {job_id}[/dim]")
        else:
            console.print(f"[red]✗ Failed to generate video: {response.status_code}[/red]")
            console.print(response.text)
    
    def get_status(self, job_id: str):
        """Get video generation status"""
        console.print(f"[cyan]Checking status for job: {job_id}[/cyan]")
        response = self._make_request("GET", f"/v1/videos/{job_id}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            
            # Color-code status
            status_colors = {
                "pending": "yellow",
                "processing": "cyan",
                "completed": "green",
                "failed": "red"
            }
            color = status_colors.get(status, "white")
            
            console.print(f"Status: [{color}]{status}[/{color}]")
            
            if status == "completed":
                video_url = data.get("video_url")
                console.print(f"[green]✓ Video ready![/green]")
                console.print(f"Download URL: [link]{video_url}[/link]")
            
            console.print_json(response.text)
        else:
            console.print(f"[red]✗ Failed to get status: {response.status_code}[/red]")
    
    def wait_for_job(self, job_id: str, timeout: int = 600):
        """Wait for job to complete"""
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing video...", total=None)
            
            while time.time() - start_time < timeout:
                response = self._make_request("GET", f"/v1/videos/{job_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    progress.update(task, description=f"Status: {status}")
                    
                    if status == "completed":
                        console.print("[green]✓ Video generation completed![/green]")
                        console.print(f"Download URL: {data.get('video_url')}")
                        return
                    elif status == "failed":
                        console.print("[red]✗ Video generation failed![/red]")
                        console.print(data.get("error", "Unknown error"))
                        return
                
                time.sleep(5)
            
            console.print("[yellow]⚠ Timeout waiting for job completion[/yellow]")
    
    def list_voices(self):
        """List available voices"""
        console.print("[cyan]Fetching available voices...[/cyan]")
        response = self._make_request("GET", "/v1/voices")
        
        if response.status_code == 200:
            data = response.json()
            voices = data.get("voices", [])
            
            table = Table(title="Available Voices")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="white")
            table.add_column("Language", style="yellow")
            table.add_column("Gender", style="magenta")
            
            for voice in voices:
                table.add_row(
                    voice.get("id"),
                    voice.get("name"),
                    voice.get("language"),
                    voice.get("gender", "N/A")
                )
            
            console.print(table)
        else:
            console.print(f"[red]✗ Failed to fetch voices: {response.status_code}[/red]")
    
    def run_integration_tests(self):
        """Run basic integration tests"""
        console.print(Panel("[cyan]Running Integration Tests[/cyan]"))
        
        tests = [
            ("Health Check", self._test_health),
            ("List Voices", self._test_list_voices),
            ("Generate Video (Quick)", self._test_generate_video),
        ]
        
        results = []
        for test_name, test_func in tests:
            console.print(f"\n[yellow]Running: {test_name}[/yellow]")
            try:
                result = test_func()
                results.append((test_name, result, None))
                console.print(f"[green]✓ {test_name} passed[/green]")
            except Exception as e:
                results.append((test_name, False, str(e)))
                console.print(f"[red]✗ {test_name} failed: {e}[/red]")
        
        # Summary
        console.print("\n" + "="*50)
        passed = sum(1 for _, result, _ in results if result)
        total = len(results)
        console.print(f"[cyan]Test Results: {passed}/{total} passed[/cyan]")
    
    def _test_health(self) -> bool:
        response = self._make_request("GET", "/health")
        return response.status_code == 200
    
    def _test_list_voices(self) -> bool:
        response = self._make_request("GET", "/v1/voices")
        return response.status_code == 200
    
    def _test_generate_video(self) -> bool:
        payload = {
            "script": "CLI test script",
            "duration": 10
        }
        response = self._make_request("POST", "/v1/generate", json=payload)
        return response.status_code in [200, 202]


def main():
    parser = argparse.ArgumentParser(description="AI Film Studio CLI Testing Tool")
    parser.add_argument("--base-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--api-key", help="API key for authentication")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Health command
    subparsers.add_parser("health", help="Check API health")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a video")
    generate_parser.add_argument("script", help="Script text")
    generate_parser.add_argument("--duration", type=int, default=30, help="Video duration in seconds")
    generate_parser.add_argument("--voice", default="professional-female-1", help="Voice ID")
    generate_parser.add_argument("--wait", action="store_true", help="Wait for completion")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get job status")
    status_parser.add_argument("job_id", help="Job ID")
    
    # Voices command
    subparsers.add_parser("voices", help="List available voices")
    
    # Test command
    subparsers.add_parser("test", help="Run integration tests")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = AIFilmStudioCLI(base_url=args.base_url, api_key=args.api_key)
    
    if args.command == "health":
        cli.health_check()
    elif args.command == "generate":
        cli.generate_video(args.script, args.duration, args.voice)
    elif args.command == "status":
        cli.get_status(args.job_id)
    elif args.command == "voices":
        cli.list_voices()
    elif args.command == "test":
        cli.run_integration_tests()


if __name__ == "__main__":
    main()
