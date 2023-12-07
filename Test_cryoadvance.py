#!/usr/bin/env python3
#

import cryoadvance
cryo = cryoadvance.CryoAdvance('192.168.1.207')

# Shows how to use high-level methods for accessing common functions
#cryo.cooldown()
#cryo.set_platform_target_temperature(3.1)
print(cryo.get_platform_temperature())
print(cryo.get_platform_temperature_rate())
print(cryo.get_platform_temperature_stability()[0])
#cryo.get_platform_temperature_stability()
#cryo.warmup()

# Shows how to use generic post/get/put methods for accessing any REST url/end-point
#cryo.call_method('/controller/methods/cooldown()')
#cryo.get_prop('/sampleChamber/temperatureControllers/platform/thermometer/sample')['sample']['temperature']
#cryo.set_prop('/controller/properties/platformTargetTemperature', 1.7)
