from gi.repository import gnomeKeyring as gk
class keyring(object):
	def __init__(self):
		if gk.is_available() is True:
			if "GoogleMusic" in gk.list_keyring_names_sync():
				self.keyring = gk.list_item_ids_sync("GoogleMusic")[1]
				if "loginDetails" in self.keyring:
					self.loginDetails = (gk.list_keyring_ids)

			else:
				gk.create_sync("GoogleMusic","GoogleMusic")
	def _find_key(key,keyring):
		
