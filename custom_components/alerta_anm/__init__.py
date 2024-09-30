async def async_setup_entry(hass, config_entry):
    # Forward setup to the sensor platform using the updated method
    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])
    return True

async def async_setup(hass, config):
    return True
