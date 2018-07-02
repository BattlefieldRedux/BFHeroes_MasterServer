from Database import Database
from Utilities.Packet import Packet

db = Database()


def HandleGetStats(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetStats")

    requestedKeysNumber = int(data.get("PacketData", "keys.[]"))
    requestedKeys = []

    isUser = False
    for i in range(requestedKeysNumber):
        key = data.get("PacketData", "keys." + str(i))
        if key == 'cdm' or key == 'edm':
            isUser = True

        requestedKeys.append(key)

    if isUser:
        keysValues = db.GetStats(data.get('PacketData', 'owner'), "account", requestedKeys)
    else:
        keysValues = db.GetStats(data.get('PacketData', 'owner'), "persona", requestedKeys)

    for i in range(len(requestedKeys)):
        toSend.set("PacketData", "stats." + str(i) + ".key", keysValues[i]['name'])
        toSend.set("PacketData", "stats." + str(i) + ".value", str(keysValues[i]['value']))
        toSend.set("PacketData", "stats." + str(i) + ".text", keysValues[i]['text'])

    toSend.set("PacketData", "stats.[]", str(requestedKeysNumber))

    Packet(toSend).send(self, "rank", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetStats':
        HandleGetStats(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)
