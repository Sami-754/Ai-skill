---
name: domain-checker
description: "Use when the user asks to check domain name availability for one or more domain names. Front-load keywords: domain, domains, available, availability, register, registration, whois, rdap, TLD, DNS, NXDOMAIN, selectra, check domain."
---

# Domain Availability Checker

Always run bash commands on the user's PC to check domain availability — it's faster and more reliable than any web API. If required tools (`whois`, `host`, `dig`) are missing, install them first:

```bash
# Debian/Ubuntu
sudo apt install -y whois dnsutils
# Arch
sudo pacman -S whois bind
# macOS
brew install whois bind
```

## Step 1 — Bulk DNS check (fastest)

```bash
for tld in com io net org dev app co ai me info xyz online shop; do
  echo -n "<name>.$tld: "
  host "<name>.$tld" 2>&1 | head -1
done
```

- `NXDOMAIN` → likely **available**
- Has A/AAAA record → **taken**
- `SERVFAIL` → ambiguous (try whois)

## Step 2 — Bulk whois check

```bash
for tld in com io net org dev app; do
  whois "<name>.$tld" 2>/dev/null | grep -iE "No match for|NOT FOUND|No Data Found|Domain not found|Status: free|No entries found" \
    && echo "<name>.$tld: AVAILABLE" \
    || echo "<name>.$tld: TAKEN (or check failed)"
done
```

Alternate TLD set:

```bash
for tld in ai co me info xyz online shop store blog; do
  echo -n "<name>.$tld: "
  whois "<name>.$tld" 2>/dev/null | grep -qiE "No match for|NOT FOUND|No Data Found|Domain not found|Status: free|No entries found" \
    && echo "AVAILABLE" \
    || echo "TAKEN or lookup error"
done
```

## Step 3 — Single domain deep check

```bash
whois "<name>.$tld" 2>/dev/null | head -30
```

- Registrar info, dates, nameservers → **taken**
- `No match for`, `NOT FOUND`, `No Data Found`, `No entries found`, `No object found` → **available**

Note: some TLDs (e.g., `.dev`) may not have reachable whois servers.

## Step 4 — dig with authoritative nameserver (when host/whois unreliable)

```bash
dig @a.gtld-servers.net "<name>.com" +nostats +noquestion +nocomments 2>&1 | grep -E "NXDOMAIN|NOERROR"
```

- `NXDOMAIN` → available
- `NOERROR` → taken

Common authoritative NS: `.com`/`.net` → `a.gtld-servers.net`, `.org` → `a0.org.afilias-nst.info`, `.info` → `a1.info.afilias-nst.info`, `.io` → `a.nic.io`

## Step 5 — curl RDAP directly (when whois blocked)

RDAP returns structured JSON over HTTPS:

```bash
# Via rdap.org (auto-routes to correct registry)
curl -s "https://rdap.org/domain/<domain>"

# Direct to registry (faster)
curl -s "https://rdap.verisign.com/com/v1/domain/<domain>"  # .com
curl -s "https://rdap.verisign.com/net/v1/domain/<domain>"  # .net
```

- JSON with `ldhName`, `events`, `nameservers` → **taken**
- 404 → **available**
- 429 → rate limited, wait & retry

HEAD request (lighter, just checks existence):

```bash
curl -s -o /dev/null -w "%{http_code}" -X HEAD "https://rdap.org/domain/<domain>"
```

## Step 6 — Python socket check (no dependencies)

Pure Python using stdlib (no whois needed):

```bash
python3 -c "
import socket
for d in ['<domain>.com', '<domain>.io', '<domain>.dev']:
    try:
        socket.getaddrinfo(d, 80)
        print(f'{d}: TAKEN')
    except socket.gaierror:
        print(f'{d}: AVAILABLE')
"
```

## Step 7 — Registrar API (authoritative)

```bash
# WhoisJSON API (1000 free req/month)
curl -s "https://whoisjson.com/api/v1/domain-availability?domain=<domain>"
```

## Step 8 — Web search (last resort)

If everything fails, use `websearch` to check registrar sites or `webfetch` on:

```
https://www.rdap.net/domain/<domain>
```

## Step 9 — Summary output

Present results as a table:

| Domain | Status |
|---|---|
| `example.com` | ❌ Taken |
| `example.dev` | ✅ Available |
| `example.xyz` | ❌ Taken |
| `example.io` | ❌ Taken |
| `example.blog` | ⚠️ Unable to verify |
