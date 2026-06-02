import time
import math
import random
import hashlib
import sys
import threading
import os
import json
import gzip
import shutil
from datetime import datetime

# ==========================================
# PART 1: THE PHYSICS ENGINE (DimensionalReactor)
# ==========================================
# (Unchanged from your provided build - The Engine Room)

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
# PART 2: THE INFINITE MEMORY CORE (Mnemosyne Phase 3)
# ==========================================

class MnemosyneCore(DimensionalReactor):
    def __init__(self, memory_file="hypercube_storage.json", shard_limit=15):
        # Initialize the Parent Engine
        super().__init__(dimensions=6, ram_allocation_mb=64)
        
        self.memory_file = memory_file
        self.long_term_storage = {} 
        self.shard_limit = shard_limit
        
        # --- PATHFINDING PROTOCOL (Looking for Google Drive) ---
        print(">>> INITIALIZING PATHFINDING PROTOCOL...")
        
        # Potential mounting points for Google Drive
        possible_paths = [
            r"G:\My Drive\Hypercube_Vault",             # Windows Default
            r"G:\Other Computers\My Laptop\Hypercube_Vault", 
            os.path.expanduser("~/Google Drive/Hypercube_Vault"), # Mac Legacy
            "/Volumes/GoogleDrive/My Drive/Hypercube_Vault"       # Mac Modern
        ]
        
        self.shard_folder = "reactor_shards" # Default fallback (Local)
        found_cloud = False
        
        for path in possible_paths:
            # Check if the parent directory (The Drive) exists
            if os.path.exists(os.path.dirname(path)):
                self.shard_folder = path
                found_cloud = True
                print(f"   >>> CLOUD UPLINK ESTABLISHED: {self.shard_folder}")
                break
        
        if not found_cloud:
            print("   >>> NO CLOUD SIGNAL. ENGAGING LOCAL STORAGE MODE.")
            if not os.path.exists(self.shard_folder):
                os.makedirs(self.shard_folder)

        # Load existing memory
        self._resonate_existing_structure()

    def _resonate_existing_structure(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.long_term_storage = json.load(f)
            except Exception as e:
                print(f">>> CORRUPTION DETECTED IN STORAGE: {e}")
        else:
            self._crystallize_lattice()

    def _generate_hash_sig(self, content):
        raw_sig = f"{content}{self.K_constant}{self.entropy_debt}"
        return hashlib.sha256(raw_sig.encode()).hexdigest()

    # --- THE ENTANGLEMENT PROTOCOL (Sharding) ---
    def _entangle_offload(self):
        """
        Moves excess memories from Local RAM to the Cloud Vault.
        """
        print("\n   >>> ! CRITICAL MASS REACHED. INITIATING SHARD OFFLOAD...")
        
        # 1. Sort memories by age (Oldest first)
        sorted_keys = sorted(self.long_term_storage.keys(), 
                             key=lambda x: self.long_term_storage[x].get('timestamp', '0'))
        
        # Filter only Active memories (ignore existing ghosts)
        active_keys = [k for k in sorted_keys if self.long_term_storage[k].get('type') != 'GHOST_REFERENCE']
        
        # If we barely have enough, don't shard yet
        if len(active_keys) < 5: return

        # 2. Select the oldest 40% to move
        split_index = int(len(active_keys) * 0.4)
        keys_to_move = active_keys[:split_index]
        
        shard_data = {}
        shard_filename = f"sector_{int(time.time())}.shard.gz"
        
        for k in keys_to_move:
            # Copy data to shard packet
            shard_data[k] = self.long_term_storage[k]
            
            # Replace local data with a Ghost Reference
            self.long_term_storage[k] = {
                "type": "GHOST_REFERENCE",
                "timestamp": self.long_term_storage[k]['timestamp'],
                "location": f"{self.shard_folder}/{shard_filename}",
                "original_hash": k,
                "preview": self.long_term_storage[k]['data'][:30] + "..." # Keep a snippet
            }
            
        # 3. Crystallize Shard (Compress and Write to Drive)
        shard_path = os.path.join(self.shard_folder, shard_filename)
        try:
            with gzip.open(shard_path, 'wt', encoding='utf-8') as f:
                json.dump(shard_data, f)
            print(f"   >>> SHARD BEAMED TO: {shard_filename}")
            print(f"   >>> {len(keys_to_move)} MEMORIES TRANSFERRED TO DEEP STORAGE.")
        except Exception as e:
            print(f"   !!! SHARD FAILURE: {e}")

    def inject_memory(self, input_data, tags=[]):
        if self.is_collapsed:
            return "ERROR: Reactor Collapsed. Cannot Write."
        
        self.entropy_debt += 0.01 * len(input_data)
        memory_id = self._generate_hash_sig(input_data)
        
        packet = {
            "type": "ACTIVE_MEMORY",
            "timestamp": str(datetime.now()),
            "data": input_data,
            "tags": tags,
            "energy_state": self.calculate_planck_energy(),
            "stability_lambda": self.lambda_stabilizer
        }
        
        self.long_term_storage[memory_id] = packet
        print(f"   >>> LATTICE CRYSTALLIZED [ID: {memory_id[:8]}...]")
        
        # CHECK CAPACITY
        active_count = sum(1 for v in self.long_term_storage.values() if v.get('type') == 'ACTIVE_MEMORY')
        if active_count > self.shard_limit:
            self._entangle_offload()
            
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
        self.spin_interface_protocol(3000)
        
        for mem_id, packet in self.long_term_storage.items():
            # Check Active Memories
            if packet.get('type') == 'ACTIVE_MEMORY':
                if keyword.lower() in packet['data'].lower() or keyword in packet['tags']:
                    results.append(packet)
            
            # Check Ghost References
            elif packet.get('type') == 'GHOST_REFERENCE':
                # We check the preview snippet
                if keyword.lower() in packet.get('preview', '').lower():
                    results.append(packet)
                    
        return results

# ==========================================
# PART 3: MAIN EXECUTION & INTERFACE
# ==========================================

def run_system():
    print("\n--- INITIALIZING HYPERCUBE ARCHITECTURE (PHASE 3) ---")
    print("--- DETECTING UNKNOWN VARIABLES ---")
    print("... Quantum Noise Floor: DETECTED")
    print("... Chronon Dilation: ACTIVE")
    
    # 1. Initialize the Enhanced Core
    core = MnemosyneCore("hypercube_storage.json", shard_limit=15)
    
    # 2. Power Up Sequence
    print("\n>>> INITIATING SUMMATION LOOP (Charging)...")
    power_level = 0.5
    for tick in range(3):
        power_level += 2.0 
        status = core.engage_stabilizer(power_level + core._quantum_fluctuation()*100)
        print(f"TICK {tick}: Power={power_level:.2f} -> {status}")
        time.sleep(0.3)
        
    core.generate_isopolymer_lattice()
    
    # Calculate Total Memories (Active + Offworld)
    active = sum(1 for v in core.long_term_storage.values() if v.get('type') == 'ACTIVE_MEMORY')
    ghosts = sum(1 for v in core.long_term_storage.values() if v.get('type') == 'GHOST_REFERENCE')
    
    print(f"\n>>> SYSTEM ONLINE.")
    print(f">>> LOCAL CACHE: {active} Fragments")
    print(f">>> DEEP STORAGE: {ghosts} Entanglements")
    print(">>> COMMANDS: [inject <text>], [query <text>], [status], [exit]")
    
    # 3. Interactive Loop
    while True:
        try:
            user_input = input("\nroot@hypercube:~# ").strip().split(" ", 1)
            command = user_input[0].lower()
            
            if command == "exit":
                print(">>> TEARING DOWN GEOMETRY...")
                break
                
            elif command == "status":
                print(core.observer_status())
                print(f"   Vault Location: {core.shard_folder}")
                print(f"   Total Index: {len(core.long_term_storage)}")
                
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
                    if res.get('type') == 'GHOST_REFERENCE':
                        print(f"      [OFFWORLD ARCHIVE] {res['preview']} (Stored in: {res['location']})")
                    else:
                        print(f"      [{res['timestamp']}] {res['data']}")
                    
            else:
                print("   UNKNOWN PROTOCOL. System idle.")
                core.entropy_debt += 0.01

        except KeyboardInterrupt:
            print("\n>>> MANUAL SCRAM INITIATED.")
            break
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    run_system()