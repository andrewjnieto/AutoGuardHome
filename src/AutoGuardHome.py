from adguardhome import AdGuardHome

import asyncio
import json
import datetime
import logging.config

def load_file(file_path):
    with open(file_path) as config_file:
        config = json.load(config_file)
        return config

def init_logger():
    logger_config = load_file('../resources/config/logger_config.json')
    logging.config.dictConfig(logger_config)
    logging.info(f"Loaded the following logger config: {logger_config}") 

async def set_blocked_services(services, adguard):
    response = await adguard.request(uri='blocked_services/set',
                          method='POST',
                          json_data=services)
    return response

async def set_blocked_websites(websites, adguard):
    response = await adguard.request(uri='filtering/set_rules',
                                     method='POST',
                                     json_data=websites)
    return response

async def main():
    init_logger()
    secrets = load_file('../resources/secrets/server_config.json')
    times = load_file('../resources/config/times.json')
    blocked_services = load_file('../resources/config/blocked_services.json')
    blocked_websites = load_file('../resources/config/blocked_websites.json')
    logging.debug("debug")
    async with AdGuardHome(host=secrets['host'],
                           port=secrets['port'],
                           username=secrets['username'],
                           password=secrets['password']) as adguard:
        hour = datetime.datetime.now().hour
        if times['lock_hour'] == hour:
            logging.info('Blocking services and websites')
            await set_blocked_services(blocked_services, adguard)
            await set_blocked_websites(blocked_websites, adguard)
            logging.info('Successfully blocked services and websites')
        elif times['unlock_hour'] == hour:
            logging.info('Unblocking services and websites')
            await set_blocked_services([], adguard)
            await set_blocked_websites({}, adguard)
            logging.info('Successfully unblocked services and websites')
        else:
            logging.info('Time to get a new watch')

if __name__ == "__main__":
    asyncio.run(main())
