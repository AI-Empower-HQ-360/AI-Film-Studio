"""Command-line interface for AI Film Studio."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from .pipeline import Pipeline
from .config import Config


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """AI Film Studio - Transform scripts into videos using AI."""
    pass


@main.command()
@click.argument('script_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='output.mp4', help='Output video file path')
@click.option('--style', '-s', default='realistic', 
              help='Visual style (realistic, cartoon, anime, etc.)')
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Configuration file path')
def generate(script_path, output, style, config):
    """Generate a video from a script."""
    console.print(Panel.fit(
        "[bold blue]AI Film Studio[/bold blue]\n"
        "Generating video from script...",
        border_style="blue"
    ))
    
    # Load configuration
    cfg = Config(config) if config else Config()
    pipeline = Pipeline(cfg)
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing...", total=None)
            result = pipeline.generate(script_path, output, style)
            progress.update(task, completed=True)
        
        if result['status'] == 'not_implemented':
            console.print(f"[yellow]{result['message']}[/yellow]")
            console.print(f"\nInput: {result['script_path']}")
            console.print(f"Output: {result['output_path']}")
            console.print(f"Style: {result['style']}")
        else:
            console.print(f"[green]✓[/green] Video generated successfully: {output}")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@main.command()
@click.argument('script_path', type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='./frames', help='Output directory for frames')
@click.option('--style', '-s', default='realistic', help='Visual style')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
def frames(script_path, output_dir, style, config):
    """Generate only frames from a script (no video)."""
    console.print(Panel.fit(
        "[bold blue]AI Film Studio[/bold blue]\n"
        "Generating frames from script...",
        border_style="blue"
    ))
    
    cfg = Config(config) if config else Config()
    pipeline = Pipeline(cfg)
    
    try:
        result = pipeline.generate_frames(script_path, output_dir, style)
        
        if result['status'] == 'not_implemented':
            console.print(f"[yellow]{result['message']}[/yellow]")
        else:
            console.print(f"[green]✓[/green] Frames generated in: {output_dir}")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@main.command()
@click.argument('script_path', type=click.Path(exists=True))
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
def analyze(script_path, config):
    """Analyze a script without generating content."""
    console.print(Panel.fit(
        "[bold blue]AI Film Studio[/bold blue]\n"
        "Analyzing script...",
        border_style="blue"
    ))
    
    cfg = Config(config) if config else Config()
    pipeline = Pipeline(cfg)
    
    try:
        result = pipeline.analyze_script(script_path)
        
        if result['status'] == 'not_implemented':
            console.print(f"[yellow]{result['message']}[/yellow]")
        else:
            console.print("[green]✓[/green] Script analysis complete")
            # TODO: Display analysis results
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise click.Abort()


@main.command()
def interactive():
    """Launch interactive mode."""
    console.print(Panel.fit(
        "[bold blue]AI Film Studio[/bold blue]\n"
        "Interactive Mode",
        border_style="blue"
    ))
    
    console.print("[yellow]Interactive mode not yet implemented[/yellow]")
    console.print("\nThis feature will allow you to:")
    console.print("• Step through the generation process")
    console.print("• Review and modify at each stage")
    console.print("• Fine-tune parameters interactively")


@main.command()
def setup():
    """Setup AI Film Studio configuration."""
    console.print(Panel.fit(
        "[bold blue]AI Film Studio Setup[/bold blue]",
        border_style="blue"
    ))
    
    config = Config()
    
    console.print("\n[cyan]API Keys Configuration[/cyan]")
    console.print("Leave empty to skip or set later in .env file\n")
    
    # Prompt for API keys
    openai_key = click.prompt("OpenAI API Key", default="", show_default=False)
    stability_key = click.prompt("Stability AI API Key", default="", show_default=False)
    elevenlabs_key = click.prompt("ElevenLabs API Key", default="", show_default=False)
    
    if openai_key:
        config.set('api_keys.openai', openai_key)
    if stability_key:
        config.set('api_keys.stability', stability_key)
    if elevenlabs_key:
        config.set('api_keys.elevenlabs', elevenlabs_key)
    
    # Output directory
    output_dir = click.prompt("Output directory", default="./output")
    config.set('output_dir', output_dir)
    
    # Save configuration
    config.save()
    console.print(f"\n[green]✓[/green] Configuration saved to {config.config_path}")


if __name__ == '__main__':
    main()
