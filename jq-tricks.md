---
title: jq tricks
description: ""
lead: ""
date: "2019-12-06T12:15:51-05:00"
lastmod: "2019-12-06T12:15:51-05:00"
categories:
  - cli
tags:
  - bash
  - cli
  - jq
draft: false
weight: 50
images: []
contributors:
  - Steve Sosik
---

# Filter a list of maps by matching a specific key:
<https://stedolan.github.io/jq/manual/#select(boolean_expression)>
<https://stedolan.github.io/jq/manual/#test(val),test(regex;flags)>
```
egrep "\Wca\W" /u4/dhafeman/vkms_audit_log_dec5-6 | sed -re 's%<.*> vkms0-syscomm-stg %%g' | jq -r 'select(.request.path | test("platform-ca/*"))' | less
```

# Test if a given map has a key:
<https://stedolan.github.io/jq/manual/#has(key)>
```
curl  -X POST -s --key $HOME/.certs/${USER}-testnet.key --cert $HOME/.certs/${USER}-testnet.crt -k -H "Content-Type: application/json" https://pull.lighthouse.shared.qa/api/v2/namespaces/vkms/metrics/http_response_time.gauge/query -d '{"tags": {"app": ["vkms0-ssosik"]}, "startTime": '$(date --date "1 day ago" +%s)', "endTime": '$(date +%s)', "aggregators": [{"type" : "AVG", "sampling": "PT10M", "alignStartTime": false, "dataPointPosition": "MIDDLE"}]}' | jq -r '.[].tags | has("host")'
```

# Read a value at a specific key which contains a special character:

```
vault read sys/mounts -format=JSON | jq -r  '.data["platform-ca/"]'
```

# jq flatten list

```bash
jq -r '.[]'
```

# Other snippets

## Debugging for service mesh matching vkms_audit log for a specific thing
```
grep '"service_account_namespace":"istio-monitoring"' vkms_audit.log | cut -d\  -f2- | /a/bin/jq -r .
```

# Filter a substructure by matching on the key

```bash
# Just filter, the resulting data structure is modified to a key=value format
vault read sys/mounts -format=json | jq -r '.data | to_entries | map(select(.key | match("<submatch string>")))'

# Convert the filtered structure back into a substructure as it was in the original data
vault read sys/mounts -format=json | jq -r '.data | to_entries | map(select(.key | match("test"))) | map(.value)'
```

# Attempting to filter vkms_audit log for only interesting requests

Grep through archived vkms_audit logs for requests where the client attempted to
sign or issue certs on `platform-ca`:

