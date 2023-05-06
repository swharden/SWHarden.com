---
Title: Determine GitHub Action Runner IP
Description: A simple way to get the IP of the server running your GitHub Actions
Date: 2022-03-12 19:51:00
tags: ["github"]
---

# Determine the IP of your GitHub Action Runner

**I recently had the need to determine the IP address of the server running my GitHib Action.** Knowing this may be useful to match-up individual workflow runs with specific entries in log files, or temporarily whitelisting the action runner's IP during testing.

I found that a [cURL](https://en.wikipedia.org/wiki/CURL) request to [ipify.org](https://www.ipify.org/) can achieve this simply:

```yaml
on:
  workflow_dispatch:
  push:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: 🛒 Checkout
        uses: actions/checkout@v2
      - name: 🔎 Check IP
        run: curl https://api.ipify.org
```

<img src="ip.jpg" class="shadow rounded mx-auto d-block my-5">

There are published/shared Actions which do something similar (e.g., [haythem/public-ip](https://github.com/marketplace/actions/public-ip)) but whenever possible I avoid these because they are a potential vector for supply chain attacks (a compromised action could access secrets in environment variables).

## Resources
* The [GitHub meta endpoint](https://api.github.com/meta) shows all IP ranges used by GitHub Actions runners and may be useful for whitelisting purposes.