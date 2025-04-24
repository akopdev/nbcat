# 📦 nbcat

`nbcat` lets you preview Jupyter notebooks directly in your terminal. Think of it as `cat`, but for `.ipynb` files.

## 🚀 Features

- Fast and lightweight with minimal external dependencies
- Preview remote notebooks without downloading them
- Supports for all Jupyter notebook versions - including legacy formats 

## 📦 Installation

From the command line using pip:

```bash
pip install nbcat
```

## 🛠️ Quickstart

```bash
$ nbcat notebook.ipynb
```

You can pass URLs as well.

```bash
$ nbcat https://raw.githubusercontent.com/akopdev/nbcat/refs/heads/main/tests/assets/test4.ipynb
```

Example use case with `fzf` command that lists all `.ipynb` files and uses `nbcat` for previewing them:

```bash
find . -type f -name "*.ipynb" | fzf --preview 'nbcat {}'
```

## 🧪 Testing & Development

Run the tests:

```bash
make test
```

Check code quality:

```bash
make format lint
```

## 🙌 Contributing

Contributions are welcome! Please open an issue or [pull request](https://github.com/akopdev/nbcat/pulls).

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

## 🔗 Useful Links

- 📘 Documentation: _coming soon_
- 🐛 Issues: [GitHub Issues](https://github.com/akopdev/nbcat/issues)
- 🚀 Releases: [GitHub Releases](https://github.com/akopdev/nbcat/releases)

---

Made with ❤️ by [Akop Kesheshyan](https://github.com/akopdev)
