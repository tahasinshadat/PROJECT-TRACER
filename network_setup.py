import subprocess
import time

def setup_wifi_network(ssid, password):
    # Install hostapd and dnsmasq
    subprocess.run(['sudo', 'apt-get', 'install', 'hostapd', 'dnsmasq', '-y'])

    # Configure hostapd
    hostapd_conf = f'''
interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
    '''

    with open('/etc/hostapd/hostapd.conf', 'w') as file:
        file.write(hostapd_conf)

    # Start hostapd service
    subprocess.run(['sudo', 'systemctl', 'unmask', 'hostapd'])
    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'])

    # Configure dnsmasq
    dnsmasq_conf = f'''
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
    '''

    with open('/etc/dnsmasq.conf', 'w') as file:
        file.write(dnsmasq_conf)

    # Restart dnsmasq service
    subprocess.run(['sudo', 'systemctl', 'restart', 'dnsmasq'])

def start_network():
    # Define network parameters
    ssid = 'TRACER_WIFI'
    password = 'tracerBot'

    try:
        setup_wifi_network(ssid, password)
        print(f'Wi-Fi network "{ssid}" with password "{password}" is now active.')

    except KeyboardInterrupt:
        print('\nWi-Fi network setup interrupted. Cleaning up...')
    finally:
        # Stop hostapd and dnsmasq services
        subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'])
        subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'])
        subprocess.run(['sudo', 'systemctl', 'mask', 'hostapd'])
        subprocess.run(['sudo', 'systemctl', 'mask', 'dnsmasq'])

start_network()
