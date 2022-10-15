# Strato DDNS Updater Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

With the `strato` integration you can keep your current IP address in sync with your [STRATO DDNS](https://www.strato.de/faq/hosting/so-einfach-richten-sie-dyndns-fuer-ihre-domains-ein/)  hostname or domain.  

To use the integration in your installation, add the following to your `configuration.yaml` file:

#### Configuration variables:
| Variable |  Required  |  Type  | Description |
| -------- | ---------- | ----------- | ----------- |
| `domain` | yes | string |  The subdomain you are modifying the DNS configuration for |
| `username` | yes | string | The DynHost username |
| `password` | yes | string | Password for the DynHost username |
| `scan_interval` | no |  time | How often to call the update service. (default: 10 minutes) |

#### Basic Example:

```yaml
strato:
  domain: subdomain.domain.com
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```
Based on the official [No-IP.com](https://github.com/home-assistant/core/tree/dev/homeassistant/components/no_ip) and [Mythic Beasts](https://github.com/home-assistant/core/blob/dev/homeassistant/components/mythicbeastsdns) integrations. Thanks to the creators!
