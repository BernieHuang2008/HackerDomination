from scripts.session import session
from scripts.checker import checker

import simulator.v0 as sim

sim.init(session)
sim.set_checker(checker)
sim.start()
