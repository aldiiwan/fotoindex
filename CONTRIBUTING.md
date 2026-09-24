# Contributing

Start with a reproducible problem from an actual photography workflow. Open an issue before substantial changes. Small documentation improvements and bug reports are welcome.

1. Describe the expected and observed behavior, OS, Python/Pillow versions, and command.
2. Use synthetic or licensed test images, remove identifying metadata, and never post client photos without permission.
3. Fork the repository, make a focused branch, add a regression test for behavioral fixes, and run `python -m unittest discover -s tests -v`.
4. Submit a pull request explaining the user problem, implementation, tests, and limitations. Disclose substantial AI assistance and verify the generated work yourself.

Do not add network access, destructive image operations, or unrelated features without discussing scope. Be respectful; criticize ideas, not people. Maintainers may close abusive or unrelated threads.
