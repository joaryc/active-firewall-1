from active_firewall.config import Config
from active_firewall.packets_consumers.dos_detector import DosDetector
from active_firewall.packets_interceptor import PacketsInterceptor
from active_firewall.utils.get_ip import get_ip


def activate_firewall():
    listening_interface = Config.get_config('ListeningInterface')
    host_ip = get_ip(listening_interface)

    consumer = DosDetector(int(Config.get_config('AllowedPacketsPerSecond')))
    interceptor = PacketsInterceptor()

    interceptor.add_consumer(consumer)

    interceptor.start_intercepting(listening_interface, only_incoming_traffic=True, host_ip=host_ip)