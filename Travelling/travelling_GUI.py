'''
TRAVELLING - a data printable file creator based on input values

I valori delle chiavi hanno un significato basato sulla posizione:
    - 0 = valore
    - 1 = unità di misura
    - 2 = formula di ricavo del valore (se è None, è un dato di input)
    - 3 = posizione nel file Excel
'''
# LIBRERIE ----------------------------------------------------------------------
import math
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os, shutil, sys
from tkinter import *
from tkinter import filedialog

# VARIABILI ----------------------------------------------------------------------
n_riga = 1 # per la GUI
i = 0
data_corrente = ''
entry_fields = [] # lista di oggetti Entry
input_list = [] # lista di valori float da inserire nella struttura

cs = ': '
E15 = 'Machine dead load'
E16 = 'Tripper / trailer dead load'
E17 = 'Live loads on machine'
E18 = 'Live loads on tripper / trailer'
E20 = 'Dead load and live load'
E21 = 'Dead load'
E22 = 'Operating wind speed'
E23 = 'Max wind speed for travelling to parking position'
E24 = 'Out of service wind'
E25 = 'Equivalent pressure to v1'
E26 = 'Equivalent pressure to v2'
E27 = 'Equivalent pressure to v3'
E28 = 'Max operating speed'
E29 = 'Max travel speed'
E30 = 'Max travel, with max travel wind'
E31 = 'Shape coefficient (according to ISO 5049)'
E32 = 'Rolling friction factor'
E33 = 'Static friction factor'
E34 = 'Fictitious friction factor'
E35 = 'Friction factor to grip limit'
E36 = 'Rail slope'
E37 = 'Belt\'s lenght on tripper'
E38 = 'Lifting height on tripper'
E39 = 'Max wind area during normal operation'
E40 = 'Min wind area during traveling to parking'
E41 = 'Tripper carrying rollers weight (single roller)'
E42 = 'Tripper carrying rollers pitch'
E43 = 'Tripper carrying rollers quantity for each station'
E44 = 'Tripper return rollers weight (single roller)'
E45 = 'Tripper return rollers pitch'
E46 = 'Tripper return rollers quantity for each station'
E47 = 'Idlers weight'
E48 = 'Belt weight'
E49 = 'Tripper capacity'
E50 = 'Tripper conveyor speed'
E51 = 'Material density'
E52 = 'Material weight'
E53 = 'Mechanical efficency'
E54 = 'Acceleration time to max speed'
E55 = 'Acceleration to max speed'
E56 = 'High speed rotating parts inertia'
E58 = 'Wheel and shaft inertia'
E59 = 'Motor, clutch and gear box inertia'

t_A61 = 'Friction force on rail'
E62F62 = t_A61 + cs + 'during normal operation, travelling at c1'
E63F63 = t_A61 + cs + 'during travelling at c2'

t_A65 = 'Wind force'
E66F66 = t_A65 + cs + 'max during normal operation (v1), travelling at c1'
E67F67 = t_A65 + cs + 'during travelling to parking position (v2), travelling at c2'
E68 = t_A65 + cs + 'during storm wind, out of service (v3), static condition'

t_A70 = 'Force due to yard slope'
E71F71 = t_A70 + cs + 'during normal operation, travelling at c1'
E72F72 = t_A70 + cs + 'during travelling at c2'

E75F75 = 'Force for lifting material on tripper travelling at c1'
E78F78 = 'Friction force due to material on tripper travelling at c1'
E81F81 = 'Friction force due to tripper idlers and belt travelling at c1'

t_A83 = 'Force due to material digging'
E84F84 = t_A83 + cs + 'normal lateral digging force travelling at c1'
E85F85 = t_A83 + cs + 'abnormal lateral digging force travelling at c1'

E88F88 = 'Acceleration force'

t_A90 = 'Load combinations'
E92F92G92H92 = t_A90 + cs + 'normal operation - stacking'
E93F93G93H93 = t_A90 + cs + 'normal operation acceleration - stacking'
E94F94G94H94 = t_A90 + cs + 'normal operation - reclaiming'
E95F95G95H95 = t_A90 + cs + 'normal operation accelaration - reclaiming'
E96F96G96H96 = t_A90 + cs + 'abnormal operation - reclaiming'
E97F97G97H97 = t_A90 + cs + 'travelling to parking position with max wind'
H98 = t_A90 + cs + 'Total percentage'

D99 = 'RMS power'
D100 = 'Min power'
D101 = 'Max power'

