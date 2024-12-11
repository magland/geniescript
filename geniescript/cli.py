#!/usr/bin/env python3
"""Command line interface for the geniescript package providing functionality to run genie scripts."""

from typing import List
import click
from .run import run as run_impl


@click.group()
def cli():
    """Main command group for geniescript CLI."""


@click.command(
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True}
)
@click.argument("source_file_name")
@click.option(
    "--no-execute", is_flag=True, help="Generate the Python file without executing it"
)
@click.option("--script-args", default="", help="Arguments to pass to the script")
@click.option(
    "--force-regenerate",
    is_flag=True,
    help="Force regeneration of the Python file regardless of changes",
)
@click.pass_context
def run(
    ctx,
    source_file_name: str,
    no_execute: bool,
    script_args: str,
    force_regenerate: bool,
):
    """Run a genie script.
    """
    if ctx.args:
        raise click.UsageError(f"Unknown arguments: {' '.join(ctx.args)}")

    # Convert script_args string to list if not empty
    args_list: List[str] = script_args.split() if script_args else []
    return run_impl(
        source_file_name,
        execute=not no_execute,
        script_args=args_list,
        force_regenerate=force_regenerate,
    )


cli.add_command(run)

if __name__ == "__main__":
    cli()
