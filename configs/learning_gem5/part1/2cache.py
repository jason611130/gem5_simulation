import os
import m5
from m5.objects import *
from caches import *
from common import SimpleOpts

# 加入 resume 選項來控制是否從 checkpoint 繼續
SimpleOpts.add_option("--resume", default=False, action="store_true",
                      help="Resume simulation from checkpoint")
SimpleOpts.add_option("binary", nargs="?", default=os.path.join(
    "/home/jason/Desktop/SPECCPU2006/benchspec/CPU2006/429.mcf/run/build_base_amd64-m64-gcc42-nn.0000/mcf"
))

args = SimpleOpts.parse_args()

# 建立 system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

system.cpu = X86TimingSimpleCPU()
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(args)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(args.binary)
process = Process()
process.executable = args.binary
process.cmd = [args.binary, "/home/jason/Desktop/SPECCPU2006/benchspec/CPU2006/429.mcf/data/test/input/inp.in"]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)

if args.resume:
    print("resume")
    m5.instantiate("mcf-200k-checkpoint")
    exit_event = m5.simulate(200_000_000_000)
    print(f"[INFO] Checkpointing at tick {m5.curTick()} due to {exit_event.getCause()}")
    m5.checkpoint("mcf-200k-checkpoint")
    
else:
    print("[INFO] Starting fresh simulation")
    m5.instantiate()
    print("[INFO] Running until 200,000 ticks to take checkpoint")
    exit_event = m5.simulate(200_000_000_000)
    print(f"[INFO] Checkpointing at tick {m5.curTick()} due to {exit_event.getCause()}")
    m5.checkpoint("mcf-200k-checkpoint")

print("[INFO] Continuing simulation")
print(f"[INFO] Exiting @ tick {m5.curTick()} due to {exit_event.getCause()}")
