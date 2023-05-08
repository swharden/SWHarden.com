---
Title: Managing Secrets in .NET Console Apps
Description: How to use dotnet user-secrets to store and retrieve secrets and set environment variables in .NET applications.
Date: 2021-10-09 13:15:00
tags: ["csharp"]
---

# Managing Secrets in .NET Console Apps

**Sometimes your code needs to work with secrets that you don't want to risk accidentally leaking on the internet.** There are many strategies for solving this problem, and here I share my preferred approach. I see a lot of articles about how to manage user secrets in ASP.NET and other web applications, but not many focusing on console or desktop applications.

## User Secrets in C# Applications

* The `dotnet user-secrets` command manages secrets

* Secrets are stored as plain-text key/value pairs in JSON format in `%AppData%\Microsoft\UserSecrets`

* This isn't totally secure, but may be an improvement over `.env` and `.json` files stored inside your project folder which can accidentally get committed to source control if your `.gitignore` file isn't meticulously managed


### 1. Create a New .NET App

```text
dotnet new console
```

### 2. Set the Secrets ID

* right-click the project and `manage user secrets`

OR

* `dotnet user-secrets init`

OR

* Edit the `.csproj` file to add a unique `UserSecretsId`
* Generate a unique ID with [uuidtools.com](https://www.uuidtools.com/)

```xml
<PropertyGroup>
  <UserSecretsId>ee35bcf4-291d-11ec-9dc7-7f3593499a27</UserSecretsId>
</PropertyGroup>
```

### 3. Add Secrets Locally

```text
dotnet user-secrets set username me@example.com
dotnet user-secrets set password mySecretPass123
```

### 4. Install the UserSecrets Package

```text
dotnet add package Microsoft.Extensions.Configuration.UserSecrets
```

> **💡 CAREFUL:** If you accidentally install [`Microsoft.Extensions.Configuration`](https://www.nuget.org/packages/Microsoft.Extensions.Configuration) instead of [`Microsoft.Extensions.Configuration.UserSecrets`](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.UserSecrets) you won't have access to `AddUserSecrets()`

### 5. Access Secrets in Code

```cs
using Microsoft.Extensions.Configuration;
```

```cs
var config = new ConfigurationBuilder().AddUserSecrets<Program>().Build();
string username = config["username"];
string password = config["password"];
```

_NOTE: If a key does not exist its value will be `null`_

## Environment Variables

**Cloud platforms (GitHub Actions, Azure, etc.) often use environment variables to manage secrets.** Using local user secrets to populate environment variables is a useful way to locally develop applications that will run in the cloud.

This example shows how to populate environment variables from user secrets:

```cs
using Microsoft.Extensions.Configuration;

class Program
{
    static void Main()
    {
        SetEnvironmentVariablesFromUserSecrets();
        string username = Environment.GetEnvironmentVariable("username");
        string password = Environment.GetEnvironmentVariable("password");
    }

    static void SetEnvironmentVariablesFromUserSecrets()
    {
        var config = new ConfigurationBuilder().AddUserSecrets<Program>().Build();
        foreach (var child in config.GetChildren())
        {
            Environment.SetEnvironmentVariable(child.Key, child.Value);
        }
    }
}
```

## GitHub Actions

**GitHub Actions makes it easy to load repository secrets into environment variables.** See [GitHub / Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) for more information about how to add secrets to your repository.

This example snippet of a GitHub action loads two GitHub repository secrets (`USERNAME` and `PASSWORD`) as environment variables (`username` and `password`) that can be read by my unit tests using `Environment.GetEnvironmentVariable()` as shown above.

```yaml
    steps:
      ...
      - name: 🧪 Run Tests
        env:
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
        run: dotnet test ./src
```

## Conclusions

**Using these strategies I am able to write code that seamlessly accesses secrets locally on my dev machine and from environment variables when running in the cloud.** Since this strategy does not store secrets inside my project folder, the chance of accidentally committing a `.env` or other secrets file to source control approaches zero.

## Resources

* NuGet [`Microsoft.Extensions.Configuration.UserSecrets`](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.UserSecrets) 

* [Using .env in .NET](https://dusted.codes/dotenv-in-dotnet) by [Dustin Moris Gorski](https://github.com/dustinmoris)

* Microsoft Documentation for [`Environment.GetEnvironmentVariable()`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.getenvironmentvariable)

* [GitHub / Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)