t_A103 = 'Installed power'
D105 = t_A103 + cs + 'number of drive units'
D106 = t_A103 + cs + 'power of each unit'
D107 = t_A103 + cs + 'motor torque'
D109 = t_A103 + cs + 'total installed power'
F109 = t_A103 + cs + 'VALUE_CHECK_F109'
D110 = t_A103 + cs + 'total motor torque'
D111 = t_A103 + cs + 'ratio of installed power vs max absorbed power'
D112 = t_A103 + cs + 'ratio of installed power vs RMS absorbed power'
F112 = t_A103 + cs + 'VALUE_CHECK_F112'

t_A114 = 'Reduction gear'
D115 = t_A114 + cs + 'service factor'
D116 = t_A114 + cs + 'wheel diameter'
D117 = t_A114 + cs + 'max travel speed'
D118 = t_A114 + cs + 'motor speed'
D119 = t_A114 + cs + 'wheel speed'
D120 = t_A114 + cs + 'prereduction gear'
D121 = t_A114 + cs + 'nominal power'
D122 = t_A114 + cs + 'reduction ratio'
D123 = t_A114 + cs + 'nominal torque'

t_A125 = 'Torque verification against wheel slipping'
D127 = t_A125 + cs + 'wheel diameter'
D128 = t_A125 + cs + 'min load on each wheel (min operating load in FEM II condition)'
D129 = t_A125 + cs + 'min load on each wheel in kN'
D130 = t_A125 + cs + 'starting factor'
D131 = t_A125 + cs + 'nominal motor torque'
D132 = t_A125 + cs + 'reduction ratio'
D133 = t_A125 + cs + 'min traction force'
D134 = t_A125 + cs + 'max allowed torque'
D135 = t_A125 + cs + 'number of motorized wheel for each motor'
D136 = t_A125 + cs + 'max wheel torque'
F136 = t_A125 + cs + 'VALUE_CHECK_F136'
D137 = t_A125 + cs + 'total number of driven wheel'
D138 = t_A125 + cs + 'total number of wheel (for machine)'

t_A142 = 'Long travel brakes'
E143 = t_A142 + cs + 'equivalent mass of motor'
E144 = t_A142 + cs + 'equivalent mass of wheels'
E145 = t_A142 + cs + 'equivalent mass of drives'

D147 = 'Rated brake torque setting'
D149 = 'Total brake force against witch the brake shall act during operation'
D150 = 'Total brake force against witch the brake shall act during relocation'

t_A152 = 'Braking forces with all drives installed, rolling friction'
D155 = t_A152 + ' ' + 'assuming straight travelling, considering dead loading and encrustation'
D156 = t_A152 + cs + 'braking torque per drive unit'
D157 = t_A152 + cs + 'braking force per drive unit'
D158 = t_A152 + cs + 'total braking force per machine'
D159 = t_A152 + cs + 'max traction under DL + LL'
D160 = t_A152 + cs + 'total braking and friction force'

D162 = 'Brake quotlent'
F162 = 'VALUE_CHECK_F162'

t_A165 = 'Stopping distance'
D167 = t_A165 + cs + 'net deceleration force'
D168 = t_A165 + cs + 'deleleration'
D169 = t_A165 + cs + 'acceleration'
D170 = t_A165 + cs + 'stopping time at c2 speed'
D171 = t_A165 + cs + 'stopping distance'

t_A173 = 'Braking forces, no wind load, emergency stop'
D175 = t_A173 + cs + 'net deceleration force'
D176 = t_A173 + cs + 'Deleleration'
D177 = t_A173 + cs + 'Acceleration'
D178 = t_A173 + cs + 'Stopping time at c2 speed'
D179 = t_A173 + cs + 'Stopping distance'

t_A181 = 'Braking design deceleration time during relocation (v2 wind speed)'
D182 = t_A181 + cs + 'design deceleration time'
D183 = t_A181 + cs + 'Design acceleration at c2 speed'
D184 = t_A181 + cs + 'Net force'
D185 = t_A181 + cs + 'Total braking force considering the slope'
D186 = t_A181 + cs + 'Stopping distance, total braking force considering the slope'
D187 = t_A181 + cs + 'Minimum required torque per brake'

t_A190 = 'Rail clamps'
D192 = t_A190 + cs + 'storm wind and slope force'
D193 = t_A190 + cs + 'total braking force per machine with 2/3 of brakes in function'
D194 = t_A190 + cs + 'max force for each rail clamp with 2/3 of brakes in function'
D195 = t_A190 + cs + 'number of rail clamps'
D196 = t_A190 + cs + 'load of each rail clamp'

