"""
Static assignments for testing the Jupiter system.
"""
dag=['localpro',
 {'aggregate0': ['1',
                 'true',
                 'simpledetector0',
                 'astutedetector0',
                 'dftdetector0',
                 'teradetector0'],
  'aggregate1': ['1',
                 'true',
                 'simpledetector1',
                 'astutedetector1',
                 'dftdetector1',
                 'teradetector1'],
  'aggregate2': ['1',
                 'true',
                 'simpledetector2',
                 'astutedetector2',
                 'dftdetector2',
                 'teradetector2'],
  'astutedetector0': ['1', 'true', 'fusioncenter0'],
  'astutedetector1': ['1', 'true', 'fusioncenter1'],
  'astutedetector2': ['1', 'true', 'fusioncenter2'],
  'dftdetector0': ['1',
                   'true',
                   'fusioncenter0',
                   'dftslave00',
                   'dftslave01',
                   'dftslave02'],
  'dftdetector1': ['1',
                   'true',
                   'fusioncenter1',
                   'dftslave10',
                   'dftslave11',
                   'dftslave12'],
  'dftdetector2': ['1',
                   'true',
                   'fusioncenter2',
                   'dftslave20',
                   'dftslave21',
                   'dftslave22'],
  'dftslave00': ['1', 'false', 'dftslave00'],
  'dftslave01': ['1', 'false', 'dftslave01'],
  'dftslave02': ['1', 'false', 'dftslave02'],
  'dftslave10': ['1', 'false', 'dftslave10'],
  'dftslave11': ['1', 'false', 'dftslave11'],
  'dftslave12': ['1', 'false', 'dftslave12'],
  'dftslave20': ['1', 'false', 'dftslave20'],
  'dftslave21': ['1', 'false', 'dftslave21'],
  'dftslave22': ['1', 'false', 'dftslave22'],
  'fusioncenter0': ['4', 'true', 'globalfusion'],
  'fusioncenter1': ['4', 'true', 'globalfusion'],
  'fusioncenter2': ['4', 'true', 'globalfusion'],
  'globalfusion': ['3', 'true', 'home'],
  'localpro': ['1', 'false', 'aggregate0', 'aggregate1', 'aggregate2'],
  'simpledetector0': ['1', 'true', 'fusioncenter0'],
  'simpledetector1': ['1', 'true', 'fusioncenter1'],
  'simpledetector2': ['1', 'true', 'fusioncenter2'],
  'teradetector0': ['1', 'true', 'fusioncenter0', 'teramaster0'],
  'teradetector1': ['1', 'true', 'fusioncenter1', 'teramaster1'],
  'teradetector2': ['1', 'true', 'fusioncenter2', 'teramaster2'],
  'teramaster0': ['1', 'false', 'teraworker00', 'teraworker01', 'teraworker02'],
  'teramaster1': ['1', 'false', 'teraworker10', 'teraworker11', 'teraworker12'],
  'teramaster2': ['1', 'false', 'teraworker20', 'teraworker21', 'teraworker22'],
  'teraworker00': ['1', 'false', 'teraworker00'],
  'teraworker01': ['1', 'false', 'teraworker01'],
  'teraworker02': ['1', 'false', 'teraworker02'],
  'teraworker10': ['1', 'false', 'teraworker10'],
  'teraworker11': ['1', 'false', 'teraworker11'],
  'teraworker12': ['1', 'false', 'teraworker12'],
  'teraworker20': ['1', 'false', 'teraworker20'],
  'teraworker21': ['1', 'false', 'teraworker21'],
  'teraworker22': ['1', 'false', 'teraworker22']},
 {'aggregate0': 'node27',
  'aggregate1': 'node39',
  'aggregate2': 'node24',
  'astutedetector0': 'node23',
  'astutedetector1': 'node31',
  'astutedetector2': 'node42',
  'dftdetector0': 'node28',
  'dftdetector1': 'node14',
  'dftdetector2': 'node25',
  'dftslave00': 'node34',
  'dftslave01': 'node12',
  'dftslave02': 'node21',
  'dftslave10': 'node44',
  'dftslave11': 'node20',
  'dftslave12': 'node23',
  'dftslave20': 'node29',
  'dftslave21': 'node43',
  'dftslave22': 'node18',
  'fusioncenter0': 'node40',
  'fusioncenter1': 'node11',
  'fusioncenter2': 'node35',
  'globalfusion': 'node6',
  'localpro': 'node4',
  'simpledetector0': 'node21',
  'simpledetector1': 'node34',
  'simpledetector2': 'node32',
  'teradetector0': 'node14',
  'teradetector1': 'node23',
  'teradetector2': 'node31',
  'teramaster0': 'node3',
  'teramaster1': 'node11',
  'teramaster2': 'node33',
  'teraworker00': 'node39',
  'teraworker01': 'node39',
  'teraworker02': 'node22',
  'teraworker10': 'node27',
  'teraworker11': 'node35',
  'teraworker12': 'node15',
  'teraworker20': 'node41',
  'teraworker21': 'node15',
  'teraworker22': 'node10'}]
