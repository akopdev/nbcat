<h1 align="center">nbcat: Jupyter notebooks viewer</h1>

[nbcat](https://github.com/akopdev/nbcat) let you preview Jupyter notebooks directly in your terminal. Think of it as `cat`, but for `.ipynb` files.

<p align="center">
  <a href="docs/screenshot.png" target="blank"><img src="docs/screenshot.png" width="400" /></a>
  <a href="docs/screenshot2.png" target="blank"><img src="docs/screenshot2.png" width="400" /></a>
</p>

## Features

- Very fast and lightweight with minimal dependencies.
- Preview remote notebooks without downloading them.
- Enable paginated view mode with keyboard navigation (similar to `less`).
- Supports image rendering in high resolution
- Supports for all Jupyter notebook versions, including old legacy formats.

## Motivation

The idea of previewing notebooks in a terminal is not new - there have been many previous attempts to achieve it.  
However, most are either slow and overengineered with a ton of half-working features, or they're outdated and incompatible with modern Python.

I was looking for a simple tool that let me quickly render Jupyter notebooks without switching context from my terminal window or installing a ton of dependencies.  

Please note, that `nbcat` doesn't aim to replace JupyterLab. If you need a full-featured terminal experience, I recommend checking out [euporie](https://euporie.readthedocs.io/) instead.


## Installation

```bash
# Install from PyPI (recommended)
$ pip install nbcat

# Install via Homebrew
$ brew tab akopdev/formulas/nbcat
$ brew install nbcat
```

## Quickstart

```bash
$ nbcat notebook.ipynb
```

You can pass URLs as well.

```bash
$ nbcat https://raw.githubusercontent.com/akopdev/nbcat/refs/heads/main/tests/assets/test4.ipynb
```
In most cases system `less` will render images in low resolution. Consider using an internal pager instead:

```bash
$ nbcat notebook.ipynb --page
```
## Integrations

`nbcat` is designed to integrate seamlessly with other tools. Here are a few examples of how easily it can be done.

### FZF (Fuzzy finder)

List all `.ipynb` files and use `nbcat` to preview them:

```bash
find . -type f -name "*.ipynb" | fzf --preview 'nbcat {}'
```

### Ranger
To enable previews in Ranger, add the `ipynb` extension to the `handle_extension` function in `~/.config/ranger/scope.sh`:

```bash 
...

handle_extension() {
    case "${FILE_EXTENSION_LOWER}" in
        ipynb)
            nbcat "${FILE_PATH}" && exit 5
            exit 1;;
        ...
```

## Testing & Development

Run the tests:

```bash
make test
```

Check code quality:

```bash
make format lint
```

## Contributing

Contributions are welcome! Please open an issue or [pull request](https://github.com/akopdev/nbcat/pulls).

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

## Useful Links

- 📘 Documentation: _coming soon_
- 🐛 Issues: [GitHub Issues](https://github.com/akopdev/nbcat/issues)
- 🚀 Releases: [GitHub Releases](https://github.com/akopdev/nbcat/releases)

---

Made with ❤️ by [Akop Kesheshyan](https://github.com/akopdev)
