from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
from scrapy.core.downloader.tls import ScrapyClientTLSOptions


class CustomClientTLSOptions(ScrapyClientTLSOptions):
    def clientConnectionForTLS(self, tlsProtocol):
        context = self._ctx
        connection = SSL.Connection(context,None)
        connection.set_app_data(tlsProtocol)
        KeyLog_path = r'/home/fu/Documents/wireshark/etsy_sslkey.log'
        key_log = 'CLIENT_RANDOM %s %s\n' % (connection.client_random(), connection.master_key())
        with open(KeyLog_path,'w') as f:
            f.write(key_log)
        return connection


class CustomContextFactory(ScrapyClientContextFactory):
    def creatorForNetloc(self, hostname, port):
        return CustomClientTLSOptions(hostname.decode("ascii"), self.getContext())