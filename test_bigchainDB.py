import datetime
import sched, time,random

import bigchaindb_driver 
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver import BigchainDB

from collections import namedtuple
import uuid

#initialize BigchainDB
tokens = {}
tokens['app_id'] = '1dbffde9'
tokens['app_key'] = '7675f75d19e546b4dae21c858c4c9827'

#bdb = BigchainDB('http://147.83.39.61:9984', headers=tokens)
bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)

print(bigchaindb_driver.__version__)
parking = generate_keypair()
owner = generate_keypair()
propietari = generate_keypair()


CryptoKeypair = namedtuple('CryptoKeypair', ('private_key', 'public_key'))
asset = {
    "data": {
        "ParkingId"   : str(uuid.uuid3(uuid.NAMESPACE_DNS, parking.public_key)),
        "SlotId"      : str(uuid.uuid1()),
        "SlotOwnerId" : str(uuid.uuid3(uuid.NAMESPACE_DNS, propietari.public_key)),
#        "type"        : "SmileSlot",
        "type"        : "ProvaS2",
    }
}

metadata = {
    "metadata":{
        "slotStatus": "Free",
        "timestamp" : str(datetime.datetime.utcnow()),
        "UserId"    : "-",
    }
}

prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=owner.public_key,
        asset=asset,
        metadata=metadata)
fulfilled_creation_tx = bdb.transactions.fulfill(prepared_creation_tx, private_keys=owner.private_key)
sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)
print("TRANSACTION " + str(sent_creation_tx) + "\n")
