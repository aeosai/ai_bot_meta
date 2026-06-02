import time
import math
import random
import hashlib
import sys
import threading
import os
import json
from datetime import datetime

# ==========================================
# PART 1: THE PHYSICS ENGINE (DimensionalReactor)
# ==========================================

class DimensionalReactor:
    def __init__(self, dimensions=6, ram_allocation_mb=64):
        # --- THE KNOWN VARIABLES ---
        self.n = dimensions
        self.G = 6.67430e-11
        self.c = 299792458
        self.h_bar = 1.0545718e-34
        self.K_constant = 1.61803 
        
        # --- THE UNKNOWN UNKNOWNS ---
        self.vacuum_noise_floor = 1e-9 
        self.chronon_tick = 0
        
        # RAM Allocation
        self.ram_size = ram_allocation_mb * 1024 * 1024
        self.lattice = bytearray(self.ram_size)
        
        # System State
        self.P_max = 0.0
        self.lambda_stabilizer = 0.0
        self.omega_spin = 0.0
        self.is_collapsed = False
        self.entropy_debt = 0.0 

    def _quantum_fluctuation(self):
        return random.gauss(0, self.vacuum_noise_floor)

    def calculate_planck_energy(self):
        numerator = self.h_bar * (self.c ** 5) * self.G
        gamma_decay = 4.0 + self._quantum_fluctuation() 
        denominator = 16 * math.pi * gamma_decay
        info_limit = (self.n + 12) / (4 * math.log(2))
        E_total = (numerator / denominator) * info_limit
        return E_total

    def engage_stabilizer(self, input_power):
        local_K = self.K_constant + (self.entropy_debt * 0.001)
        try:
            if input_power < 0: raise ValueError("Vacuum Collapse")
            root_power = math.sqrt(input_power)
            self.lambda_stabilizer = root_power - local_K
            
            if self.lambda_stabilizer < 0:
                self.is_collapsed = True
                return "CRITICAL FAILURE: Negative Lambda."
            return "STABLE"
        except Exception as e:
            self.is_collapsed = True
            return f"COLLAPSE: {str(e)}"

    def generate_isopolymer_lattice(self):
        if self.is_collapsed: return
        # print(f"   >>> Weaving Isopolymer Lattice in {self.ram_size//1024//1024}MB RAM...")
        for i in range(0, 10000): 
            geometry_stress = int((i**3 * self.G) % 255)
            self.lattice[i] = geometry_stress
        self.entropy_debt += math.log(2)

    def spin_interface_protocol(self, target_rpm):
        self.omega_spin = target_rpm
        coriolis_distortion = (self.omega_spin ** 2) * self._quantum_fluctuation()
        stability_impact = self.lambda_stabilizer - coriolis_distortion
        return stability_impact

    def observer_status(self):
        self.entropy_debt += 0.05
        if self.is_collapsed:
            return "[ SYSTEM DEAD ] - Singularity formed."
        shimmer = random.choice(["*", "+", ".", " "])
        return (f"[{shimmer}] SYS: ONLINE | Dim: {self.n} | "
                f"Lambda: {self.lambda_stabilizer:.4f} | "
                f"Entropy: {self.entropy_debt:.2f}")

# ==========================================
# PART 2: THE MEMORY EXPANSION (MnemosyneCore)
# ==========================================

