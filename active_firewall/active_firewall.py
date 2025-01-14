from active_firewall.config import Config
from active_firewall.iptables_adapter import IptablesAdapter
from active_firewall.packets_consumers.dos_detector import DosDetector
from active_firewall.packets_consumers.port_scan_detector import PortScanDetector
from active_firewall.packets_interceptor import PacketsInterceptor
from active_firewall.utils.get_ip import get_ip


def activate_firewall():
    listening_interface = Config.get_config('ListeningInterface')
    host_ip = get_ip(listening_interface)

    iptables_adapter = IptablesAdapter(Config.get_config('IptablesChain'))

    consumers = []
    consumers.append(
        DosDetector(iptables_adapter,
                    int(Config.get_config('DosAllowedPacketsPerInterval')),
                    int(Config.get_config('DosLargePacketSize')),
                    int(Config.get_config('DosAllowedLargePacketsPerInterval')),
                    int(Config.get_config('DosRuleTimeoutSeconds')),
                    float(Config.get_config('DosScanningInterval')),
                    ))

    consumers.append(PortScanDetector(iptables_adapter,
                                      int(Config.get_config('PsAllowedPortsPerInterval')),
                                      int(Config.get_config('PsRuleTimeoutSeconds')),
                                      float(Config.get_config('PsScanningInterval')),
                                      ))

    interceptor = PacketsInterceptor()

    for consumer in consumers:
        interceptor.add_consumer(consumer)

    interceptor.start_intercepting(listening_interface, only_incoming_traffic=True, host_ip=host_ip)
