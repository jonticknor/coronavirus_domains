import certstream
import datetime

'''
Use CaliDog certstream URL for testing purposes.
It is recommended that you run your own CertStream Server
for better results/higher data throughput
'''
certstream_url = 'wss://certstream.calidog.io'
# certstream_url = 'ws://127.0.0.1:4000'
domain_log = 'corona_domains.txt'

longlist = set()

# Add keywords for things you are interested in
keywords = {
    'coronavirus',
    'covid'
}

def callback(message, context):
    # Callback handler for certstream events (boilerplate from CaliDog Github)
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        for domain in all_domains:
            # Filter domain if we have already seen it (prevent duplication)
            if domain in longlist:
                continue
            longlist.add(domain)
            
            # Check if keyword exists
            if any(kword in domain for kword in keywords):
                with open(domain_log, 'a') as f:
                    f.write("{}: {}\n".format(str(datetime.datetime.now()), domain))
                    print(str(datetime.datetime.now()) + ': ' + domain)


if __name__ == '__main__':
    certstream.listen_for_events(callback, url=certstream_url)