titoli = [[t_A61 + cs, False], [t_A65 + cs, False],  [t_A70 + cs, False], [t_A83 + cs, False],
          [t_A90 + cs, False], [t_A103 + cs, False], [t_A114 + cs, False], [t_A125 + cs, False],
          [t_A142 + cs, False], [t_A152 + cs, False], [t_A165 + cs, False], [t_A173 + cs, False],
          [t_A181 + cs, False], [t_A190 + cs, False]]

data = \
{
    E15: [None, 't', None, 'E15'],
    E16: [None, 't', None, 'E16'],
    E17: [None, 't', None, 'E17'],
    E18: [None, 't', None, 'E18'],
    E20: [None, 't',
          'data[E15][0] + data[E16][0] + '
          'data[E17][0] + data[E18][0]',
         'E20'],
    E21: [None, 't',
          'data[E15][0] + '
          'data[E16][0]',
         'E21'],
    E22: [None, 'km/h', None, 'E22'],
    E23: [None, 'km/h', None, 'E23'],
    E24: [None, 'km/h', None, 'E24'],
    E25: [None, 'N/m²',
          '(data[E22][0]/3.6)**2/16*9.81',
         'E25'],
    E26: [None, 'N/m²',
          '(data[E23][0]/3.6)**2/16*9.81',
         'E26'],
    E27: [None, 'N/m²',
          '(data[E24][0]/3.6)**2/16*9.81',
         'E27'],

    E28: [None, 'm/min', None, 'E28'],
    E29: [None, 'm/min', None, 'E29'],
    E30: [None, 'm/min', None, 'E30'],
    E31: [None, '', None, 'E31'],
    E32: [None, '', None, 'E32'],
    E33: [None, '', None, 'E33'],
    E34: [None, '', None, 'E34'],
    E35: [None, '', None, 'E35'],
    E36: [None, '%', None, 'E36'],
    E37: [None, 'm', None, 'E37'],
    E38: [None, 'm', None, 'E38'],
    E39: [None, 'm²', None, 'E39'],
    E40: [None, 'm²', None, 'E40'],
    E41: [None, 'kg', None, 'E41'],
    E42: [None, 'm', None, 'E42'],
    E43: [None, '', None, 'E43'],
    E44: [None, 'kg', None, 'E44'],
    E45: [None, 'm', None, 'E45'],
    E46: [None, '', None, 'E46'],
    E47: [None, 'kg/m',
         'data[E41][0] * data[E43][0] / data[E42][0] + '
         'data[E44][0] * data[E46][0] / data[E45][0]',
         'E47'],
    E48: [None, 'kg/m', None, 'E48'],
    E49: [None, 't/h', None, 'E49'],
    E50: [None, 'm/s', None, 'E50'],
    E51: [None, 't/m³', None, 'E51'],
    E52: [None, 'kg/m',
           'data[E49][0] / 3.6 / data[E51][0] / data[E50][0]',
         'E52'],
    E53: [None, '', None, 'E53'],
    E54: [None, 's', None, 'E54'],
    E55: [None, 'm/s²',
           'data[E29][0] / 60 / data[E54][0]',
         'E55'],
    E56: [None, 'kg m²', None, 'E56'],
    E58: [None, 'kg m²', None, 'E58'],
    E59: [None, 'kg m²', None, 'E59'],

    E62F62: [[None, None], ['kN', 'kW'],
            ['9.81 * data[E20][0] * data[E32][0]',
             'data[E62F62][0][0] * data[E28][0] / 60 / data[E53][0]'],
            ['E62', 'F62']],
    E63F63: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E21][0] * data[E32][0]',
              'data[E63F63][0][0] * data[E29][0] / 60 / data[E53][0]'],
             ['E63', 'F63']],

    E66F66: [[None, None], ['kN', 'kW'],
             ['data[E31][0] * data[E25][0] * data[E39][0] / 1000',
              'data[E66F66][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E66', 'F66']],
    E67F67: [[None, None], ['kN', 'kW'],
             ['data[E31][0] * data[E26][0] * data[E40][0] / 1000',
              'data[E67F67][0][0] * data[E30][0] / 60 / data[E53][0]'],
             ['E67', 'F67']],
    E68: [None, 'kN',
          'data[E31][0] * data[E27][0] * data[E40][0] / 1000',
          'E68'],

    E71F71: [[None, None], ['kN', 'kW'],
             ['data[E20][0] * (data[E36][0] / 100) * 9.81',
              'data[E71F71][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E71', 'F71']],
    E72F72: [[None, None], ['kN', 'kW'],
             ['data[E21][0] * (data[E36][0] / 100) * 9.81',
              'data[E72F72][0][0] * data[E29][0] / 60 / data[E53][0]'],
             ['E72', 'F72']],

    E75F75: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E38][0] * data[E52][0] / 1000',
              'data[E75F75][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E75', 'F75']],

    E78F78: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E52][0] * data[E37][0] * data[E34][0] / 1000',
              'data[E78F78][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E78', 'F78']],

    E81F81: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E37][0] * (data[E48][0] + data[E47][0]) * data[E34][0] / 1000',
              'data[E81F81][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E81', 'F81']],

    E84F84: [[None, None], ['kN', 'kW'],
             [None, 'data[E84F84][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E84', 'F84']],
    E85F85: [[None, None], ['kN', 'kW'],
             [None, 'data[E85F85][0][0] * data[E28][0] / 60 / data[E53][0]'],
             ['E85', 'F85']],

    E88F88: [[None, None], ['kN', 'kW'],
             ['data[E20][0] * data[E55][0]',
              '(data[E88F88][0][0] * data[E28][0] / 60) / data[E53][0]'],
             ['E88', 'F88']],

    E92F92G92H92: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E75F75][0][0] + data[E78F78][0][0] + data[E81F81][0][0]',
                    'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E75F75][0][1] + data[E78F78][0][1] + data[E81F81][0][1]',
                    'data[E92F92G92H92][0][1] / data[D105][0]',
                    None],
                    ['E92', 'F92', 'G92', 'H92']],
    E93F93G93H93: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E75F75][0][0] + data[E78F78][0][0] + data[E81F81][0][0] + data[E88F88][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E75F75][0][1] + data[E78F78][0][1] + data[E81F81][0][1] + data[E88F88][0][1]',
                   'data[E93F93G93H93][0][1] / data[D105][0]',
                   None],
                   ['E93', 'F93', 'G93', 'H93']],
    E94F94G94H94: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E84F84][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E84F84][0][1]',
                   'data[E94F94G94H94][0][1] / data[D105][0]',
                   None],
                   ['E94', 'F94', 'G94', 'H94']],
    E95F95G95H95: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E84F84][0][0] + data[E88F88][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E84F84][0][1] + data[E88F88][0][1]',
                   'data[E95F95G95H95][0][1] / data[D105][0]',
                   None],
                   ['E95', 'F95', 'G95', 'H95']],
    E96F96G96H96: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E85F85][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E85F85][0][1]',
                   'data[E96F96G96H96][0][1] / data[D105][0]',
                    None],
                   ['E96', 'F96', 'G96', 'H96']],
    E97F97G97H97: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E63F63][0][0] + data[E67F67][0][0] + data[E72F72][0][0] + data[E88F88][0][0]',
                   'data[E63F63][0][1] + data[E67F67][0][1] + data[E72F72][0][1] + data[E88F88][0][1]',
                   'data[E97F97G97H97][0][1] / data[D105][0]',
                    None],
                   ['E97', 'F97', 'G97', 'H97']],
    H98: [None, '%',
         'sum([data[E92F92G92H92][0][3], data[E93F93G93H93][0][3],'
         'data[E94F94G94H94][0][3], data[E95F95G95H95][0][3],'
         'data[E96F96G96H96][0][3], data[E97F97G97H97][0][3]])',
         'H98'],

    D99: [None, 'kW',
          'math.sqrt(((data[E92F92G92H92][0][1] ** 2 * data[E92F92G92H92][0][3] / 100) + (data[E93F93G93H93][0][1] ** 2 * data[E93F93G93H93][0][3]  / 100) + (data[E94F94G94H94][0][1] ** 2 * data[E94F94G94H94][0][3] / 100) + (data[E95F95G95H95][0][1] ** 2 * data[E95F95G95H95][0][3] / 100) + (data[E96F96G96H96][0][1] ** 2 * data[E96F96G96H96][0][3] / 100) + (data[E97F97G97H97][0][1] ** 2 * data[E97F97G97H97][0][3] / 100) / data[H98][0]))',
          'D99'],
    D100: [None, 'kW',
           'min([data[E92F92G92H92][0][1], data[E93F93G93H93][0][1],'
           'data[E94F94G94H94][0][1], data[E95F95G95H95][0][1],'
           'data[E96F96G96H96][0][1], data[E97F97G97H97][0][1]])',
           'D100'],
    D101: [None, 'kW',
           'max([data[E92F92G92H92][0][1], data[E93F93G93H93][0][1],'
           'data[E94F94G94H94][0][1], data[E95F95G95H95][0][1],'
           'data[E96F96G96H96][0][1], data[E97F97G97H97][0][1]])',
           'D101'],

    D105: [None, '', None, 'D105'],
    D106: [None, 'kW', None, 'D106'],
    D107: [None, 'Nm',
           'data[D106][0] * 1000 / (data[D118][0] / (60 / 6.28))',
           'D107'],

    D109: [None, 'kW',
           'data[D105][0] * data[D106][0]',
           'D109'],

    F109: [None, '',
           '"verified" if data[D109][0] > data[D101][0] else "not verified"',
           'F109'],

    D110: [None, 'Nm',
           'data[D109][0] * 1000 / (data[D118][0] * 6.28 / 60)',
           'D110'],
    D111: [None, '',
           'data[D109][0] / data[D101][0]',
           'D111'],
    D112: [None, '',
           'data[D109][0] / data[D99][0]',
           'D112'],
    F112: [None, '',
           '"OK" if data[D112][0] > 1 else "NOT OK"',
           'F112'],
    D115: [None, '', None, 'D115'],
    D116: [None, 'm', None, 'D116'],
    D117: [None, 'm/min',
           'data[E29][0]',
           'D117'],
    D118: [None, 'rpm', None, 'D118'],
    D119: [None, 'rpm',
           'data[D117][0] * 2 / (data[D116][0] * 2 * 3.14)',
           'D119'],
    D120: [None, '', None, 'D120'],
    D121: [None, 'kW',
           'data[D106][0] * data[D115][0]',
           'D121'],
    D122: [None, '',
           'data[D118][0] / (data[D119][0] * data[D120][0])',
           'D122'],
    D123: [None, 'Nm',
           '(data[D107][0] * data[D122][0] * data[D115][0]) / 1000',
           'D123'],

    D127: [None, 'm',
           'data[D116][0]',
           'D127'],
    D128: [None, 't', None, 'D128'],
    D129: [None, 'kN',
           'data[D128][0] * 9.8121',
           'D129'],
    D130: [None, '', None, 'D130'],

    D131: [None, 'Nm',
           'data[D130][0] * 60 * 1000 * data[D106][0] / (data[D118][0] * 2 * 3.14)',
           'D131'],
    D132: [None, '',
           'data[D122][0] * data[D120][0]',
           'D132'],
    D133: [None, 'kN',
           'data[E35][0] * data[D129][0]',
           'D133'],
    D134: [None, 'Nm',
           'data[D133][0] * data[D127][0] * 1000 / 2',
           'D134'],
    D135: [None, '', None, 'D135'],
    D136: [None, 'Nm',
           '(data[D131][0] * data[D132][0] / data[D135][0]) * data[E53][0]',
           'D136'],
    F136: [None, '',
           '"WHEEL/RAIL GRIP VERIFIED" if data[D134][0] > data[D136][0] else "SKIDDING SLIP"',
           'F136'],
    D137: [None, '',
           'data[D135][0] * data[D105][0]',
           'D137'],
    D138: [None, '', None, 'D138'],

    E143: [None, 't',
           'data[D105][0] * data[E59][0] * data[D122][0] ** 2 * 4 / data[D116][0] ** 2 / 1000',
           'E143'],
    E144: [None, 't',
           'data[D138][0] * data[E58][0] * 4 / data[D116][0] ** 2 / 1000',
           'E144'],
    E145: [None, 't',
           'data[E143][0] + data[E144][0]',
           'E145'],

    D147: [None, 'Nm', None, 'D147'],

    D149: [None, 'kN',
           'data[E66F66][0][0] + data[E71F71][0][0]',
           'D149'],
    D150: [None, 'kN',
           'data[E67F67][0][0] + data[E72F72][0][0]',
           'D150'],

    D155: [None, 'kN',
           'data[E21][0] * data[E32][0] * 9.81',
           'D155'],
    D156: [None, 'kNm',
           'data[D147][0] * data[D122][0] / 1000',
           'D156'],
    D157: [None, 'kN',
           'data[D156][0] * 2 / data[D116][0]',
           'D157'],
    D158: [None, 'kN',
           'data[D157][0] * data[D105][0]',
           'D158'],
    D159: [None, 'kN',
           'data[E35][0] * data[E15][0] * 9.81 * data[D137][0] / data[D138][0]',
           'D159'],
    D160: [None, 'kN',
           'min([data[D158][0], data[D159][0]]) + data[D155][0]',
           'D160'],

    D162: [None, '',
           'data[D150][0] / data[D160][0]',
           'D162'],
    F162: [None, '',
           '\'OK\' if data[D162][0] < 1 else \'NOT OK\'',
           'F162'],

    D167: [None, 'kN',
           'data[D160][0] - data[D150][0]',
           'D167'],
    D168: [None, 't',
          'data[E145][0] + data[E20][0]',
           'D168'],
    D169: [None, 'm/s²',
           'data[D167][0] / data[D168][0]',
           'D169'],
    D170: [None, 's',
           'data[E29][0] / 60 / data[D169][0]',
           'D170'],
    D171: [None, 'm',
          '0.5 * data[D169][0] * data[D170][0] ** 2',
           'D171'],

    D175: [None, 'kN',
           'data[D160][0] - data[E72F72][0][0]',
           'D175'],
    D176: [None, 't',
          'data[E145][0] + data[E20][0]',
           'D176'],
    D177: [None, 'm/s²',
           'data[D175][0] / data[D176][0]',
           'D177'],
    D178: [None, 's',
           'data[D175][0] / data[D176][0]',
           'D178'],
    D179: [None, 'm',
          '0.5 * data[D177][0] * data[D178][0] ** 2',
           'D179'],

    D182: [None, 's', None, 'D182'],
    D183: [None, 'm/s²',
          'data[E29][0] / data[D182][0] / 60',
           'D183'],
    D184: [None, 'kN',
          'data[D183][0] * data[D176][0]',
           'D184'],
    D185: [None, 'm/s²',
          'data[D184][0] + data[D150][0]',
           'D185'],
    D186: [None, 'm',
          '0.5 * data[D183][0] * data[D182][0] ** 2',
           'D186'],
    D187: [None, 'Nm',
          'data[D185][0] * data[D116][0] / 2 / data[D105][0] / data[D122][0] * 1000',
           'D187'],

    D192: [None, 'kN',
          'data[E68][0] + data[E72F72][0][0]',
           'D192'],
    D193: [None, 'kN',
          'data[D158][0] * 2 / 3',
           'D193'],
    D194: [None, 'kN',
           'data[D192][0] - data[D193][0]',
           'D194'],
    D195: [None, '', None, 'D195'],
    D196: [None, 'kN',
          'data[D194][0] / data[D195][0]',
           'D196']
}

