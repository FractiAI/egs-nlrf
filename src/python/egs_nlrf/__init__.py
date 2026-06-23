"""EGS Nodal Lattice Resonator Framework — SynthOBS empirical engine."""

PHI_EGS = 1.618033988749895
A0_BOHR = 0.529177210903  # angstrom

__all__ = ["PHI_EGS", "SynthOBSEmpiricalEngine"]

def __getattr__(name: str):
    if name == "SynthOBSEmpiricalEngine":
        from egs_nlrf.engine import SynthOBSEmpiricalEngine
        return SynthOBSEmpiricalEngine
    raise AttributeError(name)
