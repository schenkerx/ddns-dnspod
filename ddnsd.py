#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2
import json
from time import sleep

# Change it to your account information here
LOGIN_EMAIL = 'example@example.com'
LOGIN_PWD = 'examplepwd'
DOMAIN = 'example.com'
SUBDOMAIN = 'www'
CHECK_INTERVAL = 10 # Time in millis

# dnspod api
DOMAIN_INFO = 'https://dnsapi.cn/Domain.Info'
RECORD_INFO = 'https://dnsapi.cn/Record.Info'
RECORD_LIST = 'https://dnsapi.cn/Record.List'
DDNS = 'https://dnsapi.cn/Record.Ddns'

# Obtain external IP of the server
def get_ext_ip():
    return urllib.urlopen('http://members.3322.org/dyndns/getip').read()

# fire a request to dnspod
def fire_request(url, post_data_dict):
	pub_data_fields = 'login_email=' + LOGIN_EMAIL + '&login_password=' + LOGIN_PWD + '&format=json'
	header = {'User-Agent':'dnspod-ddnsd-py/0.1(xys7326@gmail.com)'}
	post_data = pub_data_fields + '&' + urllib.urlencode(post_data_dict)

	# urllib2 POST data automatically when "data" parameter(The second parameter) given.
	request = urllib2.Request(url, post_data, header) 
	return_msg = urllib2.urlopen(request)

	return return_msg.read()

def get_record_value(domain_id, record_id):
	param = {'domain_id':domain_id, 'record_id':record_id}
	return json.loads(urllib.unquote(fire_request(RECORD_INFO, param)))['record']['value']

def update_record_value(domain_id, record_id, value, subdomain):
	param = {'domain_id':domain_id, 'record_id':record_id, 'sub_domain':subdomain, 'record_line':'默认', 'value':value}
	return json.loads(fire_request(DDNS, param))['status']['code']

def run(domain_id, record_id):
	ext_ip = get_ext_ip();
	record_ip = get_record_value(domain_id, record_id)

	if ext_ip != record_ip:
		update_record_value(domain_id, record_id, ext_ip, SUBDOMAIN)

def main(domain):
	# fetch domain_id
	param = {'domain':domain}
	domain_id = json.loads(urllib.unquote(fire_request(DOMAIN_INFO, param)))['domain']['id']

	# fetch subdomain record_id
	param = {'domain_id':domain_id, 'sub_domain':SUBDOMAIN}
	record_id = json.loads(urllib.unquote(fire_request(RECORD_LIST, param)))['records'][0]['id']

	while True:
		run(domain_id, record_id)
		sleep(CHECK_INTERVAL)

if __name__ == '__main__':
	main(DOMAIN)
