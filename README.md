# idox - Indirect Data Exploiter

**A CLI or embedded tool for easily downloading IDOR'd files from a burp request or raw url.**

<img src="https://github.com/Skelmis/idox/blob/master/images/idox.jpeg" alt="drawing" width="250"/>

---

This tool will enumerate the provided URL and download all responses under the correct file extension for later analysis.

Example statistics:
<img src="https://github.com/Skelmis/idox/blob/master/images/usage.png" alt="drawing" width="750"/>

*File extension incorrect or missing? Open an issue with an example response and expected behaviour*

### Example usage

#### Burp files

Imagine you have a website that looks like the following:

```text
https://domain.com/images/5/download
https://domain.com/images/6/download
```

Then you could use the following burp request:

`request.txt`
```text
GET /images/{INJECT}/download HTTP/1.1
Host: domain.com


```

To IDOR all images with the id's from `0` to `100` like so

```shell
python -m idox file --request-file-path request.txt 100
```

This would create an `output` directory which stores all the responses from your target site by response content type.

#### Raw URLS

Given it requires no auth, you can also enumerate all items with the following simpler syntax:

```shell
python -m idox url "https://domain.com/images/{INJECT}/download"  100
```

This would create an `output` directory which stores all the responses from your target site by response content type.



For further usage, see `python -m idox --help` or the `data` directory.

---

### Support

Want realtime help? Join the discord [here](https://discord.gg/BqPNSH2jPg).

---

### License
This project is licensed under the MIT license

---

### Funding

Want a feature added quickly? Want me to help build your software using Idox?

Sponsor me [here](https://github.com/sponsors/Skelmis)

