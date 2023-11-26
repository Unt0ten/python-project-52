### Hexlet tests and linter status:
[![Actions Status](https://github.com/Unt0ten/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Unt0ten/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/88408d52d4652e35e89c/maintainability)](https://codeclimate.com/github/Unt0ten/python-project-52/maintainability)

### Description
[Task Manager](https://task-manager-6iez.onrender.com) is system that allows you to set tasks, assign performers and "
"change their statuses. To work with the system you need registration and "
"authentication.

### Requirement
* Python
* Poetry
* Postgres / Sqlite3

### Installation
**Setting up enviroment**
```bash
git clone git@github.com:Unt0ten/python-project-52.git
cd task-manager
make build
```
Configure .env in the root folder
```
cp .env_example .env
```

**Dev**
```bash
make dev
```

**Prod**
```bash
make start
```