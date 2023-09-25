
import toml

class config:
    

    data = toml.load("config.toml")
    TELEGRAM_API_ID = data.get("TELEGRAM_API_ID", 0)
    TELEGRAM_API_HASH = data.get("TELEGRAM_API_HASH", '')