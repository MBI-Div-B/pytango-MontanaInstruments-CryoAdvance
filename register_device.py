import tango

dev_info = tango.DbDevInfo()
dev_info.server = "Cryostat/test"
dev_info._class = "Cryostat"
dev_info.name = "test/cryo/1"

db = tango.Database()
db.add_device(dev_info)
