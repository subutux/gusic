from gi.repository import gnomeKeyring as gk
class keyring(object):
	def __init__(self):
		if gk.is_available() is True:
			if "GoogleMusic" in gk.list_keyring_names_sync():
				self.keyring = gk.list_item_ids_sync("GoogleMusic")[1]
				