# FUNZIONI ----------------------------------------------------------------------
# per pyinstaller
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# legge un file txt interno, ormai inutile poiché utilizzata per test
def leggi_dati_txt():
    current_line = 0
    print('\nReading file...')
    try:
        with open('data_sample.txt', 'r') as f:  # apre il file di testo e leggi le righe
            lines = f.readlines()  # crea una lista, ogni riga è un elemento
            for key in data.keys():
                if type(data[key][2]) is list:
                    for i in range(len(data[key][2])):
                        if not data[key][2][i]:
                            try:
                                data[key][0][i] = float(lines[current_line].strip())  # legge la riga corrente e incrementa l'indice della riga corrente
                                current_line += 1
                            except ValueError:
                                print('\nFile input data is not valid at line ' + str(current_line) + '.')
                                input('\nPress \'enter\' key to close the program.')
                                exit(-1)
                else:
                    if not data[key][2]:
                        try:
                            data[key][0] = float(lines[current_line].strip())  # legge la riga corrente e incrementa l'indice della riga corrente
                            current_line += 1
                        except ValueError:
                            print('\nFile input data is not valid at line ' + str(current_line) + '.')
                            input('\nPress \'enter\' key to close the program.')
                            exit(-1)
    except FileNotFoundError:
        print('\nThe file with input data does not exist.')
        input('\nPress \'enter\' key to close the program.')
        exit(-1)
    return

