---
title: Embed Arbitrary Payloads into JPEGs without Special Tools
description: Using ordinary shell commands to embed and extract hidden binary data in JPEG images
Date: 2026-05-02 11:04:00
tags: ["graphics"]
---

**Arbitrary binary data can be hidden at the end of JPEG files which otherwise behave normally.** This article explores strategies for packing and unpacking payloads into JPEG images using standard console commands and no external tools or special steganography software. I find it amusing how easy it is to hide arbitrary data in JPEG images that otherwise appear normal!

<a href="https://swharden.com/static/2026/05/02/jpeg-payload-banner.png">
<img src="https://swharden.com/static/2026/05/02/jpeg-payload-banner.png" class="my-0">
</a>

**Images with unexpected trailing binary data will be quickly flagged** by antivirus systems, or the trailing data will be stripped when the image is re-encoded, but the easy detection of binary payloads in images is somewhat offset by the simplicity and availability of this method, allowing JPEG images to be appended with arbitrary binary payloads on virtually any system.

## Theory of Operation
* JPEG files terminate with an EOI (End Of Image) marker `FF D9`
* Data after the EOI marker is typically ignored when displaying the image
* Embed an arbitrary payload to a JPEG by appending it to the end of the file
* Extract the binary payloads by capturing data after the first `FF D9`
* Embedding and extracting payloads can be done with standard console commands
* Payloads may be any file type (exe, mp3, etc.) and are not restricted to other images

## Commands

**These commands can be run on any system and do not require any special tools.** See the [**JPEG binary payload GitHub repository**](https://github.com/swharden/JPEG-binary-payload) for downloadable script files, original images, and images pre-loaded with hidden data.

### Bash

```sh
# Embed a payload
cat image.jpg payload.bin > image_with_payload.jpg
```

```sh
# Extract the payload
offset=$(grep -abo $'\xff\xd9' image_with_payload.jpg | head -n1 | cut -d: -f1)
tail -c +$((offset + 3)) image_with_payload.jpg > payload.bin
```

### Powershell

```ps1
# Embed a payload
[IO.File]::WriteAllBytes(
    "image_with_payload.jpg",
    [IO.File]::ReadAllBytes("image.jpg") +
    [IO.File]::ReadAllBytes("payload.bin")
)
```

```ps1
# Extract the payload
$data = [IO.File]::ReadAllBytes("image_with_payload.jpg")
for ($i = 0; $i -lt $data.Length - 1; $i++) {
    if ($data[$i] -eq 0xFF -and $data[$i + 1] -eq 0xD9) {
        $start = $i + 2
        break
    }
}
[IO.File]::WriteAllBytes("payload.bin", $data[$start..($data.Length - 1)])
```

### Command Prompt

```cmd
:: Embed a payload
copy /b image.jpg + payload.bin image_with_payload.jpg
```

> Extracting payloads with the command prompt is difficult because it does not have native byte array handling, so extraction requires writing a script that calls external system tools like `certutil`. Although it is possible to extract payloads using only command prompt and system tools, it is recommended to use the PowerShell extraction script on Windows platforms instead.

## Example Images with Payload Data

Image + Payload | Payload
---|---
![](https://swharden.com/static/2026/05/02/embedded/image/image_with_payload.jpg)|Image: ![](https://swharden.com/static/2026/05/02/embedded/image/extracted_payload.jpg)
![](https://swharden.com/static/2026/05/02/embedded/text/image_with_payload.jpg)|Plain Text: [zen_of_python.txt](https://swharden.com/static/2026/05/02/embedded/text/extracted_payload.txt)
![](https://swharden.com/static/2026/05/02/embedded/mp3/image_with_payload.jpg)|Audio: [payload.mp3](https://swharden.com/static/2026/05/02/embedded/mp3/extracted_payload.mp3)

## Limitations
* The payload will get dropped if the image is re-encoded
* The payload increases the file size, so large payloads become obvious
* JPEGs with embedded thumbnails may have multiple `FF D9` instances
* Some software legitimately stores metadata after the JPEG EOI marker

## Resources

* [**JPEG binary payload (GitHub)**](https://github.com/swharden/JPEG-binary-payload) - Contains source images, images packed with binary data, and runnable script files for each of the platforms discussed here.

* [**JPEG file format (Wikipedia)**](https://en.wikipedia.org/wiki/JPEG)

* [**JPEG File Interchange Format (FileFormat.info)**](https://www.fileformat.info/format/jpeg/egff.htm) - Describes JFIF/JPEG markers including the `FF D8` SOI and `FF D9` EOI markers.