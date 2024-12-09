# SWHarden.com

[![Blog](https://github.com/swharden/SWHarden.com/actions/workflows/cicd-blog.yaml/badge.svg)](https://github.com/swharden/SWHarden.com/actions/workflows/cicd-blog.yaml)

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

### Tips

#### Batch Resize Images

The `input` and `output` folders must exist

```sh
magick mogrify -resize 1200 -quality 80 -path output input/*.jpg
```

```sh
magick mogrify -resize 1200 -format webP -quality 80 -path output input/*.jpg
```
