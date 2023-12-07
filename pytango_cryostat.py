#!/usr/bin/env python3
#
"""
Class to simplify RESTful API communication with the s-series Cryostation instrument.

Example usage:
 import scryostation
 cryo = scryostation.SCryostation('192.168.1.123')

 # Shows how to use high-level methods for accessing common functions
 cryo.cooldown()
 cryo.set_platform_target_temperature(3.1)
 cryo.get_platform_temperature()
 cryo.get_platform_temperature_stability()
 cryo.warmup()

 # Shows how to use generic post/get/put methods for accessing any REST url/end-point
 cryo.call_method('/controller/methods/cooldown()')
 cryo.get_prop('/sampleChamber/temperatureControllers/platform/thermometer/sample')['sample']['temperature']
 cryo.set_prop('/controller/properties/platformTargetTemperature', 1.7)
"""
import sys
import os
import time

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

import cryoadvance

class Cryostat(Device):

    # -----------------
    # Device Properties
    # -----------------

    IP = device_property(
        dtype='DevString'
    )

    # ----------
    # Attributes
    # ----------

    ptemp = attribute(
        dtype='DevFloat',
        access=AttrWriteType.READ,
        label="Platform temperature",
        unit="degree",
        format="%6.3f",
        doc="Platform temperature in K",
        fget = "get_ptemp",
    )

    settemp = attribute(
        dtype='DevFloat',
        access=AttrWriteType.READ_WRITE,
        label="Platform temperature setpoint",
        unit="degree",
        format="%6.3f",
        doc="Sample temperature in K",
        min_value = 0,
        max_value = 350,
        fget = "get_settemp",
        fset = "set_ptemp",
    )

    stemp = attribute(
        dtype='DevFloat',
        access=AttrWriteType.READ,
        label="Sample temperature",
        unit="degree",
        format="%6.3f",
        doc="Sample temperature in K",
        fget = "get_stemp",
    )
    
    isStable = attribute(label="Stable",
        dtype=bool,
        access=AttrWriteType.READ,
        doc="True if platform temperature is stable",
        fget = "get_stability")



    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        self.device = cryoadvance.CryoAdvance(self.IP)
        self.set_state(DevState.ON)

    def cooldown(self):
        self.device.cooldow()

    def warmup(self):
        self.device.warmup()

    def pull_vacuum(self):
        self.device.pull_vacuum()

    def abort(self):
        self.device.abort_goal()

    # ------------------
    # Attributes methods
    # ------------------

    def get_ptemp(self):
        return self.device.get_platform_temperature()

    def set_ptemp(self, value):
        self.device.set_platform_temperature(value)

    def get_stability(self):
        return self.device.get_platform_temperature_stability()[0]

    def get_stemp(self):
        return self.device.get_sample_temperature()
        
    def get_settemp(self):
        return self.device.get_platform_target_temperature()


if __name__ == "__main__":
    Cryostat.run_server()

"""
    #
    # Magneto-Optic
    #
    def get_mo_enabled(self):
        r = self.get_prop('/magnetoOptic/magnet/properties/enabled')
        return r['enabled']
    
    def set_mo_enabled(self, enabled):
        return self.set_prop('/magnetoOptic/magnet/properties/enabled', enabled)
    
    def get_mo_state(self):
        r = self.get_prop('/magnetoOptic/magnet/properties/state')
        return r['state']
    
    def get_mo_safe_mode(self):
        r = self.get_prop('/magnetoOptic/magnet/properties/safeMode')
        return r['safeMode']

    def get_mo_calculated_field(self):
        r = self.get_prop('/magnetoOptic/magnet/properties/calculatedField')
        return r['calculatedField']

    def get_mo_measured_current(self):
        r = self.get_prop('/magnetoOptic/magnet/properties/measuredCurrent')
        return r['measuredCurrent']

    def get_mo_target_field(self):
        r = self.get_prop('/magnetoOptic/magnet/properties/targetField')
        return r['targetField']

    def set_mo_target_field(self, target):
        return self.set_prop('/magnetoOptic/magnet/properties/targetField', target)"""

