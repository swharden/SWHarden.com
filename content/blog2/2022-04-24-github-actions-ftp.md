---
title: FTP Deploy with GitHub Actions
description: Deploy content over FTP using GitHub Actions and no dependencies
date: 2022-04-24 16:45:00
tags: ["GitHub"]
---



**This article describes how I use GitHub Actions to deploy content using FTP without any third-party dependencies.** Code executed in continuous deployment pipelines may have access to secrets (like FTP credentials and SSH keys). Supply-chain attacks are becoming more frequent, including self-sabotage by open-source authors. Without 2FA, the code of well-intentioned maintainers is one stolen password away from becoming malicious. For these reasons I find it imperative to eliminate third-party Actions from my CI/CD pipelines wherever possible.

> ⚠️ **WARNING: Third-party Actions in the GitHub Actions Marketplace may be compromised to run malicious code and leak secrets.** There are [dozens of public actions](https://github.com/marketplace?category=&query=ftp+sort%3Apopularity-desc&type=actions) claiming to facilitate FTP deployment. I advise avoiding third-party actions in your CI/CD pipeline whenever possible.

This article assumes you have at least some familiarity with GitHub Actions, but if you're never used them before I recommend taking 5 minutes to work through the [Quickstart for GitHub Actions](https://docs.github.com/en/actions/quickstart).

## FTP Deployment Workflow
**This workflow demonstrates how to use LFTP inside a GitHub Action to transfer files/folders with FTP without requiring a third-party dependency.** Users can copy/paste this workflow and edit it as needed according to the [LFTP manual](https://lftp.yar.ru/lftp-man.html).

```yaml
name: 🚀 FTP Deploy
on: [push, workflow_dispatch]
jobs:
  ftp-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: 🛒 Checkout
        uses: actions/checkout@v2
      - name: 📦 Get LFTP
        run: sudo apt install lftp
      - name: 🛠️ Configure LFTP
        run: mkdir ~/.lftp && echo "set ssl:verify-certificate false;" >> ~/.lftp/rc
      - name: 🔑 Load Secrets
        run: echo "machine ${{ secrets.FTP_HOSTNAME }} login ${{ secrets.FTP_USERNAME }} password ${{ secrets.FTP_PASSWORD }}" > ~/.netrc
      - name: 📄 Upload File
        run: lftp -e "put -O /destination/ ./README.md" ${{ secrets.FTP_HOSTNAME }}
      - name: 📁 Upload Folder
        run: lftp -e "mirror --parallel=100 -R ./ffmpeg/ /ffmpeg/" ${{ secrets.FTP_HOSTNAME }}
```

This workflow uses [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) to store secret values:

* `FTP_HOSTNAME` - a string like `ftp.example.com`
* `FTP_USERNAME` - a string like `login@example.com`
* `FTP_PASSWORD` - a string like `superSecret123`

<img src="https://swharden.com/static/2022/04/24/github-actions-ftp.jpg" class="d-block border shadow my-5 mx-auto" />

## How to Verify the Host Certificate

Extra steps can be taken to record the host's public certificate, store it as a [GitHub Encrypted Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets), load it into the GitHub Action runner, and configure LFTP to compare against at run time.

* 1: Acquire your host's _entire_ certificate chain. The `-showcerts` argument was critically important for me.

```bash
openssl s_client -connect example.com:21 -starttls ftp -showcerts
```

* 2: Copy the _entire_ output, [convert it to a Base64 string](https://emn178.github.io/online-tools/base64_encode.html), and store it as a [GitHub Encrypted Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named `FTP_CERTS_BASE64`

* 3: Update your GitHub Action to save the certificate file and configure LFTP to use it:

```yaml
      - name: 🛠️ Configure LFTP
        run: |
          mkdir ~/.lftp
          echo "set ssl:ca-file ~/.lftp/certs.crt;set ssl:check-hostname no;" >> ~/.lftp/rc
          echo "${{ secrets.FTP_CERTS_BASE64 }}" | base64 --decode > ~/.lftp/certs.crt
```

## Notes

**To avoid storing passwords to disk** you can pass them in with each `lftp` command using the `-u` argument. See the [LFTP Documentation](https://lftp.yar.ru/lftp-man.html) for details.

**Although potentially insecure, some GitHub Marketplace Actions offer compelling features:** One of the most popular is [SamKirkland's FTP Deploy Action](https://github.com/SamKirkland/FTP-Deploy-Action) which has advanced features like the use of server-stored JSON files to store file hashes to detect and selectively re-upload changed files. I encourage you to check them out, even though I try to avoid passing my secrets through third-party actions wherever possible.

**Favor SSH and `rsync` over FTP and `lftp` where possible** because `rsync` is faster, more secure, and designed to prevent needless transfer of unchanged files. I recently wrote about [how to safely deploy over SSH using rsync with GitHub Actions](https://swharden.com/blog/2022-03-20-github-actions-hugo/).

## Resources
* [LFTP project on GitHub](https://github.com/lavv17/lftp)
* [LFTP Documentation](https://lftp.yar.ru/lftp-man.html)
* [GitHub Actions: Build and deploy a Hugo site](https://swharden.com/blog/2022-03-20-github-actions-hugo/)
* [GitHub Actions: How to deploy over SSH using rsync](https://swharden.com/blog/2022-03-20-github-actions-hugo/)
* [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [GNU Manual: The .netrc file](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html)
* [SSL Checker: Certificate Decoder](https://www.sslchecker.com/certdecoder)