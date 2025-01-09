import m5
from m5.objects import *
from m5.util import addToPath
addToPath("../configs/")
from common.Caches import *

class ChallengeCache(L1Cache):
    size = '32kB'
    assoc = 8
    replacement_policy = TreePLRURP()

    def connectCPU(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMem(self, bus):
        self.mem_side = bus.cpu_side_ports

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('32MB'), AddrRange(0xff00000000, size='1MB')]

system.cpu = X86TimingSimpleCPU()

system.crossbar = L2XBar()
system.crossbar.cpu_side_ports = [system.cpu.icache_port, system.cpu.dcache_port]

system.membus = SystemXBar()
system.cache = ChallengeCache()
system.cache.connectMem(system.membus)
system.cache.connectCPU(system.crossbar)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.mem_ctrl2 = MemCtrl()
system.mem_ctrl2.dram = DDR3_1600_8x8()
system.mem_ctrl2.dram.range = system.mem_ranges[1]
system.chalmem = ChallengeMemobj()
system.mem_ctrl2.port = system.chalmem.mem_side
system.chalmem.cpu_side = system.membus.mem_side_ports
# system.mem_ctrl2.port = system.membus.mem_side_ports

system.chal = ChallengeObj()
system.chal.mem_side = system.crossbar.cpu_side_ports
system.chal.data_port = system.membus.mem_side_ports

print("page size",     system.mem_ctrl.dram.devices_per_rank.value
    * system.mem_ctrl.dram.device_rowbuffer_size.value)

binary = '/tmp/challenge-bin'

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
