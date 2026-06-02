import os
import json
import time
import hashlib
import math
from datetime import datetime

# --- IMPORTING YOUR ENGINE ---
# If your previous code is in a file named 'python_for_am.py', keep this import.
# If you are pasting this into one big file, just ensure the DimensionalReactor class is defined above.
try:
    from python_for_am import DimensionalReactor
except ImportError:
    # Fallback if running as a standalone script without the previous file
    print(">>> WARNING: Base Reactor Core not found. Initiating Standalone Mode.")
    # (Paste your DimensionalReactor class here if you aren't importing it)
    # For this example, I assume DimensionalReactor exists in the scope.
    pass 

class MnemosyneCore(DimensionalReactor):
    def __init__(self, memory_file="reactor_memory.json"):
        # Initialize the Physics Engine (The Parent Class)
        super().__init__(dimensions=6, ram_allocation_mb=64)
        
        self.memory_file = memory_file
        self.short_term_buffer = []
        self.long_term_storage = {} # The "Expanded" Digital Memory
        
        # Load existing memory if available
        self._resonate_existing_structure()

    def _resonate_existing_structure(self):
        """
        Loads the JSON database from the local device (Disk).
        This connects the Reactor to the local timeline.
        """
        if os.path.exists(self.memory_file):
            print(f">>> DETECTING EXTERNAL LATTICE: {self.memory_file}")
            try:
                with open(self.memory_file, 'r') as f:
                    self.long_term_storage = json.load(f)
                print(f">>> RESONANCE ACHIEVED. {len(self.long_term_storage)} Memories Loaded.")
            except Exception as e:
                print(f">>> CORRUPTION DETECTED: {e}")
        else:
            print(">>> NO EXTERNAL LATTICE FOUND. Initializing fresh core.")

    def _generate_hash_sig(self, content):
        """
        Creates a unique 6-Dimensional ID for the memory using SHA-256
        blended with your Golden Ratio constant.
        """
        raw_sig = f"{content}{self.K_constant}{self.entropy_debt}"
        return hashlib.sha256(raw_sig.encode()).hexdigest()

    def inject_memory(self, input_data, tags=[]):
        """
        ENCAPSULATION PROTOCOL.
        Takes real-world data (strings) and weaves them into the lattice.
        """
        # 1. Check Stability
        if self.is_collapsed:
            return "ERROR: Reactor Collapsed. Cannot Write."
        
        # 2. Calculate Energy Cost (Entropy)
        self.entropy_debt += 0.01 * len(input_data)
        
        # 3. Generate Unique ID (The Coordinate)
        memory_id = self._generate_hash_sig(input_data)
        
        # 4. Create the Packet
        packet = {
            "timestamp": str(datetime.now()),
            "data": input_data,
            "tags": tags,
            "energy_state": self.calculate_planck_energy(),
            "stability_lambda": self.lambda_stabilizer
        }
        
        # 5. Write to RAM (Short Term) and Dict (Long Term)
        self.long_term_storage[memory_id] = packet
        print(f"   >>> MEMORY INJECTED [ID: {memory_id[:8]}...]")
        
        # 6. Crystallize to Disk immediately (Persistence)
        self._crystallize_lattice()

    def _crystallize_lattice(self):
        """
        Writes the RAM state to the Hard Drive (JSON).
        This is the "Expansion" of memory.
        """
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.long_term_storage, f, indent=4)
            # print("   >>> LATTICE CRYSTALLIZED (Saved to Disk).")
        except Exception as e:
            print(f"   !!! WRITE ERROR: {e}")

    def query_vortex(self, keyword):
        """
        Retrieves memories based on keyword resonance.
        """
        print(f"\n>>> SPINNING UP VORTEX SEARCH FOR: '{keyword}'")
        results = []
        
        # Spin the reactor to "search"
        self.spin_interface_protocol(3000)
        
        for mem_id, packet in self.long_term_storage.items():
            if keyword.lower() in packet['data'].lower() or keyword in packet['tags']:
                results.append(packet)
                
        print(f">>> {len(results)} FRAGMENTS LOCATED.")
        return results

# --- THE INTERFACE ---

def activate_memory_console():
    # 1. Initialize the Enhanced Reactor
    mnemosyne = MnemosyneCore("hypercube_storage.json")
    
    # 2. Power Up Sequence (From your original code)
    print("\n--- CHARGING DIMENSIONAL FIELD ---")
    mnemosyne.engage_stabilizer(input_power=10.0)
    mnemosyne.generate_isopolymer_lattice()
    
    print("\n>>> MEMORY INTERFACE READY. COMMANDS: [inject], [query], [status], [exit]")
    
    while True:
        try:
            user_input = input("\nroot@hypercube:~# ").strip().split(" ", 1)
            command = user_input[0].lower()
            
            if command == "exit":
                print(">>> TEARING DOWN GEOMETRY. GOODBYE.")
                break
                
            elif command == "status":
                print(mnemosyne.observer_status())
                print(f"Total Memories Stored: {len(mnemosyne.long_term_storage)}")
                
            elif command == "inject":
                if len(user_input) < 2:
                    print("Usage: inject <text to remember>")
                    continue
                data = user_input[1]
                mnemosyne.inject_memory(data, tags=["user_input"])
                
            elif command == "query":
                if len(user_input) < 2:
                    print("Usage: query <keyword>")
                    continue
                results = mnemosyne.query_vortex(user_input[1])
                for res in results:
                    print(f"   [{res['timestamp']}] :: {res['data']}")
                    
            else:
                print("Unknown Protocol.")
                # Basic reactor tick to keep it "alive"
                mnemosyne._quantum_fluctuation()

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    activate_memory_console()