"""
    def vent(self):
        self.call_method('/controller/methods/vent()')
    def get_sample_chamber_pressure(self):
        return self.get_prop('/vacuumSystem/vacuumGauges/sampleChamberPressure/properties/pressureSample')['pressureSample']['pressure']

    def set_platform_bakeout_enabled(self, enabled):
        return self.set_prop('/controller/properties/platformBakeoutEnabled', enabled)

    def set_platform_bakeout_temperature(self, temperature):
        return self.set_prop('/controller/properties/platformBakeoutTemperature', temperature)

    def set_platform_bakeout_time(self, duration):
        return self.set_prop('/controller/properties/platformBakeoutTime', duration)

    def set_dry_nitrogen_purge_enabled(self, enabled):
        return self.set_prop('/controller/properties/dryNitrogenPurgeEnabled', enabled)

    def set_dry_nitrogen_purge_num_times(self, times):
        return self.set_prop('/controller/properties/dryNitrogenPurgeNumTimes', times)

    #
    # Pull Vacuum methods
    #
    def set_pull_vacuum_target_pressure(self, target):
        return self.set_prop('/controller/properties/pullVacuumTargetPressure', target)


    #
    # Stage1 methods
    #
    def get_stage1_temperature_sample(self):
        r = self.get_prop('/cooler/temperatureControllers/stage1/thermometer/properties/sample')
        return r['sample']

    def get_stage1_temperature(self):
        r = self.get_prop('/cooler/temperatureControllers/stage1/thermometer/properties/sample')
        return r['sample']['temperatureOK'], r['sample']['temperature']

    #
    # Stage2 methods
    #
    def get_stage2_temperature_sample(self):
        r = self.get_prop('/cooler/temperatureControllers/stage2/thermometer/properties/sample')
        return r['sample']

    def get_stage2_temperature(self):
        r = self.get_prop('/cooler/temperatureControllers/stage2/thermometer/properties/sample')
        return r['sample']['temperatureOK'], r['sample']['temperature']
    
    #
    # Platform methods
    #

    def set_platform_stability_target(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/platform/thermometer/properties/stabilityTarget', target)
    
    def get_platform_temperature_stable(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/platform/thermometer/properties/sample')
        return r['sample']['temperatureStabilityOK'], r['sample']['temperatureStable']

    def get_platform_temperature_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/platform/thermometer/properties/sample')
        return r['sample']

    def get_platform_heater_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/platform/heater/properties/sample')
        return r['sample']

    #
    # User1 methods
    #

    def get_sample_temperature_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user1/thermometer/properties/sample')
        return r['sample']

    def set_sample_stability_target(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/user1/thermometer/properties/stabilityTarget', target)

    def get_sample_temperature_stable(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user1/thermometer/properties/sample')
        return r['sample']['temperatureStabilityOK'], r['sample']['temperatureStable']    

    def set_sample_temperature_controller_enabled(self, enabled):
        return self.set_prop('/sampleChamber/temperatureControllers/user1/properties/controllerEnabled', enabled)

    def set_sample_temperature(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/user1/properties/targetTemperature', target)

    def get_sample_heater_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user1/heater/properties/sample')
        return r['sample']
    #
    # Vent methods
    #
    def set_vent_continuously_enabled(self, enabled):
        return self.set_prop('/controller/properties/ventContinuouslyEnabled', enabled)
    #
    # User2 methods
    #
    def get_user2_temperature_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user2/thermometer/properties/sample')
        return r['sample']

    def get_user2_temperature(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user2/thermometer/properties/sample')
        return r['sample']['temperatureOK'], r['sample']['temperature']

    def get_user2_temperature_stability(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user2/thermometer/properties/sample')
        return r['sample']['temperatureStabilityOK'], r['sample']['temperatureStability']

    def set_user2_stability_target(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/user2/thermometer/properties/stabilityTarget', target)

    def get_user2_temperature_stable(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user2/thermometer/properties/sample')
        return r['sample']['temperatureStabilityOK'], r['sample']['temperatureStable']

    def set_user2_temperature_controller_enabled(self, enabled):
        return self.set_prop('/sampleChamber/temperatureControllers/user2/properties/controllerEnabled', enabled)

    def set_user2_target_temperature(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/user2/properties/targetTemperature', target)

    def get_user2_heater_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/user2/heater/properties/sample')
        return r['sample']

    #
    # Cryo-Optic methods
    #
    def get_cryooptic_temperature_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/cryoOptic/thermometer/properties/sample')
        return r['sample']

    def get_cryooptic_temperature(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/cryoOptic/thermometer/properties/sample')
        return r['sample']['temperatureOK'], r['sample']['temperature']

    def get_cryooptic_temperature_stability(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/cryoOptic/thermometer/properties/sample')
        return r['sample']['temperatureStabilityOK'], r['sample']['temperatureStability']

    def set_cryooptic_stability_target(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/cryoOptic/thermometer/properties/stabilityTarget', target)

    def get_cryooptic_temperature_stable(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/cryoOptic/thermometer/properties/sample')
        return r['sample']['temperatureStabilityOK'], r['sample']['temperatureStable']

    def set_cryooptic_temperature_controller_enabled(self, enabled):
        return self.set_prop('/sampleChamber/temperatureControllers/cryoOptic/properties/controllerEnabled', enabled)

    def set_cryooptic_target_temperature(self, target):
        return self.set_prop('/sampleChamber/temperatureControllers/cryoOptic/properties/targetTemperature', target)

    def get_cryooptic_heater_sample(self):
        r = self.get_prop('/sampleChamber/temperatureControllers/cryoOptic/heater/properties/sample')
        return r['sample']
"""
