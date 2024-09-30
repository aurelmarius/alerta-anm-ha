import logging
from datetime import timedelta
import async_timeout
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.aiohttp_client import async_get_clientsession  # Import direct al funcției

_LOGGER = logging.getLogger(__name__)

JSON_URL = "https://www.meteoromania.ro/wp-json/meteoapi/v2/avertizari-generale"

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the ANM sensor based on the config_entry."""
    # Intervalul de actualizare
    update_interval = config_entry.data.get("update_interval", 10)

    sensor = ANMAlertSensor(hass)

    # Creare senzor
    async_add_entities([sensor])

    # Actualizare la intervalul configurat
    async_track_time_interval(hass, lambda now: sensor.async_update(), timedelta(minutes=update_interval))

class ANMAlertSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Avertizări Meteo ANM"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:weather-lightning-rainy"

    async def async_update(self, now=None):
        _LOGGER.debug("Actualizare date Avertizări Meteo ANM")
        try:
            async with async_timeout.timeout(10):
                session = async_get_clientsession(self._hass)
                async with session.get(JSON_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        toate_avertizarile = []
                        for avertizare in data['avertizare']:
                            for judet in avertizare['judet']:
                                avertizare_judet = {
                                    "judet": judet['@attributes']['cod'],
                                    "culoare": judet['@attributes']['culoare'],
                                    "fenomene_vizate": avertizare['@attributes']['fenomeneVizate'],
                                    "data_expirarii": avertizare['@attributes']['dataExpirarii'],
                                    "data_aparitiei": avertizare['@attributes']['dataAparitiei'],
                                    "intervalul": avertizare['@attributes']['intervalul']
                                }
                                toate_avertizarile.append(avertizare_judet)
                        self._state = "active" if toate_avertizarile else "inactive"
                        self._attributes = {
                            "avertizari": toate_avertizarile,
                            "friendly_name": "Avertizări Meteo ANM"
                        }
                        _LOGGER.info("Senzor ANM actualizat cu succes.")
                    else:
                        _LOGGER.error(f"Erroare HTTP {response.status} la preluarea datelor ANM")
        except Exception as e:
            _LOGGER.error(f"Eroare la actualizarea datelor ANM: {e}")