# prende una lista di dati di input e li inserisce uno ad uno all'interno della struttura
def leggi_dati_lista(input_data_list):
    index = 0
    print('\nTaking input data from list...')
    for key in data.keys():
        if type(data[key][2]) is list:
            for i in range(len(data[key][2])):
                if not data[key][2][i]:
                    data[key][0][i] = input_data_list[index]
                    index += 1
        elif not data[key][2]:
            data[key][0] = input_data_list[index]
            index += 1
    print('\nHo finito di calcolare.')
    return

# utile solo per applicazione da terminale
def richiedi_dati_input():
    print('\nInsert every values one by one as requested.\n')
    for key in data.keys():  # cerca i dati di input controllando il terzo valore
        if type(data[key][2]) is list:  # controllo se ha più di un dato
            for i in range(len(data[key][2])):  # cerco None nella lista
                if not data[key][2][i]:  # se lo trovo
                    try:  # prendo l'input
                        if data[key][1][i] == '':
                            data[key][0][i] = float(input(key + ' = '))
                        else:
                            data[key][0][i] = float(input(key + ' [' + data[key][1][i] + '] = '))
                    except ValueError:  # se non viene inserito il valore corretto
                        print('\nLast input data is not valid.')
                        input('\nPress \'enter\' key to close the program.')
                        exit(-1)  # fermo il programma
        else:  # se è un singolo valore
            if not data[key][2]:  # controllo se è dato di input
                try:  # se lo è
                    if data[key][1] == '':
                        data[key][0] = float(input(key + ' = '))
                    else:
                        data[key][0] = float(input(key + ' [' + data[key][1] + '] = '))
                except ValueError:
                    print('\nLast input data is not valid.')
                    input('\nPress \'enter\' key to close the program.')
                    exit(-1)
    return

