from typing import Dict

from main.helpers.string_helper import remove_quotations


class CdnDict:
    def __init__(self):
        # Source from https://github.com/WPO-Foundation/wptagent/blob/master/internal/optimization_checks.py
        self.cdn_names = {
            'Advanced Hosters CDN': ['.pix-cdn.org'],
            'afxcdn.net': ['.afxcdn.net'],
            'Akamai': ['.akamai.net',
                       '.akamaized.net',
                       '.akamaiedge.net',
                       '.akamaihd.net',
                       '.edgesuite.net',
                       '.edgekey.net',
                       '.srip.net',
                       '.akamaitechnologies.com',
                       '.akamaitechnologies.fr'],
            'Akamai China CDN': ['.tl88.net'],
            'Alimama': ['.gslb.tbcache.com'],
            'Amazon CloudFront': ['.cloudfront.net'],
            'Aryaka': ['.aads1.net',
                       '.aads-cn.net',
                       '.aads-cng.net'],
            'AT&T': ['.att-dsa.net'],
            'Azion': ['.azioncdn.net',
                      '.azioncdn.com',
                      '.azion.net'],
            'BelugaCDN': ['.belugacdn.com',
                          '.belugacdn.link'],
            'Bison Grid': ['.bisongrid.net'],
            'BitGravity': ['.bitgravity.com'],
            'Blue Hat Network': ['.bluehatnetwork.com'],
            'BO.LT': ['bo.lt'],
            'BunnyCDN': ['.b-cdn.net'],
            'Cachefly': ['.cachefly.net'],
            'Caspowa': ['.caspowa.com'],
            'Cedexis': ['.cedexis.net'],
            'CDN77': ['.cdn77.net',
                      '.cdn77.org'],
            'CDNetworks': ['.cdngc.net',
                           '.gccdn.net',
                           '.panthercdn.com'],
            'CDNsun': ['.cdnsun.net'],
            'CDNvideo': ['.cdnvideo.ru',
                         '.cdnvideo.net'],
            'ChinaCache': ['.ccgslb.com'],
            'ChinaNetCenter': ['.lxdns.com',
                               '.wscdns.com',
                               '.wscloudcdn.com',
                               '.ourwebpic.com'],
            'Cloudflare': ['.cloudflare.com',
                           '.cloudflare.net'],
            'Cotendo CDN': ['.cotcdn.net'],
            'cubeCDN': ['.cubecdn.net'],
            'Edgecast': ['edgecastcdn.net',
                         '.systemcdn.net',
                         '.transactcdn.net',
                         '.v1cdn.net',
                         '.v2cdn.net',
                         '.v3cdn.net',
                         '.v4cdn.net',
                         '.v5cdn.net'],
            'Facebook': ['.facebook.com',
                         '.facebook.net',
                         '.fbcdn.net',
                         '.cdninstagram.com'],
            'Fastly': ['.fastly.net',
                       '.fastlylb.net',
                       '.nocookie.net'],
            'GoCache': ['.cdn.gocache.net'],
            'Google': ['.google.',
                       'googlesyndication.',
                       'youtube.',
                       '.googleusercontent.com',
                       'googlehosted.com',
                       '.gstatic.com',
                       '.doubleclick.net'],
            'HiberniaCDN': ['.hiberniacdn.com'],
            'Highwinds': ['hwcdn.net'],
            'Hosting4CDN': ['.hosting4cdn.com'],
            'ImageEngine': ['.imgeng.in'],
            'Incapsula': ['.incapdns.net'],
            'Instart Logic': ['.insnw.net',
                              '.inscname.net'],
            'Internap': ['.internapcdn.net'],
            'jsDelivr': ['cdn.jsdelivr.net'],
            'KeyCDN': ['.kxcdn.com'],
            'KINX CDN': ['.kinxcdn.com',
                         '.kinxcdn.net'],
            'LeaseWeb CDN': ['.lswcdn.net',
                             '.lswcdn.eu'],
            'Level 3': ['.footprint.net',
                        '.fpbns.net'],
            'Limelight': ['.llnwd.net',
                          '.llnwi.net',
                          '.lldns.net'],
            'MediaCloud': ['.cdncloud.net.au'],
            'Medianova': ['.mncdn.com',
                          '.mncdn.net',
                          '.mncdn.org'],
            'Microsoft Azure': ['.vo.msecnd.net',
                                '.azureedge.net',
                                '.azure.microsoft.com'],
            'Mirror Image': ['.instacontent.net',
                             '.mirror-image.net'],
            'NetDNA': ['.netdna-cdn.com',
                       '.netdna-ssl.com',
                       '.netdna.com'],
            'Netlify': ['.netlify.com'],
            'NGENIX': ['.ngenix.net'],
            'NYI FTW': ['.nyiftw.net',
                        '.nyiftw.com'],
            'OnApp': ['.r.worldcdn.net',
                      '.r.worldssl.net'],
            'Optimal CDN': ['.optimalcdn.com'],
            'PageRain': ['.pagerain.net'],
            'PUSHR': ['.pushrcdn.com'],
            'Rackspace': ['.raxcdn.com'],
            'Reapleaf': ['.rlcdn.com'],
            'Reflected Networks': ['.rncdn1.com',
                                   '.rncdn7.com'],
            'ReSRC.it': ['.resrc.it'],
            'Rev Software': ['.revcn.net',
                             '.revdn.net'],
            'Roast.io': ['.roast.io'],
            'Rocket CDN': ['.streamprovider.net'],
            'section.io': ['.squixa.net'],
            'SFR': ['cdn.sfr.net'],
            'Simple CDN': ['.simplecdn.net'],
            'Singular CDN': ['.singularcdn.net.br'],
            'StackPath': ['.stackpathdns.com'],
            'SwiftCDN': ['.swiftcdn1.com',
                         '.swiftserve.com'],
            'Taobao': ['.gslb.taobao.com',
                       'tbcdn.cn',
                       '.taobaocdn.com'],
            'Telenor': ['.cdntel.net'],
            'TRBCDN': ['.trbcdn.net'],
            'Twitter': ['.twimg.com'],
            'UnicornCDN': ['.unicorncdn.net'],
            'VegaCDN': ['.vegacdn.vn',
                        '.vegacdn.com'],
            'VoxCDN': ['.voxcdn.net'],
            'WordPress': ['.wp.com',
                          '.wordpress.com',
                          '.gravatar.com'],
            'XLabs Security': ['.xlabs.com.br',
                               '.armor.zone'],
            'Yahoo': ['.ay1.b.yahoo.com',
                      '.yimg.',
                      '.yahooapis.com'],
            'Yottaa': ['.yottaa.net'],
            'Zenedge': ['.zenedge.net']
        }

    def get_cdn_name_to_domains(self) -> Dict[str, str]:
        return self.cdn_names

    def get_cdn_domains_to_names(self) -> Dict[str, str]:
        cdn_domains = {}
        for key in self.cdn_names.keys():
            for domain in self.cdn_names[key]:
                cdn_domains[domain] = key

        return cdn_domains

    def check_domains(self, domains) -> bool:
        domain_list = domains.split(",")
        domain_list = list(map(lambda domain: remove_quotations(domain), domain_list))
        return any(self.check_domain(domain) for domain in domain_list)

    def check_domain(self, domain) -> bool:
        domain_keys = self.get_cdn_domains_to_names().keys()
        for domain_key in domain_keys:
            if domain_key in domain:
                return self.test_for_wildcard(domain, domain_key)

        return False

    @staticmethod
    def test_for_wildcard(domain, domain_key):
        if not domain_key.endswith("."):
            return CdnDict.test_domain_ending(domain, domain_key)
        return True

    @staticmethod
    def test_domain_ending(domain, domain_key):
        return domain.endswith(domain_key)
