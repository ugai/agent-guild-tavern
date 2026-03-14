# Environment-Specific Notes

## PR Comments via File

Always write comment bodies to a temp file to avoid shell-escaping issues
with backticks and special Markdown characters:

```bash
gh pr comment <N> --body-file /tmp/qf_comment_<N>.md
```
