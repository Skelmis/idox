# idox - Indirect Data Exploiter

**A CLI or embedded tool for easily downloading IDOR'd files from a burp request.**

<img src="https://github.com/Skelmis/idox/blob/master/images/idox.jpeg" alt="drawing" width="250"/>

---

### Example usage

Imagine you have a website that looks like the following:

```text
https://domain.com/images/5/download
https://domain.com/images/6/download
```

Then you could use the following burp request:

`request.txt`
```text
GET /images/$INJECT$/download HTTP/1.1
Host: domain.com


```

To IDOR all images with the id's from `0` to `100` like so

```shell
python -m idox --request-file-path request.txt 100
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

Want a feature added quickly? Want me to help build your software using Alaric?

Sponsor me [here](https://github.com/sponsors/Skelmis)

