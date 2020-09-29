# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:50:14 2020

@author: Rohit Kumar
#Assignment_1
#Computer Applications in Power Systems
"""

import xml.etree.ElementTree as ET

# for parsing the data

EQ = ET.parse('Assignment_EQ_reduced.XML')
SSH = ET.parse('Assignment_SSH_reduced.XML')
#EQ = ET.parse('MicroGridTestConfiguration_T1_BE_EQ_V2.XML')
#SSH = ET.parse('MicroGridTestConfiguration_T1_BE_SSH_V2.XML')
microgrid_EQ = EQ.getroot()
microgrid_SSH = SSH.getroot()

ns = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

'''
# defining classes and then extraction of data for different elements of the system model from the given XML files
'''

"""
#AC Line segment
"""

ACLineSegmentValue=[]
class AC_Line_Segment:
  def __init__(self, rdf_ID, name, equip_cont_rdf_ID, ACLineSeg_r, ACLineSeg_x, bch, gch, length, base_Volt_rdf_ID):    
    self.rdf_ID = rdf_ID
    self.name = name
    self.equip_cont_rdf_ID = equip_cont_rdf_ID
    self.ACLineSeg_r = ACLineSeg_r
    self.ACLineSeg_x = ACLineSeg_x
    self.bch = bch
    self.gch = gch
    self.length = length
    self.base_Volt_rdf_ID = base_Volt_rdf_ID

# Extraction of data for AC Line from XML files
    
for AC_line_seg in microgrid_EQ.iterfind('cim:ACLineSegment', ns):
    ACLineSegmentValue.append(AC_Line_Segment(AC_line_seg.get(ns['rdf']+'ID'),
                                              AC_line_seg.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                              AC_line_seg.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource'),
                                              AC_line_seg.find("{"+ns['cim']+"}"+'ACLineSegment.r').text,
                                              AC_line_seg.find("{"+ns['cim']+"}"+'ACLineSegment.x').text,
                                              AC_line_seg.find("{"+ns['cim']+"}"+'ACLineSegment.bch').text,
                                              AC_line_seg.find("{"+ns['cim']+"}"+'Conductor.length').text,
                                              AC_line_seg.find("{"+ns['cim']+"}"+'ACLineSegment.gch').text,
                                              AC_line_seg.find("{"+ns['cim']+"}"+'ConductingEquipment.BaseVoltage').get(ns['rdf']+'resource')))  
    
""" 
# Busbar
"""

BusbarSectionValue=[]
class Busbar_Section:
    def __init__(self, rdf_ID, name, equip_cont_rdf_ID):
        self.rdf_ID=rdf_ID
        self.name=name
        self.equip_cont_rdf_ID = equip_cont_rdf_ID
        
# Extraction of data for Busbar from XML files   

for BusbarSection in microgrid_EQ.iterfind('cim:BusbarSection',ns):
    BusbarSectionValue.append(Busbar_Section(BusbarSection.get(ns['rdf']+'ID'),
                                             BusbarSection.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                             BusbarSection.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource')))

"""
# Substation
"""

SubstationValue=[]
class substation:   
    def __init__(self, rdf_ID, name, region_rdf_IDF):
        self.rdf_ID=rdf_ID
        self.name=name
        self.region_rdf_IDF=region_rdf_IDF

# Extraction of data for Substation from XML files   
          
for substation_ in microgrid_EQ.iterfind('cim:Substation',ns):
    SubstationValue.append(substation(substation_.get(ns['rdf']+'ID'),
                                      substation_.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                      substation_.find("{"+ns['cim']+"}"+'Substation.Region').get(ns['rdf']+'resource')))

"""
# Synchronous Machine
"""

SynchMachineValue=[]
class SynchMachine:
    def __init__(self, rdf_ID, name, rated_S, equip_cont_rdf_ID, gen_unit_rdf_ID, s_real, s_imag):
        self.rdf_ID=rdf_ID
        self.name=name
        self.rated_S=rated_S
        self.equip_cont_rdf_ID=equip_cont_rdf_ID
        self.gen_unit_rdf_ID=gen_unit_rdf_ID
        self.s_real=s_real
        self.s_imag=s_imag
        
# Extraction of data for Synchronous Machine from XML files         
      
j=-1   # since pyhton starts from 0, and it is here as j+1 
for synch_mach in microgrid_EQ.iterfind('cim:SynchronousMachine',ns):
    j=j+1    
    SynchMachineValue.append(SynchMachine(synch_mach.get(ns['rdf']+'ID'),
                                          synch_mach.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                          synch_mach.find("{"+ns['cim']+"}"+'RotatingMachine.ratedS').text,
                                          synch_mach.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource'),
                                          synch_mach.find("{"+ns['cim']+"}"+'RotatingMachine.GeneratingUnit').get(ns['rdf']+'resource'),
                                                     "",""))

# To find out the state of Synchronous Machine  
    
    for synch_mach in microgrid_SSH.iterfind('cim:SynchronousMachine',ns):
        RDF_SSH=synch_mach.get(ns['rdf']+'about')
        k=0
        while k<=j:
            if '#' + SynchMachineValue[k].rdf_ID == RDF_SSH:
                SynchMachineValue[k].s_real = synch_mach.find("{"+ns['cim']+"}"+'RotatingMachine.p').text
                SynchMachineValue[k].s_imag = synch_mach.find("{"+ns['cim']+"}"+'RotatingMachine.q').text
                k=k+1

"""                
# Consumer Loads
"""           
ConsumerValues=[]
class Consumer:
    def __init__(self, rdf_ID, name, equip_cont_rdf_ID, load_response_rdf_ID, P, Q):
        self.rdf_ID=rdf_ID
        self.name=name
        self.equip_cont_rdf_ID = equip_cont_rdf_ID
        self.load_response_rdf_ID=load_response_rdf_ID
        self.P=P
        self.Q=Q

# Extraction of data for Consumer Loads from XML files         
        
j=-1
for cons in microgrid_EQ.iterfind('cim:EnergyConsumer',ns):
    j=j+1
    LoadResponse = cons.find("{"+ns['cim']+"}"+'EnergyConsumer.LoadResponse')
    if LoadResponse is not None:
        ConsumerValues.append(Consumer(cons.get(ns['rdf']+'ID'),
                                       cons.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                       cons.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource'),
                                       cons.find("{"+ns['cim']+"}"+'EnergyConsumer.LoadResponse').get(ns['rdf']+'resource'),
                                       "",""))
    else:
        ConsumerValues.append(Consumer(cons.get(ns['rdf']+'ID'),
                                           cons.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                           cons.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource'),
                                           "","",""))

# To find out the state of Loads            
for cons in microgrid_SSH.iterfind('cim:EnergyConsumer',ns):
    RDF_SSH=cons.get(ns['rdf']+'about')
    k=0
    while k<=j:
        if '#' + ConsumerValues[k].rdf_ID == RDF_SSH:
                 ConsumerValues[k].P = cons.find("{"+ns['cim']+"}"+'EnergyConsumer.p').text
                 ConsumerValues[k].Q = cons.find("{"+ns['cim']+"}"+'EnergyConsumer.q').text
        k=k+1
        

'''
# Terminal
'''
        
TerminalValue=[] 
class Terminal:
    def __init__(self, rdf_ID, name, cond_eqp_rdf_ID, CN_rdf_ID, Connection):
        self.rdf_ID=rdf_ID
        self.name=name
        self.cond_eqp_rdf_ID=cond_eqp_rdf_ID
        self.CN_rdf_ID=CN_rdf_ID
        self.Connection=Connection

# Extraction of data for Terminal from XML files
        
j=-1
for terminal in microgrid_EQ.iterfind('cim:Terminal',ns):
    j=j+1
    TerminalValue.append(Terminal(terminal.get(ns['rdf']+'ID'),
                                  terminal.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                  terminal.find("{"+ns['cim']+"}"+'Terminal.ConductingEquipment').get(ns['rdf']+'resource'),
                                  terminal.find("{"+ns['cim']+"}"+'Terminal.ConnectivityNode').get(ns['rdf']+'resource')
                                  ,""))
    
for terminal in microgrid_SSH.iterfind('cim:Terminal',ns):
    terminal_SSH = terminal.get(ns['rdf']+'about')
    
    k=0
while k<=j:
    if '#'+TerminalValue[k].rdf_ID == terminal_SSH:
        TerminalValue[k].Connection = terminal.find("{"+ns['cim']+"}"+'ACDCTerminal.connected').text
    k=k+1

'''
# Node
'''
    
NodeValue=[]
class Node:
    def __init__(self, rdf_ID, name, Con_node_cont_rdf_ID, conn_eqp):
        self.rdf_ID=rdf_ID
        self.name=name
        self.Con_node_cont_rdf_ID = Con_node_cont_rdf_ID
        self.conn_eqp = []

# Extraction of data for Node from XML files        
  
for node in microgrid_EQ.iterfind('cim:ConnectivityNode',ns):
    NodeValue.append(Node(node.get(ns['rdf']+'ID'),
                          node.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                          node.find("{"+ns['cim']+"}"+'ConnectivityNode.ConnectivityNodeContainer').get(ns['rdf']+'resource'),
                          [])) 
  
'''  
# Breaker
'''
    
BreakerValue=[]    
class Breaker:
    def __init__(self, rdf_ID, name, equip_cont_rdf_ID, state):
        self.rdf_ID=rdf_ID
        self.name=name
        self.equip_cont_rdf_ID=equip_cont_rdf_ID
        self.state=state

# Extraction of data for Breaker from XML files

j=-1
for breaker in microgrid_EQ.iterfind('cim:Breaker',ns):
    j=j+1
    BreakerValue.append(Breaker(breaker.get(ns['rdf']+'ID'),
                                breaker.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                breaker.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource'),
                               ""))

# Extraction of states for Breaker from XML files

for breaker in microgrid_SSH.iterfind('cim:Breaker',ns):
    breaker_SSH=breaker.get(ns['rdf']+'about')
    k=0
    while k<=j:
        if '#'+BreakerValue[k].rdf_ID == breaker_SSH:
            BreakerValue[k].state = breaker.find("{"+ns['cim']+"}"+'Switch.open').text
        k=k+1
        

'''
# Power Transformer  
'''
        
PowerTransformerValue=[]        
class P_Tf:
    def __init__(self, rdf_ID, name, equip_cont_rdf_ID):
        self.rdf_ID=rdf_ID
        self.name = name
        self.equip_cont_rdf_ID = equip_cont_rdf_ID

# Extraction of data for Power Transformer from XML files

for tf in microgrid_EQ.iterfind('cim:PowerTransformer',ns):
    PowerTransformerValue.append(P_Tf(tf.get(ns['rdf']+'ID'),
                                      tf.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                      tf.find("{"+ns['cim']+"}"+'Equipment.EquipmentContainer').get(ns['rdf']+'resource')))
  
'''   
# Power Transformer End
'''
    
PowerTransformerEndValue=[]
class P_tf_end:
    def __init__(self, rdf_ID, name, Tf_r, Tf_x, Tf_b, Tf_g, V_base_rdf, Tf_rdf_ID, rated_S,P_tf_end_nr):
        self.rdf_ID=rdf_ID
        self.name=name
        self.Tf_r=Tf_r        
        self.Tf_x=Tf_x
        self.Tf_b=Tf_b
        self.Tf_g=Tf_g
        self.V_base_rdf = V_base_rdf
        self.Tf_rdf_ID = Tf_rdf_ID
        self.rated_S = rated_S
        self.P_tf_end_nr = P_tf_end_nr
           
# Extraction of data for Power Transformer End from XML files
        
for Tf_end in microgrid_EQ.iterfind('cim:PowerTransformerEnd',ns):
    PowerTransformerEndValue.append(P_tf_end(Tf_end.get(ns['rdf']+'ID'),
                                             Tf_end.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                             Tf_end.find("{"+ns['cim']+"}"+'PowerTransformerEnd.r').text,
                                             Tf_end.find("{"+ns['cim']+"}"+'PowerTransformerEnd.x').text,
                                             Tf_end.find("{"+ns['cim']+"}"+'PowerTransformerEnd.b').text,
                                             Tf_end.find("{"+ns['cim']+"}"+'PowerTransformerEnd.g').text,
                                             Tf_end.find("{"+ns['cim']+"}"+'TransformerEnd.BaseVoltage').get(ns['rdf']+'resource'),
                                             Tf_end.find("{"+ns['cim']+"}"+'PowerTransformerEnd.PowerTransformer').get(ns['rdf']+'resource'),
                                             Tf_end.find("{"+ns['cim']+"}"+'PowerTransformerEnd.ratedS').text,
                                             Tf_end.find("{"+ns['cim']+"}"+'TransformerEnd.endNumber').text))

'''
# voltage level
'''

VoltageLevelValue = []
class voltage_level:
    def __init__ (self, rdf_ID, name, subs_rdf_ID, base_voltage_rdf_ID):
        self.rdf_ID = rdf_ID
        self.name = name
        self.subs_rdf_ID = subs_rdf_ID
        self.base_voltage_rdf_ID = base_voltage_rdf_ID
       
# Extraction of data for voltage level from XML files 
    
for volt in microgrid_EQ.iterfind('cim:VoltageLevel',ns):
    VoltageLevelValue.append(voltage_level(volt.get(ns['rdf']+'ID'),
                                           volt.find("{"+ns['cim']+"}"+'IdentifiedObject.name').text,
                                           volt.find("{"+ns['cim']+"}"+'VoltageLevel.Substation').get(ns['rdf']+'resource'),
                                           volt.find("{"+ns['cim']+"}"+'VoltageLevel.BaseVoltage').get(ns['rdf']+'resource')))

'''    
# Base Voltage  
'''

BaseVoltageValue=[]
class base_voltage:
    def __init__(self, rdf_ID, nominal_value):
        self.rdf_ID = rdf_ID
        self.nominal_value = nominal_value

# Extraction of data for base voltage level from XML files 
        
for B_Volt in microgrid_EQ.iterfind('cim:BaseVoltage',ns):
    BaseVoltageValue.append(base_voltage(B_Volt.get(ns['rdf']+'ID'),
                                         B_Volt.find("{"+ns['cim']+"}"+'BaseVoltage.nominalVoltage').text))
     
'''    
# Conducting Equipment  
'''

ConductingEquipmentValue=[]    
class Conducting_Equipment:
    def __init__(self, rdf_ID, name):
        self.rdf_ID=rdf_ID
        self.name=name
  
# For different conducting equipments in the system

#print("\n"'Number of particular equipments in the system model')        
for elementa in range(len(ACLineSegmentValue)):
    ConductingEquipmentValue.append(Conducting_Equipment(ACLineSegmentValue[elementa].rdf_ID, ACLineSegmentValue[elementa].name))
print('AC line:', len(ACLineSegmentValue)) # to get number of element in the model
    
for elementa in range(len(BusbarSectionValue)):
    ConductingEquipmentValue.append(Conducting_Equipment(BusbarSectionValue[elementa].rdf_ID, BusbarSectionValue[elementa].name))
print('Busbar Section:', len(BusbarSectionValue))  # to get number of element in the model
    
for elementa in range(len(SubstationValue)):
    ConductingEquipmentValue.append(Conducting_Equipment(SubstationValue[elementa].rdf_ID, SubstationValue[elementa].name))
print('Substation:', len(SubstationValue))  # to get number of element in the model
    
for elementa in range(len(SynchMachineValue)):
    ConductingEquipmentValue.append(Conducting_Equipment(SynchMachineValue[elementa].rdf_ID, SynchMachineValue[elementa].name))
print('Synch Machine:', len(SynchMachineValue))  # to get number of element in the model    
    
for elementa in range(len(ConsumerValues)):
    ConductingEquipmentValue.append(Conducting_Equipment(ConsumerValues[elementa].rdf_ID, ConsumerValues[elementa].name))
print('Consumer Load:', len(ConsumerValues))  # to get number of element in the model      
    
for elementa in range(len(BreakerValue)):
    ConductingEquipmentValue.append(Conducting_Equipment(BreakerValue[elementa].rdf_ID, BreakerValue[elementa].name))
print('Breaker:', len(BreakerValue)) # to get number of element in the model
    
for elementa in range(len(PowerTransformerValue)):
    ConductingEquipmentValue.append(Conducting_Equipment(PowerTransformerValue[elementa].rdf_ID, PowerTransformerValue[elementa].name))
print('Power Transformer:', len(PowerTransformerValue)) # to get number of element in the model


'''
# fetching different equipments connected to each node, 
# Terminal Id and node ids are compared to find out which terminal is connected to that particular node
# Conducting Equipments are identified in the model by matching the equipment id contained in the terminal 
'''
print("\n"'Node and their respected connected equipments')
for equipx in range(len(TerminalValue)):
    for equipy in range(len(NodeValue)):
        if TerminalValue[equipx].CN_rdf_ID == '#'+NodeValue[equipy].rdf_ID:
            for equipz in range(len(ConductingEquipmentValue)):
                if TerminalValue[equipx].cond_eqp_rdf_ID == '#'+ConductingEquipmentValue[equipz].rdf_ID:
                    NodeValue[equipy].conn_eqp.append(ConductingEquipmentValue[equipz].name)
'''
# This loop particularly for showing which element is connected to which node                     
'''
for equipa in range(len(NodeValue)): 
    print("\n"'Node:',NodeValue[equipa].name )
    print('Connected equipments:', NodeValue[equipa].conn_eqp)                 

                 
'''
# PandaPower implementation
'''

import pandapower as pp
net = pp.create_empty_network()

'''
# To create the bus in pandapower
'''
'''
I have tried to find certain connected elements (Bus) in Node dictionary/list, then have to run the 
check logic to identify the type of bus.
'''                    
for elementx in range(len(NodeValue)):   # for searching values in the Node list or dictionary
    Statement = 0   # Condition for checking bus type
    # rq_nodes= 
    for elementy in range(len(VoltageLevelValue)): # for searching values in the Voltages list or dictionary
        if NodeValue[elementx].Con_node_cont_rdf_ID == '#' + VoltageLevelValue[elementy].rdf_ID:  # matching the particular equipment connected to node and its voltage level 
            #return VoltageLevelValue[elementy]                      
            vn_kv = float(VoltageLevelValue[elementy].name)   # saving the voltage level of that bus
    for elementa in range(len(NodeValue[elementx].conn_eqp)): # searching connected equipments to certain node
        for elementb in range(len(BusbarSectionValue)):       # loop for digging in Busbar's list
            if BusbarSectionValue[elementb].name == NodeValue[elementx].conn_eqp[elementa]:  # finding the busbar connected at node
                #return NodeValue[elementx].name
                Statement = 1 # check logic to identify the bus type 
                bus = pp.create_bus(net, vn_kv, NodeValue[elementx].name, type='b' )
    if Statement == 0:
    #elif BusbarSectionValue[elementb].name != NodeValue[elementx].conn_eqp[elementa]:
    #else:
    #return NodeValue[elementx].name
        bus = pp.create_bus(net, vn_kv, NodeValue[elementx].name, type='n' )

print("\n"'BusBar')        
print(net.bus)

'''    
# To create Circuit breaker
'''

CB_element = []  # list for storing circuit breaker connected to particular node 
for elementa in range(len(BreakerValue)):
    for elementb in range(len(NodeValue)):
        for elementc in range(len(NodeValue[elementb].conn_eqp)):
            if BreakerValue[elementa].name == NodeValue[elementb].conn_eqp[elementc]:
                CB_element.append(NodeValue[elementb].name)
                
'''
Now I have the list of circuit breaker connected to particular nodes, since there are nine Circuit breakers 
in the system, and each has two connections/sides so to get the values from the list, each increment will 
show one connected to particular circuit breaker, each increment indentifies the buses connected to that end.
'''                
for elementa in range(len(BreakerValue)):
    name=BreakerValue[elementa].name
            
    if elementa == 0:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 1])
    
    if elementa == 1:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 1])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 2])
           
    if elementa == 2:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 2])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 3]) 
            
    if elementa == 3:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 3])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 4])    
            
    if elementa == 4:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 4])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 5])
            
    if elementa == 5:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 5])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 6])
        
    if elementa == 6:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 6])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 7])
        
    if elementa == 7:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 7])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 8])
            
    if elementa == 8:
        connection1 = pp.get_element_index(net, "bus", CB_element[elementa + 8])
    
        connection2 = pp.get_element_index(net, "bus", CB_element[elementa + 9])        
        
        
    switch = pp.create_switch(net, connection1, connection2, 'b', 'True','None', name)

print("\n"'Circuit Breaker')            
print(net.switch )  

'''
# To create transformer
'''

'''
Although this is not an ideal approach, I have tried to match the ids of Power Transformer with 
an end power tranformer, and if it matches then end number will identify the high voltage side
and low voltage side respectively. Since these XML files are pretty much consistent, end number 1
traces the high voltage side where as 2 as low voltage side. So I have tried to implement similiar 
approach further. 
'''

for elementa in range(len(PowerTransformerValue)):
    Tf_ID = (PowerTransformerValue[elementa].rdf_ID)
    for elementb in range(len(PowerTransformerEndValue)):
       Tf_end_ID = (PowerTransformerEndValue[elementb].Tf_rdf_ID)
       if '#' + Tf_ID == Tf_end_ID:
           Ptf_mva = PowerTransformerEndValue[elementb].rated_S
           #P_tf_end_R = PowerTransformerEndValue[elementb].Tf_r
           #P_tf_end_X = PowerTransformerEndValue[elementb].Tf_x
           #P_tf_end_Z = (P_tf_end_R*2 * P_tf_end_X*2)**0.5
           #P_tf_VSC = 0.1 * P_tf_end_Z * Ptf_mva
           #P_tf_VSCR = 0.1 * P_tf_end_R * Ptf_mva
           
           P_tf_end_nr_a = (PowerTransformerEndValue[elementb].P_tf_end_nr)
           #print('a')
           if P_tf_end_nr_a == '1':
               
               for elementc in range(len(NodeValue)):
                   for elementd in range(len(NodeValue[elementc].conn_eqp)):
                       if PowerTransformerValue[elementa].name == NodeValue[elementc].conn_eqp[elementd]:    
                           Tf_bus=(NodeValue[elementc].name)
                           for elemente in range(len(VoltageLevelValue)):
                               if NodeValue[elementd].Con_node_cont_rdf_ID == '#' + VoltageLevelValue[elemente].rdf_ID:
                                   #print('d')
                                   Side1=(VoltageLevelValue[elemente].name)
                                   hv_bus = pp.get_element_index(net, "bus", Tf_bus)
                                   vn_hv = float(Side1)
           elif P_tf_end_nr_a == '2':
               for elementc in range(len(NodeValue)):
                   for elementd in range(len(NodeValue[elementc].conn_eqp)):
                       if PowerTransformerValue[elementa].name == NodeValue[elementc].conn_eqp[elementd]:    
                           Tf_bus=(NodeValue[elementc].name)
                           for elemente in range(len(VoltageLevelValue)):
                               if NodeValue[elementd].Con_node_cont_rdf_ID == '#' + VoltageLevelValue[elemente].rdf_ID:
                                   #print('c')
                                   Side2=(VoltageLevelValue[elemente].name)
                                   lv_bus = pp.get_element_index(net, "bus", Tf_bus)
                                   vn_lv = float(Side2)
                                   trasnformer = pp.create_transformer_from_parameters(net, hv_bus, lv_bus, Ptf_mva, vn_hv, vn_lv, "0", "0", "0", "0", "0", None,None,None,None,None,None,None,False,True,PowerTransformerValue[elementa].name)


print("\n"'Transformer')
print(net.trafo) 

'''
# to create Line
'''
'''
Similiary, line has two ends and to find what is  connected at both ends, I have found the 
list of matching buses connected to particular line then have tried to identify if list 
starts from 0 or 1 and select the bus respectively from the list. 
'''

connected_bus = []
for elementa in range(len(ACLineSegmentValue)):
    length = float(ACLineSegmentValue[elementa].length)
    r = float(ACLineSegmentValue[elementa].ACLineSeg_r)/length
    x = float(ACLineSegmentValue[elementa].ACLineSeg_x)/length
    c = float(ACLineSegmentValue[elementa].bch)
    for elementb in range(len(NodeValue)):
        for elementc in range(len(NodeValue[elementb].conn_eqp)):
            if ACLineSegmentValue[elementa].name == NodeValue[elementb].conn_eqp[elementc]:
                connected_bus.append(NodeValue[elementb].name)

for elementa in range(len(ACLineSegmentValue)):                 
    if elementa == 0:
        bus_1 = pp.get_element_index(net, "bus", connected_bus[elementa])
        bus_2 = pp.get_element_index(net, "bus", connected_bus[elementa+1])
        
    if elementa == 1:
        bus_1 = pp.get_element_index(net, "bus", connected_bus[elementa+1])
        bus_2 = pp.get_element_index(net, "bus", connected_bus[elementa+2])
        
     
    name = ACLineSegmentValue[elementa].name
    
    line = pp.create_line_from_parameters(net, bus_1, bus_2, length, r, x, c, 'NaN', name)

print("\n"'Line')
print(net.line)

'''    
# To create the Load in pandapower
'''

'''
This is very basic logic that I have implemtneted, I have searched for name 
of load from dictionary connected to particular node. 
'''

for elementa in range(len(ConsumerValues)):
     p_mw = float(ConsumerValues[elementa].P)
     q_mw = float(ConsumerValues[elementa].Q)
    
     for elementc in range(len(NodeValue)):
        for elementd in range(len(NodeValue[elementc].conn_eqp)):
            if ConsumerValues[elementa].name == NodeValue[elementc].conn_eqp[elementd]:
                bus = pp.pp.get_element_index(net, "bus", NodeValue[elementc].name)
     load = pp.create_load(net, bus, p_mw, q_mw, 0, 0, None, ConsumerValues[elementa].name)


print("\n"'Consumer Load')
print(net.load)

'''
# To create the Generator in pandapower
'''

'''
This is a kind of similiar approach as in the case of load, I have searched for name 
of Machine from dictionary connected to particular node. 
'''

for elementa in range(len(SynchMachineValue)):
    name = SynchMachineValue[elementa].name
    sn_mva = float(SynchMachineValue[elementa].rated_S)
    p_mw = float(SynchMachineValue[elementa].s_real)
    
    for elementb in range(len(NodeValue)):   
        for elementc in range(len(NodeValue[elementb].conn_eqp)):
            if SynchMachineValue[elementa].name == NodeValue[elementb].conn_eqp[elementc]:
                bus = pp.pp.get_element_index(net, "bus", NodeValue[elementb].name)
    generator = pp.create_gen(net, bus, p_mw, 1, sn_mva, name)
    
print("\n"'Generator')
print(net.gen)
         

'''
# Network plotting 
'''
'''
plotting from the equipments created in the system in the pandapower
'''  
import pandapower.plotting as pp_plot
pp_plot.simple_plot(net, line_width=2.0, bus_size=2.0, trafo_size=4.0, plot_loads=True, load_size=6.0, sgen_size=4.0, switch_size=4.0, switch_distance=4,\
                            plot_line_switches=True, scale_size=True, bus_color='r',\
                            line_color='b',trafo_color='g',switch_color='k')