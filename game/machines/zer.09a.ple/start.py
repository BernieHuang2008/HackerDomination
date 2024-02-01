import sys, os

sys.path.append(os.getcwd())

from scripts.session import session
from scripts.checker import checker
import simulator.v0.main as sim

if __name__ == "__main__":
    user, pwd = sys.argv[1], sys.argv[2]

    session["prof"]["user"] = user
    session["dir"] = "/home/" + user

    sim.init(session)
    sim.set_checker(checker)
    sim.start()
