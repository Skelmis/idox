# idox - Indirect Data Exploiter

**A CLI or embedded tool for easily downloading IDOR'd files from a burp request or raw url.**

<img src="https://github.com/Skelmis/idox/blob/master/images/idox.jpeg" alt="drawing" width="250"/>

---

This tool will enumerate the provided URL and download all responses under the correct file extension for later analysis.

Example statistics:

<img src="https://github.com/Skelmis/idox/blob/master/images/usage.png" alt="drawing" width="600"/>

*File extension incorrect or missing? Open an issue with an example response and expected behaviour*

### Example usage

#### Install

```shell
python -m pip install idox
```

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

#### Raw URLS

Given it requires no auth, you can also enumerate all items with the following simpler syntax:

```shell
python -m idox url "https://domain.com/images/{INJECT}/download" 100
```

#### Non-incrementing numeric ID enumeration

Imagine a site uses a predictable schema, but it's not `1`, `2`, `3`, etc. This package allows you to instead replace the numeric sequencer with a file of id's to use.

We have created a file [example_ids.txt](example_ids.txt) which is our case is a list of UUID's we leaked from somewhere else out of scope. In order to use this within the program, all you'd need to do is the following command:
```shell
python -m idox url "https://blurp.skelmis.co.nz/{INJECT}" --sequence-file example_ids.txt
```

### Example output

All of these would create an `output` directory which stores all the responses from your target site by response content type.

The following image contains an example output structure:

<img src="https://github.com/Skelmis/idox/blob/master/images/output.png" alt="drawing" width="500"/>


For further usage, see `python -m idox --help` or the `data` directory.

---

#### Other stuff

- Want realtime help? Join the discord [here](https://discord.gg/BqPNSH2jPg).
- This project is licensed under the MIT license
- Consider sponsoring me [here](https://github.com/sponsors/Skelmis)

