import config
from app import web
from app.data.model import DatastoreConfig
from app.web.model import WebConfig


def main():
    datastore_config = DatastoreConfig(config.DATASTORE_CONFIG_KIND, config.DATASTORE_CONFIG_ID)
    web_config = WebConfig(config.WEB_API_KEY, config.WEB_HOST_ADDRESS, config.WEB_PORT)
    web.run(web_config, datastore_config)


main()
