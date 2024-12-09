<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Resume - Scott W Harden</title>
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
            display: inline-block;
            width: 1%;
            height: 10px;
            border: 1px solid transparent;
            border-top: 3px solid black;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 0.5rem;
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