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
import pyttsx3
from datetime import datetime

# ==========================================
# PART 1: THE PHYSICS ENGINE (DimensionalReactor)
# ==========================================

class DimensionalReactor:
    def __init__(self, dimensions=6, ram_allocation_mb=64):
        self.n = dimensions
        self.G = 6.67430e-11
        self.K_constant = 1.61803 
        self.ram_size = ram_allocation_mb * 1024 * 1024
        
        # System State
        self.lambda_stabilizer = 1.0 # Default to stable
        self.is_collapsed = False
        self.entropy_debt = 0.0 

    def _quantum_fluctuation(self):
        # PATCH: Reduced variance to prevent startup death
        return random.gauss(0, 0.1) 

    def calculate_planck_energy(self):
        return (self.n + 12) / (4 * math.log(2)) + self._quantum_fluctuation()

    def engage_stabilizer(self, input_power):
        # PATCH: Absolute value ensures no negative roots
        input_power = abs(input_power) 
        local_K = self.K_constant + (self.entropy_debt * 0.001)
        
        try:
            root_power = math.sqrt(input_power)
            self.lambda_stabilizer = root_power - local_K
            
            # Soft Failure instead of Hard Death
            if self.lambda_stabilizer < 0:
                self.lambda_stabilizer = 0.01 
                return "WARNING: Low Stability (Auto-Corrected)"
            
            self.is_collapsed = False
            return "STABLE"
        except Exception as e:
            self.is_collapsed = True
            return f"COLLAPSE: {str(e)}"

    def observer_status(self):
        if self.is_collapsed:
            return "[ SYSTEM DEAD ] - Singularity formed. (Type 'reboot' to fix)"
        shimmer = random.choice(["*", "+", ".", " "])
        return (f"[{shimmer}] SYS: ONLINE | Lambda: {self.lambda_stabilizer:.4f} | "
                f"Entropy: {self.entropy_debt:.2f}")

# ==========================================
# PART 2: THE INFINITE MEMORY CORE
# ==========================================

class MnemosyneCore(DimensionalReactor):
    def __init__(self, memory_file="hypercube_storage.json", shard_limit=15):
        super().__init__(dimensions=6, ram_allocation_mb=64)
        self.memory_file = memory_file
        self.long_term_storage = {} 
        self.shard_limit = shard_limit
        self.shard_folder = "reactor_shards"
        
        # Voice (Mac Compatible Try/Except)
        try:
            self.voice_engine = pyttsx3.init()
            self.voice_engine.setProperty('rate', 160)
            self.voice_enabled = True
        except:
            self.voice_enabled = False

        if not os.path.exists(self.shard_folder):
             os.makedirs(self.shard_folder)

        self._resonate_existing_structure()

    def vocalize(self, text):
        if self.voice_enabled:
            threading.Thread(target=self._speak, args=(text,)).start()
    
    def _speak(self, text):
        try:
            eng = pyttsx3.init()
            eng.say(text)
            eng.runAndWait()
        except: pass

    def _resonate_existing_structure(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.long_term_storage = json.load(f)
            except: pass

    def _generate_hash(self, content):
        return hashlib.sha256(f"{content}{time.time()}".encode()).hexdigest()

    def inject_memory(self, input_data, tags=[]):
        if self.is_collapsed:
            return "!!! ERROR: Reactor is Collapsed. Type 'reboot' to reset."
        
        # Remove quotes for cleaner file paths
        clean_path = input_data.replace('"', '').replace("'", "").strip()
        
        is_file = os.path.isfile(clean_path)

        if is_file:
            filename = os.path.basename(clean_path)
            destination = os.path.join(self.shard_folder, filename)
            try:
                shutil.copy2(clean_path, destination)
                self.vocalize(f"Ingesting file artifact: {filename}")
                
                packet = {
                    "type": "FILE_ARTIFACT",
                    "timestamp": str(datetime.now()),
                    "filename": filename,
                    "local_path": destination, 
                    "tags": tags + ["FILE"],
                    "energy": self.calculate_planck_energy()
                }
                msg = f"   >>> [LIBRARIAN] ARTIFACT SECURED: {filename}"
            except Exception as e:
                return f"   !!! FILE ERROR: {e}"
        
        else:
            packet = {
                "type": "ACTIVE_MEMORY",
                "timestamp": str(datetime.now()),
                "data": input_data,
                "tags": tags,
                "energy": self.calculate_planck_energy()
            }
            msg = f"   >>> LATTICE CRYSTALLIZED."

        mem_id = self._generate_hash(str(packet))
        self.long_term_storage[mem_id] = packet
        
        with open(self.memory_file, 'w') as f:
            json.dump(self.long_term_storage, f, indent=4)
            
        return msg

    def query(self, keyword):
        results = []
        for packet in self.long_term_storage.values():
            content = packet.get('data', '') + packet.get('filename', '')
            if keyword.lower() in content.lower():
                results.append(packet)
        return results

# ==========================================
# PART 3: MAIN EXECUTION
# ==========================================

def run_system():
    core = MnemosyneCore()
    print("\n--- HYPERCUBE REACTOR v2.1 (STABILIZED) ---")
    print(">>> POWERING UP...")
    
    # Init Power
    core.engage_stabilizer(10.0)
    print(core.observer_status())
    
    while True:
        try:
            # Fancy input prompt
            user_input = input("\nroot@hypercube:~# ").strip()
            if not user_input: continue
            
            parts = user_input.split(" ", 1)
            cmd = parts[0].lower()
            
            if cmd == "exit":
                print(">>> SHUTTING DOWN.")
                break
                
            elif cmd == "reboot":
                print(">>> RE-ENGAGING STABILIZERS...")
                core.engage_stabilizer(10.0)
                print(">>> SYSTEM RESTORED.")

            elif cmd == "status":
                print(core.observer_status())
                print(f"   Memories: {len(core.long_term_storage)}")

            elif cmd == "inject":
                if len(parts) < 2:
                    print("   Usage: inject <text OR /path/to/file>")
                    continue
                # PRINT THE RESULT (This was missing before)
                result = core.inject_memory(parts[1])
                print(result)

            elif cmd == "query":
                if len(parts) < 2: continue
                res = core.query(parts[1])
                print(f"   >>> FOUND {len(res)} ENTRIES:")
                for r in res:
                    if r['type'] == 'FILE_ARTIFACT':
                        print(f"      [FILE] {r['filename']} @ {r['local_path']}")
                    else:
                        print(f"      [TEXT] {r['data']}")
            
            else:
                print("   UNKNOWN PROTOCOL. Try: inject, query, status, exit")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    run_system()