# calcola i valori di output
def calcola_dati_output():
    msg.config(text='')
    print('\nCalculating ouput values...')
    for key in data.keys(): # cerca i dati di output
        if type(data[key][2]) is list: # controllo se ha più di un dato
            for i in range(len(data[key][2])): # cerco formule nella lista
                if data[key][2][i]: # se trovo la formula
                    data[key][0][i] = eval(data[key][2][i]) # calcolo con eval il dato di output
        elif data[key][2]: # se è un valore singolo, controllo che sia una formula
            data[key][0] = eval(data[key][2]) # calcolo
    return

# stampa dei valori incolonnati
def stampa_dati():
    print("{:<150} {:<10} {:<10}".format("Key", "Value", "Unit")) # header con titoli delle colonne
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    for key, value in data.items():
        if type(value[0]) is list:
            for i in range(len(data[key][0])):
                if type(value[0][i]) is float:
                    formatted_value = '{:.3f}'.format(value[0][i])
                    print("{:<150} {:<10} {:<10}".format(key, formatted_value, value[1][i]))
        elif type(value[0]) is float:
            formatted_value = '{:.3f}'.format(value[0])
            print("{:<150} {:<10} {:<10}".format(key, formatted_value, value[1]))
        else:
            print("{:<150} {:<10} {:<10}".format(key, value[0], value[1]))

