---
title: Test React Apps in Azure Pipelines
date: 2020-09-22 13:15:00
---

# Test React Apps in Azure Pipelines

Azure Pipelines makes it easy to run tests in the cloud, but I found that a new React projects made with [`create-react-app`](https://reactjs.org/docs/create-a-new-react-app.html) fail to properly test in the cloud using the simple `npm test` command. Attempting this would display `No tests found related to files changed since last commit` but hang forever.

<div class="text-center img-border">

[![](npm-test-azure-pipelines_thumb.jpg)](npm-test-azure-pipelines.jpg)

</div>

I solved this problem and got my React app to test properly in the cloud by adding `-- --watchAll=false` after `npm test`. This is my final `azure-pipelines.yml` file:

```yaml
trigger:
  - master

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: "10.x"
    displayName: "Install Node.js"

  - script: npm install
    displayName: "Install NPM"

  - script: npm run build
    displayName: "Build"

  - script: npm test -- --watchAll=false
    displayName: "Test"
```

A working React app that tests properly with Azure Pipelines is [GitHub.com/swharden/AliCalc](https://github.com/swharden/AliCalc)