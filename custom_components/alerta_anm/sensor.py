import logging
from datetime import timedelta
import async_timeout
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

JSON_URL = "https://www.meteoromania.ro/wp-json/meteoapi/v2/avertizari-generale"

async def async_setup_entry(hass, config_entry, async_add_entities):
    # Intervalul de actualizare
    update_interval = config_entry.data.get("update_interval", 10)

    sensor = ANMAlertSensor(hass)

    # Creare senzor
    async_add_entities([sensor])

    # Actualizare la intervalul configurat
    async_track_time_interval(hass, sensor.async_update, timedelta(minutes=update_interval))

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
                        if not data or isinstance(data, str):
                            _LOGGER.warning(f"Nu există date disponibile: {data}")
                            self._state = "inactive"
                            self._attributes = {
                                "avertizari": "Nu exista avertizari",
                                "friendly_name": "Avertizări Meteo ANM"
                            }
                            return
                        
                        toate_avertizarile = []
                        for avertizare in data.get('avertizare', []):
                            if isinstance(avertizare, dict):
                                for judet in avertizare.get('judet', []):
                                    if isinstance(judet, dict):
                                        try:
                                            avertizare_judet = {
                                                "judet": judet.get('@attributes', {}).get('cod', 'necunoscut'),
                                                "culoare": judet.get('@attributes', {}).get('culoare', 'necunoscut'),
                                                "fenomene_vizate": avertizare.get('@attributes', {}).get('fenomeneVizate', 'necunoscut'),
                                                "data_expirarii": avertizare.get('@attributes', {}).get('dataExpirarii', 'necunoscut'),
                                                "data_aparitiei": avertizare.get('@attributes', {}).get('dataAparitiei', 'necunoscut'),
                                                "intervalul": avertizare.get('@attributes', {}).get('intervalul', 'necunoscut'),
                                                "mesaj": avertizare.get('@attributes', {}).get('mesaj', 'necunoscut')
                                            }
                                            toate_avertizarile.append(avertizare_judet)
                                        except KeyError as e:
                                            _LOGGER.error(f"Eroare la procesarea datelor pentru județ: {e}")
                                    else:
                                        _LOGGER.error("Judete nu este un dicționar, s-a primit: %s", type(judet))
                                        _LOGGER.debug("Conținut judet: %s", judet)
                            else:
                                _LOGGER.error("Avertizare nu este un dicționar, s-a primit: %s", type(avertizare))
                                _LOGGER.debug("Conținut avertizare: %s", avertizare)
                        
                        if toate_avertizarile:
                            self._state = "active"
                            self._attributes = {
                                "avertizari": toate_avertizarile,
                                "friendly_name": "Avertizări Meteo ANM"
                            }
                        else:
                            self._state = "inactive"
                            self._attributes = {
                                "avertizari": "Nu exista avertizari",
                                "friendly_name": "Avertizări Meteo ANM"
                            }
                        _LOGGER.info("Senzor ANM actualizat cu succes.")
                    else:
                        _LOGGER.error(f"Eroare HTTP {response.status} la preluarea datelor ANM")
        except Exception as e:
            _LOGGER.error(f"Eroare la actualizarea datelor ANM: {e}")