```bash
# WIP: -c does not pretty print
zcat vkms_audit.log.235p5-ml60b-2uwd4-h22rh-j0226.2884.1590676320.1590676462.gz | cut -f2- -d\  | \
  /a/bin/jq -c 'select( .type | contains("request"))' | less
# WIP: same as above, -r does pretty print
zcat vkms_audit.log.235p5-ml60b-2uwd4-h22rh-j0226.2884.1590676320.1590676462.gz | cut -f2- -d\  | \
  /a/bin/jq -r 'select( .type | contains("request"))' | less

# Filter by type and request.path
zcat vkms_audit.log.235p5-ml60b-2uwd4-h22rh-j0226.2884.1590676320.1590676462.gz | cut -f2- -d\  | \
  /a/bin/jq -r 'select( .type | contains("request")) | select( .request.path | contains("platform-ca"))' | less

# Exclude entries that had an error:
zcat vkms_audit.log.235p5-ml60b-2uwd4-h22rh-j0226.2884.1590676320.1590676462.gz | cut -f2- -d\  | \
  /a/bin/jq -r 'select( .type | contains("request")) | select( .request.path | contains("platform-ca")) | select( has("error") | not)' | less

# Filter down to just the interesting data
zcat vkms_audit.log.235p5-ml60b-2uwd4-h22rh-j0226.2884.1590676320.1590676462.gz | cut -f2- -d\  | \
  /a/bin/jq -r 'select( .type | contains("request")) | select( .request.path | contains("platform-ca")) | select( has("error") | not) | .time, .auth.metadata.role, .auth.display_name, .auth.token_type, .request.path' | less

# Instead of filter, return a new map
zcat vkms_audit.log.235p5-ml60b-2uwd4-h22rh-j0226.2884.1590676320.1590676462.gz | cut -f2- -d\  | \
  /a/bin/jq -c 'select( .type | contains("request")) | select( .request.path | contains("platform-ca")) | select( has("error") | not) | {time: .time, role: .auth.metadata.role, name: .auth.display_name, token_type: .auth.token_type, path: .request.path}' | less

# Iterate over all gzip files:
for F in /a/logs/abattery_apps.old/vkms0-syscomm/vkms_audit.log.old/*.gz
do zcat $F | cut -f2- -d\  | /a/bin/jq -c 'select( .type | contains("request")) | select( .request.path | contains("platform-ca")) | select( has("error") | not) | {time: .time, role: .auth.metadata.role, name: .auth.display_name, token_type: .auth.token_type, path: .request.path}' >> /tmp/platform-ca-requests.json
done

# Similar to previous, but get all errored requests:
for F in *.gz
do zcat $F | cut -f2- -d\  | /a/bin/jq -c 'select( .type | contains("request")) | select( .request.path | contains("platform-ca")) | select( has("error")) | {time: .time, role: .auth.metadata.role, name: .auth.display_name, token_type: .auth.token_type, path: .request.path}' >> /tmp/platform-ca-error-requests.json
done

# Look for requests on platform-ca that were NOT issue or signs
grep -v 'sign\|issue' /tmp/platform-ca-requests.json

# Get all paths and count their calls
/a/bin/jq -r .path /tmp/platform-ca-requests.json | sort | uniq -c

# Get all entries on a specific path
/a/bin/jq -r 'select( .path == "platform-ca/issue/kaas" )' /tmp/platform-ca-requests.json | less

# Get all entries NOT using batch tokens
/a/bin/jq -r 'select( .token_type == "batch" | not)' /tmp/platform-ca-requests.json | less
/a/bin/jq -c 'select( .token_type == "batch" | not)' /tmp/platform-ca-requests.json
```

# Ignore non-JSON lines

From https://stackoverflow.com/questions/41599314/ignore-unparseable-json-with-jq

```bash
jq -c -R 'fromjson? | select( .type | contains("request")) ...'
```

# Map filtering and string formatting

```bash
# Filter/reduce a map to just interesting things
╰─ terraform show -json | jq '.values.root_module.resources[] | select(.address == "vault_mount.local_pki_engines")'
{
  "address": "vault_mount.local_pki_engines",
  "mode": "managed",
  "type": "vault_mount",
  "name": "local_pki_engines",
  "index": "vkms_telegraf",
  "provider_name": "vault",
  "schema_version": 0,
  "values": {
    "accessor": "pki_a79f0623",
    "default_lease_ttl_seconds": 0,
    "description": "enable vkms_telegraf PKI engine",
    "id": "pki_vkms_telegraf",
    "local": false,
    "max_lease_ttl_seconds": 0,
    "options": null,
    "path": "pki_vkms_telegraf",
    "type": "pki"
  }
}
{
  "address": "vault_mount.local_pki_engines",
  "mode": "managed",
  "type": "vault_mount",
  "name": "local_pki_engines",
  "index": "akauser",
  "provider_name": "vault",
  "schema_version": 0,
  "values": {
    "accessor": "pki_8464fdcc",
    "default_lease_ttl_seconds": 0,
    "description": "enable akauser PKI engine",
    "id": "pki_akauser",
    "local": false,
    "max_lease_ttl_seconds": 0,
    "options": null,
    "path": "pki_akauser",
    "type": "pki"
  }
}

# Select specific attributes from the matches and format them
╰─ terraform show -json | jq -r '.values.root_module.resources[] | select(.address == "vault_mount.local_pki_engines") | "My Format \(.index) foo \(.values.path)"'
My Format akauser foo pki_akauser
My Format vkms_telegraf foo pki_vkms_telegraf
```

# jq query with special characters in the keys

From <https://github.com/stedolan/jq/issues/140>

To select the top-level key "sys/" (containing a backslash) use the following
query:
```bash
jq -r '.["sys/"]'
```

Should be similar for other keys containing special characters.