class MnemosyneCore(DimensionalReactor):
    def __init__(self, memory_file="hypercube_storage.json"):
        # Initialize the Parent Engine
        super().__init__(dimensions=6, ram_allocation_mb=64)
        
        self.memory_file = memory_file
        self.long_term_storage = {} 
        
        # Load existing memory from Disk
        self._resonate_existing_structure()

    def _resonate_existing_structure(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.long_term_storage = json.load(f)
            except Exception as e:
                print(f">>> CORRUPTION DETECTED IN STORAGE: {e}")
        else:
            # Create empty file if none exists
            self._crystallize_lattice()

    def _generate_hash_sig(self, content):
        # Creates a unique ID based on content + physics constants
        raw_sig = f"{content}{self.K_constant}{self.entropy_debt}"
        return hashlib.sha256(raw_sig.encode()).hexdigest()

    def inject_memory(self, input_data, tags=[]):
        if self.is_collapsed:
            return "ERROR: Reactor Collapsed. Cannot Write."
        
        # Entropy Cost
        self.entropy_debt += 0.01 * len(input_data)
        
        # Generate ID
        memory_id = self._generate_hash_sig(input_data)
        
        # Create Data Packet
        packet = {
            "timestamp": str(datetime.now()),
            "data": input_data,
            "tags": tags,
            "energy_state": self.calculate_planck_energy(),
            "stability_lambda": self.lambda_stabilizer
        }
        
        # Save to Dict and Disk
        self.long_term_storage[memory_id] = packet
        print(f"   >>> LATTICE CRYSTALLIZED [ID: {memory_id[:8]}...]")
        self._crystallize_lattice()

    def _crystallize_lattice(self):
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.long_term_storage, f, indent=4)
        except Exception as e:
            print(f"   !!! WRITE ERROR: {e}")

    def query_vortex(self, keyword):
        print(f"   >>> SPINNING UP VORTEX SEARCH FOR: '{keyword}'")
        results = []
        
        # Spin the reactor to "search" (adds simulated load)
        self.spin_interface_protocol(3000)
        
        for mem_id, packet in self.long_term_storage.items():
            if keyword.lower() in packet['data'].lower() or keyword in packet['tags']:
                results.append(packet)
        return results

# ==========================================
# PART 3: MAIN EXECUTION & INTERFACE
# ==========================================

def run_system():
    print("\n--- INITIALIZING HYPERCUBE ARCHITECTURE ---")
    print("--- DETECTING UNKNOWN VARIABLES ---")
    print("... Quantum Noise Floor: DETECTED")
    print("... Chronon Dilation: ACTIVE")
    
    # 1. Initialize the Enhanced Core
    core = MnemosyneCore("hypercube_storage.json")
    
    # 2. Power Up Sequence (Visuals)
    print("\n>>> INITIATING SUMMATION LOOP (Charging)...")
    power_level = 0.5
    for tick in range(3):
        power_level += 2.0 
        status = core.engage_stabilizer(power_level + core._quantum_fluctuation()*100)
        print(f"TICK {tick}: Power={power_level:.2f} -> {status}")
        time.sleep(0.3)
        
    core.generate_isopolymer_lattice()
    
    print(f"\n>>> SYSTEM ONLINE. {len(core.long_term_storage)} Memory Fragments Loaded.")
    print(">>> COMMANDS: [inject <text>], [query <text>], [status], [exit]")
    
    # 3. Interactive Loop
    while True:
        try:
            # Dynamic prompt
            user_input = input("\nroot@hypercube:~# ").strip().split(" ", 1)
            command = user_input[0].lower()
            
            if command == "exit":
                print(">>> TEARING DOWN GEOMETRY...")
                break
                
            elif command == "status":
                print(core.observer_status())
                print(f"   Storage File: {core.memory_file}")
                print(f"   Total Memories: {len(core.long_term_storage)}")
                
            elif command == "inject":
                if len(user_input) < 2:
                    print("   Usage: inject <text to remember>")
                    continue
                data = user_input[1]
                core.inject_memory(data, tags=["user_input"])
                
            elif command == "query":
                if len(user_input) < 2:
                    print("   Usage: query <keyword>")
                    continue
                results = core.query_vortex(user_input[1])
                print(f"   >>> {len(results)} MATCHES FOUND:")
                for res in results:
                    print(f"      [{res['timestamp']}] {res['data']}")
                    
            else:
                print("   UNKNOWN PROTOCOL. System idle.")
                # Idle decay
                core.entropy_debt += 0.01

        except KeyboardInterrupt:
            print("\n>>> MANUAL SCRAM INITIATED.")
            break
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    run_system()