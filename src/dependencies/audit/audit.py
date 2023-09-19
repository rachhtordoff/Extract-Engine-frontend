import requests
import json
from datetime import datetime

class Audit_logger(object):
	def __init__(self, audit_api_url, component):
		self.audit_api_url = audit_api_url
		self.component = component

		print("audit logger initialized", flush=True)

	def send_audit_message(self, message, request, event, actor_type, client_id=None, staff_id=None, company_id=None):
		date = datetime.now().isoformat()

		#in flask ip address will be at request.headers["X-Forwarded-For"]


		if "X-Forwarded-For" in request.headers.keys():
			ip_addresses= request.headers["X-Forwarded-For"]
			ip_addresses = ip_addresses.split(",")
			ip_address = ip_addresses[0]
		else:
			ip_address = request.remote_addr

		audit_data = {
			"component": self.component,
			"date": date,
			"message": message,
			"event": event,
			"actor_type": actor_type,
			"ip_address": ip_address
		}

		if company_id:
			audit_data["company_id"] = company_id
		if client_id:
			audit_data["client_id"] = client_id
		if staff_id:
			audit_data["staff_id"] = staff_id

		if self.__make_audit_call(audit_data):
			return True
		return False

	def send_logged_audit_message(self, message, request, event, actor_type, client_id, staff_id=None, company_id=None):
		date = datetime.now().isoformat()

		#in flask ip address will be at request.headers["X-Forwarded-For"]


		if "X-Forwarded-For" in request.headers.keys():
			ip_addresses= request.headers["X-Forwarded-For"]
			ip_addresses = ip_addresses.split(",")
			ip_address = ip_addresses[0]
		else:
			ip_address = request.remote_addr

		audit_data = {
			"component": self.component,
			"date": date,
			"message": message,
			"event": event,
			"actor_type": actor_type,
			"ip_address": ip_address
		}

		if company_id:
			audit_data["company_id"] = company_id
		if client_id:
			audit_data["client_id"] = client_id
		if staff_id:
			audit_data["staff_id"] = staff_id

		if self.__make_logged_audit_call(audit_data):
			return True
		return False

	def __make_audit_call(self, audit_data):
		url = "{}/audit".format(self.audit_api_url)

		payload = json.dumps(audit_data)
		headers = {'Content-Type': "application/json"}

		response = requests.request("POST", url, data=payload, headers=headers)

		print(response.text)
		if response.status_code == 200:
			return True
		return False

	def __make_logged_audit_call(self, audit_data):
		url = "{}/logged_audit".format(self.audit_api_url)

		payload = json.dumps(audit_data)
		headers = {'Content-Type': "application/json"}

		response = requests.request("POST", url, data=payload, headers=headers)

		print(response.text)
		if response.status_code == 200:
			return True
		raise Exception('I know Python!')

