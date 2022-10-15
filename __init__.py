"""Integrate with Strato DNS service."""
import asyncio
from datetime import timedelta
import logging

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.const import (
    CONF_DOMAIN,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_SCAN_INTERVAL
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "strato"

DEFAULT_INTERVAL = timedelta(minutes=15)

TIMEOUT = 30
HOST = "dyndns.strato.com/nic/update"

STRATO_ERRORS = {
    "nohost": "Hostname supplied does not exist under specified account",
    "badauth": "Invalid username password combination",
    "badagent": "Client disabled",
    "!donator": "An update request was sent with a feature that is not available",
    "abuse": "Username is blocked due to abuse",
}

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_DOMAIN): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_INTERVAL): vol.All(
                    cv.time_period, cv.positive_timedelta
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the STRATO component."""
    conf = config[DOMAIN]
    domain = conf.get(CONF_DOMAIN).strip()
    user = conf.get(CONF_USERNAME).strip()
    password = conf.get(CONF_PASSWORD).strip()
    interval = conf.get(CONF_SCAN_INTERVAL)

    session = async_get_clientsession(hass)

    result = await _update_STRATO(session, domain, user, password)

    if not result:
        return False

    async def update_domain_interval(now):
        """Update the STRATO entry."""
        await _update_STRATO(session, domain, user, password)

    async_track_time_interval(hass, update_domain_interval, interval)

    return True





async def _update_STRATO(session, domain, user, password):
    """Update STRATO."""
    try:
        myip = await session.get(f"https://v6.ident.me/")
        url = f"https://{user}:{password}@{HOST}?hostname={domain}&myip={myip}"
        async with async_timeout.timeout(TIMEOUT):
            resp = await session.get(url)
            body = await resp.text()

            if body.startswith("good") or body.startswith("nochg"):
                _LOGGER.info("Updating STRATO for domain: %s", domain)

                return True

            _LOGGER.warning("Updating STRATO failed: %s => %s", domain, STRATO_ERRORS[body.strip()])

    except aiohttp.ClientError:
        _LOGGER.warning("Can't connect to STRATO API")

    except asyncio.TimeoutError:
        _LOGGER.warning("Timeout from STRATO API for domain: %s", domain)

    return False
