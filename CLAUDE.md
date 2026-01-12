# CLAUDE.md - AI Assistant Guide

This document provides comprehensive guidance for AI assistants (like Claude) working on this repository. It covers codebase structure, development workflows, conventions, and best practices.

## Repository Overview

**Repository:** borakrglu/try
**Purpose:** [To be determined based on project development]
**Primary Language:** [To be determined]
**Current Status:** Fresh repository, initial setup phase

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Development Workflow](#development-workflow)
3. [Git Conventions](#git-conventions)
4. [Code Quality Standards](#code-quality-standards)
5. [AI Assistant Guidelines](#ai-assistant-guidelines)
6. [Testing Strategy](#testing-strategy)
7. [Documentation Requirements](#documentation-requirements)
8. [Common Tasks & Commands](#common-tasks--commands)

---

## Project Structure

### Expected Directory Layout

```
/
├── src/                  # Source code
├── tests/                # Test files
├── docs/                 # Documentation
├── config/               # Configuration files
├── scripts/              # Build and utility scripts
├── .github/              # GitHub workflows and templates
├── CLAUDE.md             # This file - AI assistant guide
├── README.md             # User-facing documentation
└── [build configs]       # package.json, requirements.txt, etc.
```

### Key Directories

- **src/**: Contains all application source code
- **tests/**: Contains test files (unit, integration, e2e)
- **docs/**: Additional documentation, architecture diagrams, ADRs
- **config/**: Environment configs, constants, feature flags

---

## Development Workflow

### Branch Strategy

1. **Feature Branches**: All development happens on feature branches
   - Branch naming: `claude/claude-md-{session-id}`
   - Create from: main/master branch
   - Merge via: Pull Request with review

2. **Branch Operations**:
   ```bash
   # Create new feature branch
   git checkout -b claude/feature-name-{session-id}

   # Keep branch updated
   git fetch origin
   git merge origin/main

   # Push changes
   git push -u origin claude/feature-name-{session-id}
   ```

### Commit Guidelines

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(api): add user authentication endpoint

Implement JWT-based authentication with refresh tokens.
Includes middleware for protected routes.

Closes #123
```

```bash
fix(ui): resolve button alignment issue

Buttons were misaligned on mobile viewports due to
incorrect flexbox properties.
```

### Pull Request Process

1. **Create PR** with clear title and description
2. **Include**:
   - Summary of changes
   - Related issue numbers
   - Test plan
   - Screenshots (if UI changes)
3. **Checklist**:
   - [ ] Tests pass
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No security vulnerabilities introduced
   - [ ] Performance impact considered

---

## Git Conventions

### Push Operations

- **Always use**: `git push -u origin <branch-name>`
- **Branch naming**: Must start with `claude/` and end with session ID
- **Retry logic**: If network errors, retry up to 4 times (2s, 4s, 8s, 16s backoff)

### Fetch/Pull Operations

- **Prefer specific branches**: `git fetch origin <branch-name>`
- **For pulls**: `git pull origin <branch-name>`
- **Apply retry logic** for network failures

### Git Hooks

Follow repository hook configurations:
- Pre-commit: Linting, formatting checks
- Pre-push: Test suite execution
- Commit-msg: Commit message validation

---

## Code Quality Standards

### General Principles

1. **Readability First**: Code should be self-documenting
2. **KISS Principle**: Keep it simple, avoid over-engineering
3. **DRY Principle**: Don't repeat yourself (but avoid premature abstraction)
4. **YAGNI**: You aren't gonna need it - build what's needed now

### Security Best Practices

Always guard against:
- **Injection Attacks**: SQL injection, command injection, XSS
- **Authentication Issues**: Weak passwords, insecure sessions
- **Sensitive Data Exposure**: Secrets in code, logs, or version control
- **Security Misconfiguration**: Default credentials, unnecessary services
- **Broken Access Control**: Unauthorized access to resources

**Never commit:**
- API keys, tokens, passwords
- `.env` files with real credentials
- Private certificates or keys
- Personal data or PII

### Code Style

- **Consistent formatting**: Use project's formatter (Prettier, Black, etc.)
- **Meaningful names**: Variables, functions, and classes should be self-explanatory
- **Comments**: Only where logic isn't obvious - prefer clear code over comments
- **File size**: Keep files focused and reasonably sized (< 500 lines)

### Error Handling

- **Validate at boundaries**: User input, external APIs, file I/O
- **Trust internal code**: Don't add defensive checks for impossible states
- **Fail fast**: Detect errors early, provide clear messages
- **Handle gracefully**: User-facing errors should be informative

---

## AI Assistant Guidelines

### Before Making Changes

1. **Always read files first** before suggesting modifications
2. **Understand context** by exploring related files
3. **Check existing patterns** to maintain consistency
4. **Plan complex changes** using TodoWrite tool

### When Editing Code

1. **Minimal changes**: Only modify what's necessary
2. **Preserve style**: Match existing code formatting and conventions
3. **No scope creep**: Don't add unrequested features or refactors
4. **Test changes**: Verify functionality after modifications
5. **Document public APIs**: Add/update docs for public functions/classes

### What NOT to Do

- ❌ Don't add features beyond the request
- ❌ Don't refactor unrelated code
- ❌ Don't add comments to unchanged code
- ❌ Don't create abstractions for one-time operations
- ❌ Don't add error handling for impossible scenarios
- ❌ Don't use backwards-compatibility hacks for unused code
- ❌ Don't create documentation files unless explicitly requested

### Tool Usage Preferences

1. **File Operations**:
   - Read files: `Read` tool (not `cat`)
   - Search content: `Grep` tool (not `grep` command)
   - Find files: `Glob` tool (not `find` command)
   - Edit files: `Edit` tool (not `sed`/`awk`)
   - Write files: `Write` tool (not `echo >` or heredoc)

2. **Task Management**:
   - Use `TodoWrite` for complex multi-step tasks
   - Update status as work progresses
   - Mark completed immediately after finishing

3. **Exploration**:
   - Use `Task` tool with `subagent_type=Explore` for broad questions
   - Use direct tools (`Read`, `Grep`, `Glob`) for specific queries

### Parallel Operations

When tasks are independent:
- Make multiple tool calls in a single message
- Example: Reading multiple files, running parallel searches
- Don't use placeholders - wait for dependencies before calling dependent tools

---

## Testing Strategy

### Test Organization

```
tests/
├── unit/           # Unit tests for individual functions/classes
├── integration/    # Integration tests for component interactions
├── e2e/            # End-to-end tests for user workflows
└── fixtures/       # Test data and mocks
```

### Testing Guidelines

1. **Test Coverage**: Aim for meaningful coverage, not just high percentages
2. **Test Naming**: Descriptive names that explain what's being tested
3. **Arrange-Act-Assert**: Follow AAA pattern for clarity
4. **Test Independence**: Tests should not depend on each other
5. **Fast Tests**: Unit tests should be quick; reserve slow tests for integration

### Running Tests

```bash
# Run all tests
[test-command]

# Run specific test file
[test-command] [file-path]

# Run with coverage
[test-command] --coverage
```

---

## Documentation Requirements

### Code Documentation

- **Public APIs**: Document all public functions, classes, and modules
- **Complex Logic**: Explain the "why" behind non-obvious implementations
- **TODOs**: Format as `TODO: description` with context

### Project Documentation

Update these as the project evolves:
- **README.md**: Getting started, installation, basic usage
- **ARCHITECTURE.md**: High-level system design (if applicable)
- **API.md**: API endpoints and contracts (if applicable)
- **CHANGELOG.md**: Version history and notable changes

### Documentation Style

- Clear and concise
- Include code examples where helpful
- Keep documentation close to the code it describes
- Update docs when changing behavior

---

## Common Tasks & Commands

### Project Setup

```bash
# Clone repository
git clone [repo-url]
cd try

# Install dependencies
[package-manager] install

# Set up environment
cp .env.example .env
# Edit .env with your values
```

### Development

```bash
# Start development server
[dev-command]

# Run linter
[lint-command]

# Run formatter
[format-command]

# Run tests
[test-command]

# Build for production
[build-command]
```

### Git Workflows

```bash
# Create feature branch
git checkout -b claude/feature-name-[session-id]

# Stage changes
git add [files]

# Commit with message
git commit -m "feat: description of changes"

# Push to remote
git push -u origin claude/feature-name-[session-id]

# Create pull request
gh pr create --title "Title" --body "Description"
```

---

## Project-Specific Notes

### Technology Stack

To be determined as the project develops. Expected technologies might include:
- **Frontend**: React, Vue, Angular, or similar
- **Backend**: Node.js, Python, Go, or similar
- **Database**: PostgreSQL, MongoDB, or similar
- **Testing**: Jest, Pytest, or similar

### Environment Variables

Store sensitive configuration in `.env` files (never commit these):
```env
# Example structure
API_KEY=your_key_here
DATABASE_URL=your_db_url_here
NODE_ENV=development
```

### Configuration Management

- Development config: `.env.development`
- Production config: Set via environment/secrets management
- Shared config: Can be committed if no sensitive data

---

## Best Practices Checklist

Before pushing code, verify:

- [ ] All tests pass
- [ ] Code follows project style guidelines
- [ ] No console.log/print statements left in production code
- [ ] No commented-out code blocks
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated where needed
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts
- [ ] Branch is up to date with main/master
- [ ] Pull request is ready for review

---

## Troubleshooting

### Common Issues

**Issue**: Git push fails with 403 error
**Solution**: Ensure branch name starts with `claude/` and ends with correct session ID

**Issue**: Tests failing locally
**Solution**: Ensure dependencies are installed and environment is configured

**Issue**: Merge conflicts
**Solution**: Fetch latest changes, resolve conflicts manually, then commit

### Getting Help

- Check README.md for project-specific guidance
- Review existing code for patterns and conventions
- Consult with team members on architectural decisions
- Document solutions to novel problems

---

## Maintenance

### Regular Updates

This document should be updated when:
- Project structure changes significantly
- New conventions are adopted
- Technology stack changes
- New team members need onboarding
- Common patterns emerge that should be documented

### Version History

- **2026-01-12**: Initial version created for fresh repository

---

## Contact & Resources

**Repository Owner**: borakrglu
**Repository**: try
**Issues**: [Track issues in GitHub Issues]
**Discussions**: [Use GitHub Discussions for questions]

---

*This document is maintained by AI assistants and human developers working on this project. Keep it updated as the project evolves.*