schedule=['localpro',
 {'aggregate0': ['1',
                 'true',
                 'simpledetector0',
                 'astutedetector0',
                 'dftdetector0',
                 'teradetector0'],
  'aggregate1': ['1',
                 'true',
                 'simpledetector1',
                 'astutedetector1',
                 'dftdetector1',
                 'teradetector1'],
  'aggregate2': ['1',
                 'true',
                 'simpledetector2',
                 'astutedetector2',
                 'dftdetector2',
                 'teradetector2'],
  'astutedetector0': ['1', 'true', 'fusioncenter0'],
  'astutedetector1': ['1', 'true', 'fusioncenter1'],
  'astutedetector2': ['1', 'true', 'fusioncenter2'],
  'dftdetector0': ['1',
                   'true',
                   'fusioncenter0',
                   'dftslave00',
                   'dftslave01',
                   'dftslave02'],
  'dftdetector1': ['1',
                   'true',
                   'fusioncenter1',
                   'dftslave10',
                   'dftslave11',
                   'dftslave12'],
  'dftdetector2': ['1',
                   'true',
                   'fusioncenter2',
                   'dftslave20',
                   'dftslave21',
                   'dftslave22'],
  'dftslave00': ['1', 'false', 'dftslave00'],
  'dftslave01': ['1', 'false', 'dftslave01'],
  'dftslave02': ['1', 'false', 'dftslave02'],
  'dftslave10': ['1', 'false', 'dftslave10'],
  'dftslave11': ['1', 'false', 'dftslave11'],
  'dftslave12': ['1', 'false', 'dftslave12'],
  'dftslave20': ['1', 'false', 'dftslave20'],
  'dftslave21': ['1', 'false', 'dftslave21'],
  'dftslave22': ['1', 'false', 'dftslave22'],
  'fusioncenter0': ['4', 'true', 'globalfusion'],
  'fusioncenter1': ['4', 'true', 'globalfusion'],
  'fusioncenter2': ['4', 'true', 'globalfusion'],
  'globalfusion': ['3', 'true', 'home'],
  'localpro': ['1', 'false', 'aggregate0', 'aggregate1', 'aggregate2'],
  'simpledetector0': ['1', 'true', 'fusioncenter0'],
  'simpledetector1': ['1', 'true', 'fusioncenter1'],
  'simpledetector2': ['1', 'true', 'fusioncenter2'],
  'teradetector0': ['1', 'true', 'fusioncenter0', 'teramaster0'],
  'teradetector1': ['1', 'true', 'fusioncenter1', 'teramaster1'],
  'teradetector2': ['1', 'true', 'fusioncenter2', 'teramaster2'],
  'teramaster0': ['1', 'false', 'teraworker00', 'teraworker01', 'teraworker02'],
  'teramaster1': ['1', 'false', 'teraworker10', 'teraworker11', 'teraworker12'],
  'teramaster2': ['1', 'false', 'teraworker20', 'teraworker21', 'teraworker22'],
  'teraworker00': ['1', 'false', 'teraworker00'],
  'teraworker01': ['1', 'false', 'teraworker01'],
  'teraworker02': ['1', 'false', 'teraworker02'],
  'teraworker10': ['1', 'false', 'teraworker10'],
  'teraworker11': ['1', 'false', 'teraworker11'],
  'teraworker12': ['1', 'false', 'teraworker12'],
  'teraworker20': ['1', 'false', 'teraworker20'],
  'teraworker21': ['1', 'false', 'teraworker21'],
  'teraworker22': ['1', 'false', 'teraworker22']},
 {'aggregate0': ['aggregate0', 'rpi27', 'root', 'PASSWORD'],
  'aggregate1': ['aggregate1', 'rpi39', 'root', 'PASSWORD'],
  'aggregate2': ['aggregate2', 'rpi24', 'root', 'PASSWORD'],
  'astutedetector0': ['astutedetector0', 'rpi23', 'root', 'PASSWORD'],
  'astutedetector1': ['astutedetector1', 'rpi31', 'root', 'PASSWORD'],
  'astutedetector2': ['astutedetector2', 'rpi42', 'root', 'PASSWORD'],
  'dftdetector0': ['dftdetector0', 'rpi28', 'root', 'PASSWORD'],
  'dftdetector1': ['dftdetector1', 'rpi14', 'root', 'PASSWORD'],
  'dftdetector2': ['dftdetector2', 'rpi25', 'root', 'PASSWORD'],
  'dftslave00': ['dftslave00', 'rpi34', 'root', 'PASSWORD'],
  'dftslave01': ['dftslave01', 'rpi12', 'root', 'PASSWORD'],
  'dftslave02': ['dftslave02', 'rpi21', 'root', 'PASSWORD'],
  'dftslave10': ['dftslave10', 'rpi44', 'root', 'PASSWORD'],
  'dftslave11': ['dftslave11', 'rpi20', 'root', 'PASSWORD'],
  'dftslave12': ['dftslave12', 'rpi23', 'root', 'PASSWORD'],
  'dftslave20': ['dftslave20', 'rpi29', 'root', 'PASSWORD'],
  'dftslave21': ['dftslave21', 'rpi43', 'root', 'PASSWORD'],
  'dftslave22': ['dftslave22', 'rpi18', 'root', 'PASSWORD'],
  'fusioncenter0': ['fusioncenter0', 'rpi40', 'root', 'PASSWORD'],
  'fusioncenter1': ['fusioncenter1', 'rpi11', 'root', 'PASSWORD'],
  'fusioncenter2': ['fusioncenter2', 'rpi35', 'root', 'PASSWORD'],
  'globalfusion': ['globalfusion', 'rpi6', 'root', 'PASSWORD'],
  'home': ['home', 'rpi1', 'root', 'PASSWORD'],
  'localpro': ['localpro', 'rpi4', 'root', 'PASSWORD'],
  'simpledetector0': ['simpledetector0', 'rpi21', 'root', 'PASSWORD'],
  'simpledetector1': ['simpledetector1', 'rpi34', 'root', 'PASSWORD'],
  'simpledetector2': ['simpledetector2', 'rpi32', 'root', 'PASSWORD'],
  'teradetector0': ['teradetector0', 'rpi14', 'root', 'PASSWORD'],
  'teradetector1': ['teradetector1', 'rpi23', 'root', 'PASSWORD'],
  'teradetector2': ['teradetector2', 'rpi31', 'root', 'PASSWORD'],
  'teramaster0': ['teramaster0', 'rpi3', 'root', 'PASSWORD'],
  'teramaster1': ['teramaster1', 'rpi11', 'root', 'PASSWORD'],
  'teramaster2': ['teramaster2', 'rpi33', 'root', 'PASSWORD'],
  'teraworker00': ['teraworker00', 'rpi39', 'root', 'PASSWORD'],
  'teraworker01': ['teraworker01', 'rpi39', 'root', 'PASSWORD'],
  'teraworker02': ['teraworker02', 'rpi22', 'root', 'PASSWORD'],
  'teraworker10': ['teraworker10', 'rpi27', 'root', 'PASSWORD'],
  'teraworker11': ['teraworker11', 'rpi35', 'root', 'PASSWORD'],
  'teraworker12': ['teraworker12', 'rpi15', 'root', 'PASSWORD'],
  'teraworker20': ['teraworker20', 'rpi41', 'root', 'PASSWORD'],
  'teraworker21': ['teraworker21', 'rpi15', 'root', 'PASSWORD'],
  'teraworker22': ['teraworker22', 'rpi10', 'root', 'PASSWORD']}]