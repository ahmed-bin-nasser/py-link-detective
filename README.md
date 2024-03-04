<div align="center">
<pre align="center">
<h2 align="center">
;; Python-Link-Detective ;;
</h2>
<h4 align="center">A simple implementation of a dead link detection tool using python httpx & asyncio library</h4>
</pre>
</div>

## Installation
```sh
pip install py-link-detective
```

## Usage
```sh
py-link-detective -h
```

```text

usage: py-link-detective [-h] [--version] [--num_async_requests] [--timeout] (-c | -j) url

A simple implementation of a dead link detection tool using python asyncio library

positional arguments:
  url                   The url of the website to be checked

options:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --num_async_requests , -n
                        number of concurrent request at a time, default is 10
  --timeout , -t        timeout for each request, default is 5 seconds
  -c                    use console for output
  -j                    use a json file(in the current path) for output

```

## Run Tests

```sh
pytest -v
```

## Demo

### For Console Output

```sh

py-link-detective -c https://stackoverflow.com -n 20

```

```text

################################# https://stackoverflow.com #################################

200 | https://stackoverflow.com/users/signup?ssrc=site_switcher&returnurl=https%3a%2f%2fstackoverflow.com%2f
200 | https://meta.stackoverflow.com
200 | https://stackoverflow.com
200 | https://stackoverflow.com/users/signup?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f
200 | https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f
200 | https://stackoverflow.com/users/login?ssrc=site_switcher&returnurl=https%3a%2f%2fstackoverflow.com%2f
200 | https://stackoverflow.com/questions
200 | https://stackoverflow.com/beta/discussions
200 | https://stackoverflow.com/tags
200 | https://stackoverflow.com/users/signup?ssrc=product_home
200 | https://stackoverflow.com/
200 | https://stackexchange.com/sites
200 | https://stackoverflow.com/help
200 | https://stackoverflow.com/jobs/companies?so_medium=stackoverflow&so_source=SiteNav
200 | https://stackoverflow.co/teams/
200 | https://stackoverflow.co/advertising/
200 | https://stackoverflow.blog
200 | https://stackoverflow.co/labs/

------------------------------------------------------------------

```

### For JSON Output

```sh

py-link-detective -j https://stackoverflow.com -n 20

```

```json

{
    "200": [
        "https://stackoverflow.com/help",
        "https://stackoverflow.com/users/login?ssrc=site_switcher&returnurl=https%3a%2f%2fstackoverflow.com%2f",
        "https://meta.stackoverflow.com",
        "https://stackoverflow.com/jobs/companies?so_medium=stackoverflow&so_source=SiteNav",
        "https://stackoverflow.com/tags",
        "https://stackoverflow.com/users/signup?ssrc=site_switcher&returnurl=https%3a%2f%2fstackoverflow.com%2f",
        "https://www.facebook.com/officialstackoverflow/"
    ],
    "302": [
        "https://stackoverflow.com/users",
        "https://stackoverflow.co/talent/",
        "https://stackoverflow.co/collectives/",
        "https://stackoverflow.com/legal"
    ],
    "400": [
        "https://twitter.com/stackoverflow"
    ],
    "301": [
        "https://linkedin.com/company/stack-overflow",
        "https://www.instagram.com/thestackoverflow"
    ],
    "-1": [
        "javascript:void(0)"
    ]
}

```


## Contributing

Following improvements can be made to current project.

1. Add structured logging
2. Write more tests
3. Add support for more output formats
4. Add url validation
