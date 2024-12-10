<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Resume - Scott W Harden</title>

    <meta name=theme-color content="#003366">

    <link rel=icon href="https://swharden.com/favicon.ico">

    <meta property="og:url" content="https://swharden.com/resume/">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Resume">
    <meta property="og:description" content="The Resume of Scott W Harden">
    <meta property="og:image" content="https://swharden.com/resume/images/og.png">

    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        a {
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .spinner {
            width: 10px;
            height: 10px;
            border: 2px solid transparent;
            border-top-color: black;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-left: 0.5rem;
        }

        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }

            100% {
                transform: rotate(360deg);
            }
        }
    </style>
</head>

<body>
    <div style="text-align: center; margin: 3rem; font-size: 1.2rem;">
        Forwarding to <a href="https://swharden.com/resume/resume.pdf?<?php echo rand(); ?>">resume.pdf</a>
        <div class="spinner"></div>
    </div>

    <script>
        window.setTimeout(function () {
            window.location.href = "resume.pdf?<?php echo rand(); ?>";
        }, 2000);
    </script>
</body>

</html>