# inserimento dei dati su file Excel
def inserisci_dati_excel():
    for key in data.keys():
        if type(data[key][3]) is list: # controllo se ha più di una cella
            for i in range(len(data[key][3])): # per ogni posizione
                trav_sheet[data[key][3][i]].value = data[key][0][i] # inserisco il valore
        else: # se non è una lista
            trav_sheet[data[key][3]].value = data[key][0]

# richiesta directory e salvataggio del file nella stessa
def salva_file_excel():
    data_corrente = datetime.now().strftime('__%Y-%m-%d__%H-%M')
    trav_file_name = 'Travelling' + data_corrente + '.xlsx'
    root = Tk()  # creo la finestra principale di tkinter
    root.withdraw()  # la nascondo
    new_dir_path = filedialog.askdirectory()  # chiedo dove salvare il file
    new_file_path = os.path.join(new_dir_path, trav_file_name)  # salvo il percorso del file
    trav_file.save(new_file_path)  # salvataggio del file
    if new_dir_path == '':
        msg.config(text='File was not created.')
    else:
        msg.config(text='File created in ' + new_dir_path + '.')

# unisce le funzioni di inserimento dati nel file excel e del suo salvataggio nella directory scelta da utente
def crea_file_excel(entry_fields_list, input_data_list):
    try:
        submit(entry_fields_list)
        leggi_dati_lista(input_data_list)
        calcola_dati_output()
        inserisci_dati_excel()
        salva_file_excel()
    except (ValueError, IndexError):
        print('Fermo il flusso del pulsante.')

# i due eventi relativi alla finestra associati al ridimensionamento della finestra e
# al movimento della rotella del mouse
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# aggiunge una riga nella finestra con il formato --> Distanza [   ] m
def aggiungi_riga(desc, unità, riga):
    entry_fields.append(Entry(input_frame, font='Helvetica 12', width=10, background='#e8f0ff'))
    Label(input_frame, text=desc, font='Helvetica 12', background='white', padx=10).grid(row=riga, column=0, sticky="W")
    entry_fields[-1].grid(row=riga, column=1, sticky='W', padx=0, pady=10)
    Label(input_frame, text=unità, font='Helvetica 12', background='white').grid(row=riga, column=2, sticky="W", padx=10)
    return riga+1

