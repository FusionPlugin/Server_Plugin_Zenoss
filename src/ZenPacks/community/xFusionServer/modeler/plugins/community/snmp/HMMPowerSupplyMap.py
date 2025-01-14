"""
HMMPowerSupplyMap
"""
from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap, GetMap
)
from DeviceDefine import HMMSTATUS, HMMPRESENCE, HMMPOWERMODE, HMMLOCATION


class HMMPowerSupplyMap(SnmpPlugin):
    """
    HMMPowerSupplyMap
    """
    relname = 'hmmpowerSupplys'
    modname = 'ZenPacks.community.xFusionServer.HMMPowerSupply'

    snmpGetTableMaps = (
        GetTableMap(
            'hmmPowerSupplyTable', '1.3.6.1.4.1.58132.2.82.1.82.6.2001.1', {
                '.1': 'powerIndex',
                '.2': 'powerPresence',
                '.3': 'powerState',
                '.4': 'powerRatingPower',
                '.5': 'powerMode',
                '.8': 'powerRuntimePower',
            }
        ),
        GetTableMap(
            'hmmPSUTable', '1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1', {
                '.1': 'psuIndex',
                '.2': 'psuLocation',
                '.3': 'psuHealth',
            }
        ),
    )
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.1.1': 'psuIndex1',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.2.1': 'psuLocation1',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.3.1': 'psuHealth1',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.1.2': 'psuIndex2',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.2.2': 'psuLocation2',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.3.2': 'psuHealth2',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.1.3': 'psuIndex3',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.2.3': 'psuLocation3',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.3.3': 'psuHealth3',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.1.4': 'psuIndex4',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.2.4': 'psuLocation4',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.3.4': 'psuHealth4',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.1.5': 'psuIndex5',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.2.5': 'psuLocation5',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.3.5': 'psuHealth5',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.1.6': 'psuIndex6',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.2.6': 'psuLocation6',
        '.1.3.6.1.4.1.58132.2.82.1.82.100.4.2001.1.3.6': 'psuHealth6',
    })

    def process(self, device, results, log):
        """
        process oid
        """

        log = log
        device = device
        temp_sensors = results[1].get('hmmPowerSupplyTable', {})

        getdata = results[0]
        psumap = {}

        for row in range(1, 7):
            rindex = 'psuIndex%s' % str(row)
            rlocation = 'psuLocation%s' % str(row)
            rhealth = 'psuHealth%s' % str(row)
            psumap[row] = [HMMLOCATION.get(getdata.get(rlocation), ''),
                           HMMSTATUS.get(getdata.get(rhealth), 'normal')]

        relmap = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = str(row.get('powerIndex'))
            if not name:
                log.warn('Skipping hmmPSUTable with no name')
                continue
            if 1 != int(row.get('powerPresence')):
                continue

            psustatus = ''
            psulocation = ''
            # 2018-01-12 djg fixed psu[1... and powersuperly[0... in same row.
            psuidx = int(name) + 1
            if (psuidx) in psumap:
                psulocation = psumap.get(psuidx)[0]
                psustatus = psumap.get(psuidx)[1]

            relmap.append(self.objectMap({
                'id': self.prepId('PS_' + name),
                'title': 'PS_' + name,
                'snmpindex': snmpindex.strip('.'),
                'hpspresence': HMMPRESENCE.get(row.get('powerPresence'),
                                               'unknown'),
                'hpsratingPower': row.get('powerRatingPower'),
                'hpsruntimePower': row.get('powerRuntimePower'),
                'hpsstatus': psustatus,
                'hpslocation': psulocation,
                'hpspowerMode': HMMPOWERMODE.get(
                    row.get('powerMode'), row.get('powerMode')),
            }))

        return relmap
