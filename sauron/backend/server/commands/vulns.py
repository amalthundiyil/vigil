from sauron.processor.vulns import VulnsProcessor


def process_vulns(url):
    vulns = VulnsProcessor(url)
    reports = vulns.process()
    return reports


def check_vulns(url):
    pass
