import aerospike

VALUE_DEFAULT_KEY = 'id_'
KEY_AEROSPIKE = ('test', 'demo', 'key')

def connect_client():
      config = {
            'hosts': [ ('127.0.0.1', 3000) ]
      }
      return aerospike.client(config).connect()

def save_in_cache(product):
      id = VALUE_DEFAULT_KEY + str(product["id"])
      data = {id: product}
      policy = {'key': aerospike.POLICY_KEY_SEND}
      client = connect_client() #Create connection
      client.put(KEY_AEROSPIKE ,data, policy=policy) # Write the record to Aerospike
      client.close()
     
def get_value_on_cache(product_id):
      id = VALUE_DEFAULT_KEY + str(product_id)
      policy = {'socket_timeout': 300}
      client = connect_client()
      try: 
            (key_, meta, bins) = client.select(KEY_AEROSPIKE, (id, ), policy=policy)
            client.close()
            return bins[id]
      except:
            print("occurring error")

def delete_value_on_cache(product_id):
      id = VALUE_DEFAULT_KEY + str(product_id)
      remove_policy = {'durable_delete': True}
      client = connect_client()
      try:
            client.remove(KEY_AEROSPIKE, policy=remove_policy)
      except:
            print("occurring error")
      client.close()