# Universal Code Voyager

**AI assistant memory that works with any CLI and IDE.**

Code Voyager adds persistent memory and skill management to AI coding assistants.
Originally designed for Claude Code, it now works with **any editor** and **any AI provider**.

## What's New: Universal Adapters

Code Voyager now features:

- 🔌 **IDE Adapters**: Works with any editor (Claude Code, VS Code, Vim, or just CLI)
- 🤖 **AI Provider Adapters**: Choose your AI (Claude, GPT-4, local models via Ollama)
- 📁 **Flexible Storage**: Configure where your memory lives
- 🔧 **Full Backward Compatibility**: Existing Claude Code users unaffected

## Quick Start

### 1. Choose Your Setup

#### Generic CLI (Works Anywhere)

```bash
# Install
uv tool install "git+https://github.com/zenbase-ai/code-voyager.git"

# Initialize in your project
cd my-project
mkdir -p .voyager
cat > .voyager/config.toml << EOF
[voyager]
ide_adapter = "generic_cli"
ai_provider = "claude"
EOF

# Use
voyager session start
voyager brain update
voyager session end
```

#### Claude Code (Original)

```bash
# Install CLI
uv tool install "git+https://github.com/zenbase-ai/code-voyager.git"

# Install skills
mkdir -p .claude/skills && \
  curl -sL https://github.com/zenbase-ai/code-voyager/archive/main.tar.gz | \
  tar -xz -C .claude/skills --strip-components=3 code-voyager-main/.claude/skills/

# Add hooks to .claude/settings.json
# (See original README for hook configuration)
```

### 2. Choose Your AI Provider

#### Claude (Recommended)

```toml
[voyager]
ai_provider = "claude"

[ai.claude]
model = "claude-3-5-sonnet-20241022"
```

Set API key: `export ANTHROPIC_API_KEY="sk-ant-..."`

#### OpenAI

```bash
pip install openai
```

```toml
[voyager]
ai_provider = "openai"

[ai.openai]
model = "gpt-4"
```

Set API key: `export OPENAI_API_KEY="sk-..."`

#### Ollama (Local, Private)

```bash
# Install Ollama from https://ollama.ai/
ollama pull codellama:34b
ollama serve
```

```toml
[voyager]
ai_provider = "ollama"

[ai.ollama]
model = "codellama:34b"
base_url = "http://localhost:11434"
```

No API key needed!

## Core Features

All these work regardless of your IDE or AI provider:

### 1. Session Brain

Persistent memory of what you're working on.

```bash
# Start session (loads brain state)
voyager session start

# Your AI now remembers context from previous sessions

# Update brain with progress
voyager brain update

# End session (saves state)
voyager session end
```

**Storage:** `.voyager/brain.json` and `.voyager/brain.md`

### 2. Curriculum Planner

Generates prioritized task sequences.

```bash
# Generate a curriculum
voyager curriculum plan

# Output saved to .voyager/curriculum.md
```

### 3. Skill Factory

Proposes and scaffolds reusable skills.

```bash
# Propose new skills
voyager factory propose

# List proposals
voyager factory list

# Scaffold a skill
voyager factory scaffold --name deploy-workflow
```

**Storage:** `.voyager/skills/generated/`

### 4. Skill Retrieval

Semantic search over your skill library.

```bash
# Index skills
voyager skill index

# Search for skills
voyager skill find "deployment process"
```

### 5. Skill Refinement

Feedback-driven skill improvement.

```bash
# View skill insights
voyager feedback insights

# Shows which skills need improvement based on usage
```

## IDE Adapters

### Claude Code (`claude_code`)

**Full automation** with hooks.

- ✅ Automatic session management
- ✅ Context injection
- ✅ Brain updates on session end
- ✅ Tool use feedback

**Setup:** See original README for hook configuration.

### Generic CLI (`generic_cli`)

**Manual control** for any environment.

- ✅ Works with any editor
- ✅ No IDE integration needed
- ✅ Scriptable
- ✅ Full control

**Usage:**
```bash
voyager session start
# Work on code...
voyager brain update
voyager session end
```

### Coming Soon

- **VS Code**: Extension with sidebar and automatic integration
- **JetBrains**: Plugin for IntelliJ, PyCharm, WebStorm, etc.
- **Vim/Neovim**: Lua-based plugin with commands
- **Generic LSP**: Works with any LSP-compatible editor

## AI Providers

| Provider | Best For | Cost | Privacy | Setup |
|----------|----------|------|---------|-------|
| **Claude** | Code quality | $$$ | Low | Easy |
| **OpenAI** | Flexibility | $-$$$ | Low | Easy |
| **Ollama** | Privacy, offline | Free* | High | Medium |

*Requires local hardware

## Configuration

