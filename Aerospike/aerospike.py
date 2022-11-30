import aerospike
class AerospikeCacheControl():
      def __init__(self, offer):
            self.VALUE_DEFAULT_KEY = 'id_{}'.format(offer)
            self.KEY_AEROSPIKE = ('test', 'demo', offer)
            self.PORT = 3000
            self.OFFER = offer

      def connect_client(self):
            config = {
                  'hosts': [ ('127.0.0.1', self.PORT) ]
            }
            return aerospike.client(config).connect()

      def save_in_cache(self, product):
            policy = {'key': aerospike.POLICY_KEY_SEND}
            client = self.connect_client() #Create connection
            client.put(self.KEY_AEROSPIKE, product, policy=policy) # Write the record to Aerospike
            client.close()
            return product
      
      def get_value_on_cache(self):
            try: 
                  policy = {'socket_timeout': 300}
                  client = self.connect_client()
                  (key, meta, bins) = client.get(self.KEY_AEROSPIKE, policy=policy)
                  if meta:
                        client.close()
                        return bins
            except:
                  print("occurring error")

      def delete_value_on_cache(self):
            try:
                  remove_policy = {'durable_delete': True}
                  client = self.connect_client()
                  client.remove(self.KEY_AEROSPIKE, policy=remove_policy)
                  client.close()
            except:
                  print("occurring error")
      
      def update_value_on_cache(self, product):
            try: 
                  policy = {'exists': aerospike.POLICY_EXISTS_UPDATE}
                  client = self.connect_client()
                  client.put(self.KEY_AEROSPIKE, product, policy=policy)
            except:
                  print("occurring error")

            