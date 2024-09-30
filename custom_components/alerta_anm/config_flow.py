import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

class AlertaANMConfigFlow(config_entries.ConfigFlow, domain="alerta_anm"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validăm datele introduse
            update_interval = user_input.get("update_interval")
            if update_interval and update_interval > 0:
                return self.async_create_entry(title="Alerta ANM", data=user_input)
            else:
                errors["base"] = "invalid_interval"

        # Formulăm schema de configurare
        schema = vol.Schema({
            vol.Required("update_interval", default=10): cv.positive_int
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AlertaANMOptionsFlowHandler(config_entry)

class AlertaANMOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Required("update_interval", default=self.config_entry.options.get("update_interval", 10)): cv.positive_int
        })

        return self.async_show_form(step_id="user", data_schema=schema)
