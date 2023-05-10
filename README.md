# SWHarden.com

[![CICD](https://github.com/swharden/SWHarden.com/actions/workflows/cicd.yaml/badge.svg)](https://github.com/swharden/SWHarden.com/actions/workflows/cicd.yaml)

* This repository contains source code for https://swharden.com
* Questions, issues, and pull requests are welcome

### Local Development
* [Download Hugo](https://github.com/gohugoio/hugo/releases)
* Run `hugo.exe serve` in this repository folder
* Navigate to http://localhost:1313

### Deployment
* Run `hugo` in this repository folder to build the site
* Use `rsync` to transfer the `public` folder to the web server
* This process is run automatically by [`cicd.yaml`](.github/workflows/cicd.yaml) on every commit
