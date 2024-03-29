# Notty

[![Known Vulnerabilities](https://snyk.io/test/github/JakubBialoskorski/notty/badge.svg)](https://snyk.io/test/github/JakubBialoskorski/notty) [![Test and build a Dockerfile](https://github.com/JakubBialoskorski/notty/actions/workflows/testAndBuildDockerfile.yml/badge.svg)](https://github.com/JakubBialoskorski/notty/actions/workflows/testAndBuildDockerfile.yml)

Flask notes app with MySQL as a backend.
---

---

[**DEPRECATED**]

Due to the lack of time and invention of great products like [Obsidian](https://obsidian.md/), I will no longer provide maintenance or support for this product.

Feel free to fork it or improve as you see fit.

---

Based on [this repository](https://github.com/OmkarPathak/A-Simple-Note-Taking-Web-App) but with:
* MySQL / Aurora support (instead of local SQLite) with optional SSL/TLS
* `strftime` was cut out along with any time-related functions
* all `delete` actions explicit confirmations
* support for `utfmb4` (special characters like `śćźżó` / emojis etc.)
* [multiarch Dockerfile](.github/workflows/testAndBuildDockerfile.yml): amd64, arm64, arm/v6, arm/v7 - deployable to K3S/K8S
* bumped dependencies to match Snyk scans recommendations
---
#### How to develop:
* install [prerequisites](https://pypi.org/project/mysqlclient):
    * Linux: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`
    * MacOS:
        * `brew install mysql-client`
        * add `PATH="/usr/local/opt/mysql-client/bin:$PATH"` to .bashrc or .zshrc
        * `source .zshrc` / `source .bashrc` or reload the terminal before next step
* `pip install -r requirements.txt`
* create a database with `utf8mb4` charset and `utf8mb4_unicode_ci` collation (look at "Hacks" section)
* set your MySQL credentials in `utils/functions.py`
* run initial schema from `schema_mysql.sql`
* `python manage.py` or `gunicorn manage:app`
---
#### How to run locally in Docker:
* `docker build . -t notty-development`
* `docker run -d -p 80:80 -e SQLALCHEMY_CONFIG='mysql://USER:PASSWORD@DATABASE_IP/DATABASE_NAME' notty-development`

`SQLALCHEMY_CONFIG` can be put into Jenkins as build parameter to pass database credentials (though there are more secure methods).

---
#### How to run in k3s:
Adjust database parameters in `deployment.yaml` before proceeding.

Assuming you have [MetalLB](https://metallb.universe.tf) configured in your cluster:
* `kubectl apply -f service.yaml`
* `kubectl apply -f deployment.yaml`
---
#### Hacks:

MySQL cheat sheet:
* To create a database: `CREATE DATABASE notty CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
* To check charset and collation: `use notty;` and then `SELECT @@character_set_database, @@collation_database;`

Aurora with SSL/TLS:
* Enable custom parameter group with `require_secure_transport` set to `ON` and apply to your cluster
* Alter service user with `ALTER USER 'encrypted_user'@'%' REQUIRE SSL;`
* Add `?ssl=true` at the at the end of the database endpoint definition (point it to the writer instance)

Quick development with bash helpers:
* Fill credentials in `build_and_run.sh` and run it to build the Dockerfile with `notty` as container name
* `stop_and_destroy.sh` quickly does the obvious and you can proceed with another change