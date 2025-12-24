"""Hook handler commands for Claude Code integration.

These commands are designed to be called by Claude Code hooks:
    voyager hook session-start   # SessionStart hook
    voyager hook session-end     # SessionEnd hook
    voyager hook pre-compact     # PreCompact hook
    voyager hook post-tool-use   # PostToolUse hook
"""

from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

import typer

from voyager.llm import is_internal_call
from voyager.scripts.brain.inject import inject_from_stdin
from voyager.scripts.brain.update import main as brain_update_main

app = typer.Typer(
    name="hook",
    help="Claude Code hook handlers",
    no_args_is_help=True,
)


@app.command("session-start")
def session_start() -> None:
    """Handle SessionStart hook - injects brain context.

    Reads hook input JSON from stdin and outputs hook response JSON to stdout.
    Injects the session brain context and repo snapshot into the session.
    """
    # Recursion guard
    if is_internal_call():
        typer.echo(json.dumps({"suppressOutput": True}))
        raise typer.Exit(0)

    try:
        output = inject_from_stdin()
        typer.echo(json.dumps(output))
    except Exception as e:
        print(f"session-start error: {e}", file=sys.stderr)
        fallback = {
            "hookSpecificOutput": {"additionalContext": ""},
            "suppressOutput": True,
        }
        typer.echo(json.dumps(fallback))


@app.command("session-end")
def session_end() -> None:
    """Handle SessionEnd hook - persists session memory.

    Reads hook input JSON from stdin and updates the brain state
    from the transcript when the session ends.
    """
    # Recursion guard
    if is_internal_call():
        typer.echo(json.dumps({}))
        raise typer.Exit(0)

    # Parse hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        hook_input = {}

    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")
    cwd = hook_input.get("cwd", str(Path.cwd()))

    # Resolve transcript path
    transcript = None
    if transcript_path:
        tp = Path(transcript_path)
        if not tp.is_absolute():
            tp = Path(cwd) / tp
        transcript = tp

    try:
        brain_update_main(
            transcript=transcript,
            session_id=session_id,
            snapshot_path=None,
            dry_run=False,
            skip_llm=False,
        )
    except typer.Exit:
        pass  # Normal exit from typer command
    except Exception as e:
        print(f"session-end error: {e}", file=sys.stderr)

    # Always return success to not block the hook
    typer.echo(json.dumps({}))


@app.command("pre-compact")
def pre_compact() -> None:
    """Handle PreCompact hook - persists session memory before compaction.

    Reads hook input JSON from stdin and updates the brain state
    from the transcript before context compaction occurs.
    """
    # Recursion guard
    if is_internal_call():
        typer.echo(json.dumps({}))
        raise typer.Exit(0)

    # Parse hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        hook_input = {}

    session_id = hook_input.get("session_id", "")
    transcript_path = hook_input.get("transcript_path", "")
    cwd = hook_input.get("cwd", str(Path.cwd()))

    # Resolve transcript path
    transcript = None
    if transcript_path:
        tp = Path(transcript_path)
        if not tp.is_absolute():
            tp = Path(cwd) / tp
        transcript = tp

    try:
        brain_update_main(
            transcript=transcript,
            session_id=session_id,
            snapshot_path=None,
            dry_run=False,
            skip_llm=False,
        )
    except typer.Exit:
        pass  # Normal exit from typer command
    except Exception as e:
        print(f"pre-compact error: {e}", file=sys.stderr)

    # Always return success to not block the hook
    typer.echo(json.dumps({}))


@app.command("post-tool-use")
def post_tool_use() -> None:
    """Handle PostToolUse hook - collects feedback for skill refinement.

    Reads hook input JSON from stdin. Currently a placeholder for
    feedback collection functionality.
    """
    # Recursion guard
    if is_internal_call():
        raise typer.Exit(0)

    # Parse hook input from stdin (consume it even if not used yet)
    with contextlib.suppress(json.JSONDecodeError):
        json.load(sys.stdin)

    # TODO: Implement feedback collection
    # - Extract tool name, inputs, outputs, success/failure
    # - Attribute to active skill(s)
    # - Store in feedback DB

    # Silent success
    typer.echo(json.dumps({}))