Configuration lives in `.voyager/config.toml` or `voyager.toml`:

```toml
[voyager]
state_dir = ".voyager"
skills_dir = ".voyager/skills"
ide_adapter = "generic_cli"
ai_provider = "claude"

[ai.claude]
model = "claude-3-5-sonnet-20241022"
timeout_seconds = 60

[ide.generic_cli]
auto_save_brain = true
verbose = true
```

See [docs/configuration.md](docs/configuration.md) for full reference.

## Examples

### Generic CLI with Claude

```bash
cp examples/generic-cli/voyager.toml .voyager/config.toml
export ANTHROPIC_API_KEY="sk-ant-..."
voyager session start
```

### Generic CLI with OpenAI

```bash
pip install openai
cp examples/with-openai/voyager.toml .voyager/config.toml
export OPENAI_API_KEY="sk-..."
voyager session start
```

### Local with Ollama

```bash
ollama pull codellama:34b
ollama serve
cp examples/with-ollama/voyager.toml .voyager/config.toml
voyager session start
```

## Hybrid Approach

Use different providers for different tasks:

```bash
# Quick brain updates (free, private)
voyager brain update --provider ollama

# Complex skill generation (best quality)
voyager factory propose --provider claude

# Simple questions (cheap)
voyager ask "What's next?" --provider openai --model gpt-3.5-turbo
```

## Benefits

### Universal Compatibility

- ✅ Works with **any editor**: Vim, Emacs, VS Code, Sublime, etc.
- ✅ Works with **any AI**: Claude, GPT-4, local models
- ✅ Works **anywhere**: Terminal, SSH, Docker containers

### Portability

- ✅ Your memory travels with your code (`.voyager/` directory)
- ✅ Team members can share skills and curriculum
- ✅ Switch IDEs without losing context

### Flexibility

- ✅ Choose your AI provider based on needs (quality, cost, privacy)
- ✅ Manual or automatic session management
- ✅ Scriptable and CLI-first design

### Privacy

- ✅ Use local models (Ollama) for complete privacy
- ✅ No data leaves your machine
- ✅ Run offline if needed

## Documentation

- [Architecture](ARCHITECTURE.md) - System design and adapter architecture
- [IDE Adapters](docs/ide-adapters.md) - Detailed IDE adapter guide
- [AI Providers](docs/ai-providers.md) - AI provider comparison and setup
- [Configuration](docs/configuration.md) - Complete configuration reference

## Migration from Claude Code

Existing Claude Code users can continue using the original setup.
The adapter system is fully backward compatible:

```toml
[voyager]
state_dir = ".claude/voyager"
skills_dir = ".claude/skills"
ide_adapter = "claude_code"
ai_provider = "claude"
```

Or migrate to the universal setup:

```bash
# Move state to new location
mv .claude/voyager .voyager
mv .claude/skills .voyager/skills

# Update config
cat > .voyager/config.toml << EOF
[voyager]
ide_adapter = "generic_cli"
ai_provider = "claude"
EOF
```

## Creating Custom Adapters

### IDE Adapter

```python
from voyager.adapters.base.ide_adapter import IDEAdapter, IDEEvent, IDEContext

class MyIDEAdapter(IDEAdapter):
    def get_project_dir(self) -> Path:
        return Path.cwd()
    
    def on_session_start(self, event: IDEEvent) -> IDEContext | None:
        # Load and return brain context
        pass
    
    # Implement other methods...
```

### AI Provider

```python
from voyager.adapters.base.ai_provider import AIProvider, AIRequest, AIResponse

class MyAIProvider(AIProvider):
    def call(self, request: AIRequest) -> AIResponse:
        # Make API call and return response
        pass
    
    def is_available(self) -> bool:
        # Check if provider is available
        pass
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## Contributing

We welcome contributions for:

- New IDE adapters (VS Code, JetBrains, Vim, etc.)
- New AI providers (Gemini, Cohere, etc.)
- Documentation improvements
- Bug fixes and features

## Roadmap

### High Priority

- [x] Generic CLI adapter
- [x] OpenAI provider
- [x] Ollama provider
- [ ] VS Code extension
- [ ] Generic LSP server

### Medium Priority

- [ ] JetBrains plugin
- [ ] Vim/Neovim plugin
- [ ] Gemini provider
- [ ] Anthropic API provider

### Low Priority

- [ ] Emacs package
- [ ] Sublime Text plugin
- [ ] Cohere provider

## License

MIT

## Acknowledgments

Inspired by the [Voyager paper](https://arxiv.org/abs/2305.16291) from NVIDIA and Caltech.

Original Claude Code integration by the Zenbase team.

Universal adapter system designed to make AI memory accessible to everyone,
regardless of their IDE or AI provider choice.
