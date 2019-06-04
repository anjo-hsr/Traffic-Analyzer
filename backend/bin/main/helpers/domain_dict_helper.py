from main.helpers.string_helper import remove_quotations


class DomainDictHelper:
    def __init__(self, provider_domain_dict) -> None:
        self.provider_domain_dict = provider_domain_dict
        self.domain_provider_dict = {}
        self.get_domains_to_provider_dict()

    def get_domains_to_provider_dict(self) -> None:
        for key in self.provider_domain_dict:
            for domain in self.provider_domain_dict[key]:
                self.domain_provider_dict[domain] = key

    def check_domains(self, domains) -> bool:
        domain_list = domains.split(",")
        domain_list = list(map(remove_quotations, domain_list))
        return any(self.check_domain(domain) for domain in domain_list)

    def check_domain(self, domain) -> bool:
        for domain_key in self.domain_provider_dict:
            if domain_key in domain:
                return self.test_for_wildcard(domain, domain_key)

        return False

    @staticmethod
    def test_for_wildcard(domain, domain_key) -> bool:
        if domain_key.endswith("."):
            return True

        return DomainDictHelper.test_domain_ending(domain, domain_key)

    @staticmethod
    def test_domain_ending(domain, domain_key) -> bool:
        return domain.endswith(domain_key)
