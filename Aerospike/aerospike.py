import aerospike
class AerospikeCacheControl():
      def __init__(self, offer = None):
            self.KEY_DEFAULT = 'id_'
            self.VALUE_DEFAULT_KEY = '{}{}'.format(self.KEY_DEFAULT,offer)
            self.KEY_AEROSPIKE = ('test', 'demo', self.VALUE_DEFAULT_KEY)
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
      
      def delete_array_value_on_cache(self, array):
            client = self.connect_client()
            remove_policy = {'durable_delete': True}
            for item in array:
                  try:
                        client.remove(item, policy=remove_policy)
                        client.close()
                  except:
                        print("occurring error")

            return "clear cache for keys: {}".format(array)

      def generate_multiples_keys(self, array):
            for item in range(len(array)): 
                  array[item] = ('test', 'demo', f"{self.KEY_DEFAULT}{array[item]}")
            return array

            