"""
CLI commands contributed by splent_feature_comments.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:comments`` group.

Usage::

    splent feature:comments hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_comments!")


cli_commands = [hello]
