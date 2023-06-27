---
title: Build and Deploy a Hugo Site with GitHub Actions
description: How I use GitHub Actions to build a static website with Hugo and deploy it using rsync without requiring any third-party dependencies
date: 2022-03-20 22:45:00
tags: ["github", "hugo"]
---


**This article describes how I _safely_ use GitHub Actions to build a static website with Hugo and deploy it using SSH without any third-party dependencies.** Code executed in continuous deployment pipelines may have access to secrets (like FTP credentials and SSH keys). Supply-chain attacks are becoming more frequent, including self-sabotage by open-source authors. Without 2FA, the code of well-intentioned maintainers is one stolen password away from becoming malicious. For these reasons I find it imperative to eliminate third-party Actions from my CI/CD pipelines wherever possible. 

> ⚠️ **WARNING: Third-party Actions in the GitHub Actions Marketplace may be compromised to run malicious code and leak secrets.** There are hundreds of public actions claiming to help with [Hugo](https://github.com/marketplace?type=actions&query=hugo), [SSH](https://github.com/marketplace?type=actions&query=SSH), and [Rsync](https://github.com/marketplace?type=actions&query=rsync) execution. I advise avoiding third-party actions in your CI/CD pipeline whenever possible.

This article assumes you have at least some familiarity with GitHub Actions, but if you're never used them before I recommend taking 5 minutes to work through the [Quickstart for GitHub Actions](https://docs.github.com/en/actions/quickstart).

## Example Workflow

This is my `cicd-website.yaml` workflow for building a Hugo website and deploying it with SSH. Most people can just copy/paste what they need from here, but the rest of the article will discuss the purpose and rationale for each of these sections in more detail.

```yaml
name: Website

on:
  workflow_dispatch:
  push:

jobs:
  build:
    name: Build and Deploy
    runs-on: ubuntu-latest
    steps:
      - name: 🛒 Checkout
        uses: actions/checkout@v2

      - name: ✨ Setup Hugo
        env:
          HUGO_VERSION: 0.92.2
        run: |
          mkdir ~/hugo
          cd ~/hugo
          curl -L "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz" --output hugo.tar.gz
          tar -xvzf hugo.tar.gz
          sudo mv hugo /usr/local/bin

      - name: 🛠️ Build
        run: hugo --source website --minify

      - name: 🔑 Install SSH Key
        run: |
          install -m 600 -D /dev/null ~/.ssh/id_rsa
          echo "${{ secrets.PRIVATE_SSH_KEY }}" > ~/.ssh/id_rsa
          echo "${{ secrets.KNOWN_HOSTS }}" > ~/.ssh/known_hosts

      - name: 🚀 Deploy
        run: rsync --archive --delete --stats -e 'ssh -p 18765' 'website/public/' ${{ secrets.REMOTE_DEST }}
```

## Triggers

The `on` section determines which triggers will initiate this workflow (building/deploying the site). The following will run the workflow after _every_ push to the GitHub repository. The `workflow_dispatch` allows the workflow to be triggered manually through the GitHub Actions web interface.

```yaml
on:
  workflow_dispatch:
  push:
```

I store my hugo site in the subfolder `./website`, so if I wanted to only rebuild/redeploy when the _website_ files are changed (and not other files in the repository) I could add a `paths` filter. If your repository has multiple branches you likely want a `branches` filter as well.

```yaml
on:
  workflow_dispatch:
  push:
    paths:
      - "website/**"
    branches:
      - main
```

## Download Hugo

This step defines the Hugo version I want as a temporary environment variable, downloads latest binary from the [Hugo Releases page on GitHub](https://github.com/gohugoio/hugo/releases), extracts it, and moves the executable file to the user's `bin` folder so it can be subsequently run from any folder.

```yaml
- name: ✨ Setup Hugo
  env:
    HUGO_VERSION: 0.92.2
  run: |
    mkdir ~/hugo
    cd ~/hugo
    curl -L "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz" --output hugo.tar.gz
    tar -xvzf hugo.tar.gz
    sudo mv hugo /usr/local/bin
```

## Build the Static Site with Hugo

I store my hugo site in the subfolder `./website`, so when I build the site I must define the source folder. Check-out the [Hugo build commands](https://gohugo.io/commands/hugo/) page for documentation about all the available options.

```yaml
- name: 🛠️ Build
  run: hugo --source website --minify
```

## SSH Secrets

This part is likely the most confusing for new users, so I'll keep it as minimal as possible. Before you start, I recommend you follow your hosting provider's guide for setting-up SSH. Once you can SSH from your own machine, it will be much easier to set it up in GitHub Actions. 

### Your Keys

* Start by creating a private/public key pair 
  * `ssh-keygen -t ed25519 -C "you@gmail.com"`
  * Code here assumes you use an empty passphrase
  * The public key is one long line that starts with `ssh-rsa`
  * The private key is a multi-line text block that starts and ends with `---`
* You give the PUBLIC key to your hosting provider to remember
* When you log in SSH you present your PRIVATE key
* GitHub Actions will need your PRIVATE key, so store it as a [GitHub Encrypted Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) (`PRIVATE_SSH_KEY`)

### The Host's Keys

To protect you from leaking your private key to a compromised host, you can retrieve your host's public key and check against it later to be sure it does not change. To get keys for your hosts run the following command:

```sh
ssh-keyscan example.com
```

My hosting provider uses a non-standard SSH port, so I must specify it with:

```sh
ssh-keyscan -p 12345 example.com
```

The host's public keys will be a short list of text. Store it as a [GitHub Encrypted Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) (`KNOWN_HOSTS`)

### Loading SSH Secrets in GitHub Actions

These commands will create text files in your `.ssh` folder containing your private key and the public keys of your host. Later `rsync` will complain if your private key is in a file with general read/write access, so the `install` command is used to create an empty file with user-only read/write access (chmod 600), then an `echo` command is used to populate that file with your private key information.

```yaml
- name: 🔑 Install SSH Key
  run: |
    install -m 600 -D /dev/null ~/.ssh/id_rsa
    echo "${{ secrets.PRIVATE_SSH_KEY }}" > ~/.ssh/id_rsa
    echo "${{ secrets.KNOWN_HOSTS }}" > ~/.ssh/known_hosts
```

## Deploy with Rsync

[Rsync](https://en.wikipedia.org/wiki/Rsync) is an application for synchronizing files over networks which is available on most Linux distributions. It only sending files with different modification times and file sizes, so it can be used to efficiently deploy changes to very large websites. 

Many people are okay with the defaults:

```yaml
- name: 🚀 Deploy
  run: rsync --archive public/ username@example.com:~/www/
```

I use additional arguments (see [rsync documentation](https://linux.die.net/man/1/rsync)) to:
* allow remote deletion of files
* use a non-standard SSH port (12345)
* store my remote destination as a [GitHub Encrypted Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) - not because it's private, but so I don't accidentally mess it up by incorrectly managing my workflow yaml (which could result in remote data deletion)
* display a small stats section after finishing (see screenshot)

```yaml
- name: 🚀 Deploy
  run: rsync --archive --delete --stats -e 'ssh -p 12345' website/public/ ${{ secrets.REMOTE_DEST }}
```

<img src="https://swharden.com/static/2022/03/20/github-actions-hugo-rsync-deploy.jpg" class="border shadow d-block mx-auto my-4">

## Conclusions

That's a lot to figure-out and set-up the first time, but once you have your SSH keys ready and some YAML you can copy/paste across multiple projects it's not that bad. 

I find `rsync` to be extremely fast compared to something like FTP run in GitHub Actions, and I'm very satisfied that I can achieve all these steps using Linux console commands and not depending on any other Actions.

## Resources

* This content was written after recently creating [
C# Data Visualization](https://swharden.com/csdv/) (a Hugo site built and deployed with GitHub Actions).
  * You can inspect the workflow files in [`.GitHub/workflows/`](https://github.com/swharden/Csharp-Data-Visualization/tree/main/.github/workflows) for full details.
  * My hosting provider is [SiteGround](https://www.siteground.com) (see their [SSH Tutorials](https://www.siteground.com/tutorials/ssh/)).
* The official [Hosting and Deployment](https://gohugo.io/hosting-and-deployment/) site has information for:
Google Cloud, AWS, Azure, Netlify, GitHub Pages, KeyCDN, Render CDN, Bitbucket, Netlify, Firebase, GitLab, and Rsync over SSH.
* A collection of my personal notes related to Hugo is in my [code-notes/Hugo](https://github.com/swharden/code-notes/tree/main/Hugo) repository.
* [Deploying a Hugo site with Github Actions](https://www.yellowduck.be/posts/deploy-hugo-site-with-github-actions/) by Jono Fotografie
* Hugo: [Deployment with Rsync](https://gohugo.io/hosting-and-deployment/deployment-with-rsync/)
* Rsync documentation and argument information: [rsync(1)](https://linux.die.net/man/1/rsync)