# aggiunge un titolo nella finestra
def aggiungi_titolo(titolo, riga):
    Label(input_frame, text=titolo, font='Helvetica 12 bold', background='white', anchor='w', pady=10).grid(row=riga, column=0, padx=5, pady=0, sticky='w')
    return riga+1

# inserisce in una lista i dati che l'utente ha scritto nei vari campi di input
def submit(texts):
    input_list.clear()
    for i, text in enumerate(texts): # itero per gli oggetti Entry
        try:
            input_list.append(float(text.get())) # prendo il loro valore
            entry_fields[i].config(background='#e8f0ff')
        except ValueError:
            msg.config(text='Some values are missing or not valid.')
            entry_fields[i].config(background='#ff8080')
    return


# ELABORAZIONE ----------------------------------------------------------------------
print('-- TRAVELLING EXCEL FILE CREATOR --')

# caricamento del file Travelling.xlsx vuoto per riempimento futuro
try:
    trav_file = load_workbook(resource_path('Travelling.xlsx')) # carico il file Travelling.xlsx completo
    trav_sheet = trav_file.active # carico il foglio singolo, l'unico che è presente, TRAVELLING
except FileNotFoundError:
    print('\nThe blank Travelling Excel file does not exist.')
    input('\nPress \'enter\' key to close the program.')
    exit(-1)

# creazione della finestra dotata di scrollbar
window = Tk()
window.geometry('700x600')
window.resizable(False, False)
window.title('Travelling Excel File Creator')
window.grid_columnconfigure(0, weight=1)
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)
canvas_frame = Frame(main_frame)
canvas_frame.pack(fill=BOTH, expand=1)
canvas = Canvas(canvas_frame, bg='white', highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
input_frame = Frame(canvas)
input_frame.pack(side=TOP, fill=X, padx=10, pady=10)
input_frame.configure(background='white')
canvas.create_window((0, 0), window=input_frame, anchor="nw")
canvas.bind("<Configure>", on_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

# posizionamento titolo
Label(input_frame, text='Travelling Excel File Creator', fg='#002975', font='Helvetica 22 bold', background='white').grid(row=0, column=0, padx=0, pady=15, columnspan=3)

#inserimento di ogni riga nella finestra
for key in data.keys():  # cerca i dati di input controllando il terzo valore
    aggiunto = False
    if type(data[key][2]) is list:  # controllo se ha più di un dato
        for i in range(len(data[key][2])):  # cerco i dati di input
            if not data[key][2][i]:  # se lo trovo
                for j in range(len(titoli)):
                    if titoli[j][0] in key:
                        if titoli[j][1] == False:
                            n_riga = aggiungi_titolo(titoli[j][0].replace(cs, ''), n_riga)
                            titoli[j][1] = True
                        new_key = key.replace(titoli[j][0], '')
                        n_riga = aggiungi_riga(new_key, data[key][1][i], n_riga)  # aggiungo la riga
                        aggiunto = True
                if aggiunto == False:
                    n_riga = aggiungi_riga(key, data[key][1][i], n_riga)  # aggiungo la riga
    else:  # se è un singolo valore
        if not data[key][2]:  # controllo se è un dato di input
            for j in range(len(titoli)):
                if titoli[j][0] in key:
                    if titoli[j][1] == False:
                        n_riga = aggiungi_titolo(titoli[j][0].replace(cs, ''), n_riga)
                        titoli[j][1] = True
                    new_key = key.replace(titoli[j][0], '')
                    n_riga = aggiungi_riga(new_key, data[key][1], n_riga)  # aggiungo la riga
                    aggiunto = True
            if aggiunto == False:
                n_riga = aggiungi_riga(key, data[key][1], n_riga)  # aggiungo la riga

submit_button = Button(input_frame, command=lambda: crea_file_excel(entry_fields, input_list), background='#b3deff', text='CREATE EXCEL FILE', font='Helvetica 12 bold', width=20, height=1)
submit_button.grid(row=n_riga, column=0, sticky="w", padx=15, pady=20, columnspan=3)
msg = Label(input_frame, background='white', text='', font='Helvetica 12', wraplength=430)
msg.grid(row=n_riga, column=0, sticky="e", padx=20, pady=20, columnspan=3)

window.mainloop()
