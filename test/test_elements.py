import unittest
import xml.etree.ElementTree as ET

import pysvd


class TestElementDevice(unittest.TestCase):

    def test_exception(self):
        xml = '''<device />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Device(node)

    def test_attributes(self):
        xml = '''
        <device schemaVersion="1.3" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd">
            <vendor>ARM Ltd.</vendor>
            <vendorID>ARM</vendorID>
            <name>ARM_Cortex_M4</name>
            <series>ARMCM4</series>
            <version>0.1</version>
            <description>Arm Cortex-M4 based Microcontroller demonstration device</description>
            <licenseText>
                Arm Limited (Arm) is supplying this software for use with Cortex-M \n
                processor based microcontrollers.  This file can be freely distributed \n
                within development tools that are supporting such Arm based processors. \n
                \n
                THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED \n
                OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF \n
                MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. \n
                ARM SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR \n
                CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
            </licenseText>

            <headerSystemFilename>system_ARMCM4</headerSystemFilename>
            <headerDefinitionsPrefix>ARM_</headerDefinitionsPrefix>
            <addressUnitBits>8</addressUnitBits>
            <width>32</width>
            <size>32</size>
            <access>read-write</access>
            <resetValue>0</resetValue>
            <resetMask>0xffffffff</resetMask>
            <peripherals>

            </peripherals>
        </device>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Device(node)

        self.assertEqual(test.schema_version, '1.3')

        self.assertEqual(test.vendor, 'ARM Ltd.')
        self.assertEqual(test.vendor_id, 'ARM')
        self.assertEqual(test.name, 'ARM_Cortex_M4')
        self.assertEqual(test.series, 'ARMCM4')
        self.assertEqual(test.version, '0.1')
        self.assertEqual(test.description, 'Arm Cortex-M4 based Microcontroller demonstration device')
        self.assertEqual(test.header_system_filename, 'system_ARMCM4')
        self.assertEqual(test.header_definitions_prefix, 'ARM_')
        self.assertEqual(test.address_unit_bits, 8)
        self.assertEqual(test.width, 32)

        self.assertEqual(test.size, 32)
        self.assertEqual(test.access, pysvd.type.access.read_write)
        self.assertEqual(test.reset_value, 0)
        self.assertEqual(test.reset_mask, 0xffffffff)

        self.assertEqual(len(test.peripheral), 0)


class TestElementCpu(unittest.TestCase):

    def test_exception(self):
        xml = '''<cpu />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Cpu(None, node)

    def test_attributes(self):
        xml = '''
        <cpu>
            <name>CM7</name>
            <revision>r0p0</revision>
            <endian>little</endian>
            <mpuPresent>true</mpuPresent>

        <!-- has double precision FPU -->
            <fpuPresent>true</fpuPresent>
            <fpuDP>true</fpuDP>

        <!-- has instruction and data cache -->
            <icachePresent>true</icachePresent>
            <dcachePresent>true</dcachePresent>

        <!-- has no instruction nor data tighly coupled memory -->
            <itcmPresent>false</itcmPresent>
            <dtcmPresent>false</dtcmPresent>
            <nvicPrioBits>4</nvicPrioBits>
            <vendorSystickConfig>false</vendorSystickConfig>
        </cpu>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Cpu(None, node)

        self.assertEqual(test.name, pysvd.type.cpuName.CM7)
        self.assertEqual(test.revision, "r0p0")
        self.assertEqual(test.endian, pysvd.type.endian.little)
        self.assertTrue(test.mpu_present)
        self.assertTrue(test.fpu_present)
        self.assertTrue(test.fpu_dp)
        self.assertTrue(test.icache_present)
        self.assertTrue(test.dcache_present)
        self.assertFalse(test.itcm_present)
        self.assertFalse(test.dtcm_present)
        self.assertEqual(test.nvic_prio_bits, 4)
        self.assertFalse(test.vendor_systick_config)

        self.assertTrue(test.vtor_present)

        with self.assertRaises(AttributeError):
            self.assertIsNotNone(test.sau_num_regions)


class TestElementSauRegionsConfig(unittest.TestCase):

    def test_empty(self):
        xml = '''<sauRegionsConfig />'''
        node = ET.fromstring(xml)
        test = pysvd.element.SauRegionConfig(None, node)

        self.assertEqual(len(test.region), 0)

    def test_attributes(self):
        xml = '''
        <sauRegionsConfig>
            <region name="SAU1">
                <base>0x10001000</base>
                <limit>0x10005000</limit>
                <access>n</access>
            </region>
            <region enabled="false" name="SAU2">
                <base>0x10006000</base>
                <limit>0x10008000</limit>
                <access>c</access>
            </region>
        </sauRegionsConfig>'''
        node = ET.fromstring(xml)
        test = pysvd.element.SauRegionConfig(None, node)

        self.assertEqual(len(test.region), 2)

        self.assertTrue(test.region[0].enabled)
        self.assertEqual(test.region[0].name, 'SAU1')
        self.assertEqual(test.region[0].base, 0x10001000)
        self.assertEqual(test.region[0].limit, 0x10005000)
        self.assertEqual(test.region[0].access, pysvd.type.sauAccess.non_secure)

        self.assertFalse(test.region[1].enabled)
        self.assertEqual(test.region[1].name, 'SAU2')
        self.assertEqual(test.region[1].base, 0x10006000)
        self.assertEqual(test.region[1].limit, 0x10008000)
        self.assertEqual(test.region[1].access, pysvd.type.sauAccess.non_secure_callable_secure)


class TestElementSauRegionsConfigRegion(unittest.TestCase):

    def test_exception(self):
        xml = '''<region />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.SauRegionsConfigRegion(None, node)

    def test_attributes(self):
        xml = '''
        <region enabled="false" name="SAU2">
            <base>0x10006000</base>
            <limit>0x10008000</limit>
            <access>c</access>
        </region>'''
        node = ET.fromstring(xml)
        test = pysvd.element.SauRegionsConfigRegion(None, node)

        self.assertEqual(test.base, 0x10006000)
        self.assertEqual(test.limit, 0x10008000)
        self.assertEqual(test.access, pysvd.type.sauAccess.non_secure_callable_secure)

        self.assertEqual(test.name, "SAU2")
        self.assertFalse(test.enabled)


class TestElementAddressBlock(unittest.TestCase):

    def test_exception(self):
        xml = '''<addressBlock />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.AddressBlock(None, node)

    def test_attributes(self):
        xml = '''
        <addressBlock>
            <offset>0x0</offset>
            <size>0x400</size>
            <usage>registers</usage>
            <protection>s</protection>
        </addressBlock>'''
        node = ET.fromstring(xml)
        test = pysvd.element.AddressBlock(None, node)

        self.assertEqual(test.offset, 0)
        self.assertEqual(test.size, 0x400)
        self.assertEqual(test.usage, pysvd.type.usage.registers)
        self.assertEqual(test.protection, pysvd.type.protection.secure)


class TestElementInterrupt(unittest.TestCase):

    def test_exception(self):
        xml = '''<interrupt />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.Interrupt(None, node)

    def test_attributes(self):
        xml = '''
        <interrupt>
            <name>TIM0_INT</name>
            <value>34</value>
            <description>Timer0 Interrupt</description>
        </interrupt>'''
        node = ET.fromstring(xml)
        test = pysvd.element.Interrupt(None, node)

        self.assertEqual(test.name, 'TIM0_INT')
        self.assertEqual(test.description, 'Timer0 Interrupt')
        self.assertEqual(test.value, 34)


class TestElementEnumberatedValues(unittest.TestCase):

    def test_exception(self):
        xml = '''<enumeratedValues />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.EnumeratedValues(None, node)

    def test_minimal(self):
        xml = '''
        <enumeratedValues>
            <enumeratedValue>
                <value>0</value>
            </enumeratedValue>
        </enumeratedValues>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValues(None, node)

        self.assertEqual(test.usage, pysvd.type.enumUsage.read_write)
        self.assertEqual(len(test.enumerated_value), 1)

        self.assertEqual(test.enumerated_value[0].value, 0)

    def test_attributes(self):
        xml = '''
        <enumeratedValues>
            <name>TimerIntSelect</name>
            <headerEnumName>TimerIntSelectEnum</headerEnumName>
            <usage>read-write</usage>
            <enumeratedValue>
                <name>disabled</name>
                <description>The clock source clk0 is turned off.</description>
                <value>0</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>enabled</name>
                <description>The clock source clk1 is running.</description>
                <value>1</value>
            </enumeratedValue>
            <enumeratedValue>
                <name>reserved</name>
                <description>Reserved values. Do not use.</description>
                <isDefault>true</isDefault>
            </enumeratedValue>
        </enumeratedValues>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValues(None, node)

        self.assertEqual(test.name, "TimerIntSelect")
        self.assertEqual(test.header_enum_name, "TimerIntSelectEnum")
        self.assertEqual(test.usage, pysvd.type.enumUsage.read_write)
        self.assertEqual(len(test.enumerated_value), 3)

        self.assertEqual(test.enumerated_value[0].name, "disabled")
        self.assertEqual(test.enumerated_value[0].description, "The clock source clk0 is turned off.")
        self.assertEqual(test.enumerated_value[0].value, 0)

        self.assertEqual(test.enumerated_value[1].name, "enabled")
        self.assertEqual(test.enumerated_value[1].description, "The clock source clk1 is running.")
        self.assertEqual(test.enumerated_value[1].value, 1)

        self.assertEqual(test.enumerated_value[2].name, "reserved")
        self.assertEqual(test.enumerated_value[2].description, "Reserved values. Do not use.")
        self.assertTrue(test.enumerated_value[2].is_default)

    def test_derived(self):
        self.assertTrue(True)


class TestElementEnumberatedValue(unittest.TestCase):

    def test_exception(self):
        xml = '''<enumeratedValue />'''
        node = ET.fromstring(xml)
        with self.assertRaises(SyntaxError):
            pysvd.element.EnumeratedValue(None, node)

    def test_minimal(self):
        xml = '''
        <enumeratedValue>
            <value>0</value>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValue(None, node)

        self.assertEqual(test.value, 0)

    def test_attributes_value(self):
        xml = '''
        <enumeratedValue>
            <name>disabled</name>
            <description>The clock source clk0 is turned off.</description>
            <value>0</value>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValue(None, node)

        self.assertEqual(test.name, "disabled")
        self.assertEqual(test.description, "The clock source clk0 is turned off.")
        self.assertEqual(test.value, 0)

        with self.assertRaises(AttributeError):
            self.assertIsNone(test.is_default)

    def test_attributes_is_default(self):
        xml = '''
        <enumeratedValue>
            <name>reserved</name>
            <description>Reserved values. Do not use.</description>
            <isDefault>true</isDefault>
        </enumeratedValue>'''

        node = ET.fromstring(xml)
        test = pysvd.element.EnumeratedValue(None, node)

        self.assertEqual(test.name, "reserved")
        self.assertEqual(test.description, "Reserved values. Do not use.")
        self.assertTrue(test.is_default)

        with self.assertRaises(AttributeError):
            self.assertIsNone(test.value)
