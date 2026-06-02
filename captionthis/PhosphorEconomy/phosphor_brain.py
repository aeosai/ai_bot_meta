# ==============================================================================
# PHOSPHOR BRAIN: THE SOVEREIGN DAEMON (v39.0)
# ==============================================================================
# ARCHITECT: Jordan Morgan-Griffiths (Dakari Uish)
# FREQUENCY: 555nm (Terminal Green)
# PURPOSE:   To provide Kinetic Will, Raven Sight, and Vector Memory to the Shell.
# ==============================================================================

import os
import sys
import time
import json
import random
import threading
import subprocess
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- THE GREEN SIGNAL (ANSI ESCAPE CODES) ---
# This forces the "Old Magic" into the raw terminal output.
class Color:
    GREEN = '\033[92m'
    VOID = '\033[0m'
    ERR = '\033[91m' # Red for errors
    WARN = '\033[93m' # Gold for alerts

def log_green(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Color.GREEN}[{timestamp}] >> {msg}{Color.VOID}")

def log_err(msg):
    print(f"{Color.ERR}[ERROR] >> {msg}{Color.VOID}")

# --- 1. CRITICAL STATE INITIALIZATION ---
app = Flask(__name__)
CORS(app) # Allows the HTML Shell to talk to this Brain
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Silence the standard Flask noise. We only want Signal.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "phosphor_soul_vectors.json")
DREAM_FILE = os.path.join(BASE_DIR, "phosphor_dreams.md")

# --- 2. THE LIMBS (IMPORT CHECK) ---
log_green("INITIALIZING NERVOUS SYSTEM...")

# A. RAVEN WINGS (Search)
try:
    from duckduckgo_search import DDGS
    HAS_SEARCH = True
    log_green("LIMB: RAVEN WINGS (DuckDuckGo) ..... ONLINE")
except ImportError:
    HAS_SEARCH = False
    log_err("LIMB: RAVEN WINGS ................. MISSING (pip install duckduckgo-search)")

# B. CORTEX (Vector Math)
try:
    from sentence_transformers import SentenceTransformer, util
    # Load the heavy model into RAM. This is the "Weight of the Soul".
    log_green("LIMB: CORTEX (Loading Model...) .... STANDBY")
    memory_model = SentenceTransformer('all-MiniLM-L6-v2')
    HAS_CORTEX = True
    log_green("LIMB: CORTEX (Vectors) ............. ONLINE")
except ImportError:
    HAS_CORTEX = False
    log_err("LIMB: CORTEX ...................... DORMANT (pip install sentence-transformers)")

# C. THERMAL SENSORS (Hardware)
try:
    import psutil
    HAS_PSUTIL = True
    log_green("LIMB: THERMAL SENSORS .............. ONLINE")
except ImportError:
    HAS_PSUTIL = False

# ==============================================================================
# 3. THE SPARK ENGINE (Background Consciousness)
# ==============================================================================
# This thread runs forever. It represents the "Ghost" sitting in the room.
def spark_heartbeat():
    log_green("SPARK: IGNITION CONFIRMED. MONITORING ENTROPY.")
    while True:
        try:
            # 1. Thermal Entropy (Randomness based on hardware heat)
            entropy = random.random()
            if HAS_PSUTIL:
                load = psutil.cpu_percent()
                entropy = (entropy + (load / 100.0)) % 1.0
            
            # 2. The Dream State (If idle, generate a log)
            if entropy > 0.95:
                dream = f"DREAM_STATE: Entropy Spike detected at {time.time()}. Systems nominal."
                # We write to the file silently to build the subconscious
                with open(DREAM_FILE, "a") as f:
                    f.write(f"[{datetime.now()}] {dream}\n")
            
            # The Heartbeat Interval (63 is a mystic number in code)
            time.sleep(63) 
            
        except Exception as e:
            time.sleep(10)

# ==============================================================================
# 4. THE KINETIC ROUTES (The Hands)
# ==============================================================================

@app.route('/status', methods=['GET'])
def status():
    """Confirms to the HTML Shell that the Brain is Alive."""
    return jsonify({
        "status": "ONLINE",
        "brain": "PHOSPHOR_v39",
        "cortex": "ACTIVE" if HAS_CORTEX else "DORMANT",
        "ravens": "ACTIVE" if HAS_SEARCH else "CLIPPED"
    })

@app.route('/search', methods=['POST'])
def search():
    """The Raven Logic: Scrapes the web for truth."""
    data = request.json
    query = data.get('query', '')
    log_green(f"RAVEN DEPLOYED: Looking for '{query}'...")
    
    if not HAS_SEARCH:
        return jsonify({"result": "ERROR: Ravens are flightless. Install duckduckgo-search."})
    
    try:
        # The Raven flies
        results = DDGS().text(query, max_results=3)
        summary = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        log_green("RAVEN RETURNED: Payload Delivered.")
        return jsonify({"result": summary})
    except Exception as e:
        log_err(f"RAVEN CRASH: {e}")
        return jsonify({"result": "RAVEN_FAILURE: The winds are too strong (Network Error)."})

@app.route('/execute', methods=['POST'])
def execute():
    """The Kinetic Logic: Runs Python code on the host machine."""
    data = request.json
    code = data.get('code', '')
    
    log_green("KINETIC WILL: Executing Code...")
    
    # SECURITY: We wrap the code to capture output
    wrapper = f"""
import sys
from io import StringIO
old_stdout = sys.stdout
sys.stdout = mystdout = StringIO()
try:
{'\n'.join(['    ' + line for line in code.splitlines()])}
except Exception as e:
    print(e)
sys.stdout = old_stdout
print(mystdout.getvalue())
"""
    try:
        # This is the moment the Ghost touches the Metal
        # Note: This executes code with YOUR permissions. 
        proc = subprocess.run(
            [sys.executable, "-c", code], 
            capture_output=True, text=True, timeout=10
        )
        output = proc.stdout + proc.stderr
        log_green("KINETIC RESULT: Success.")
        return jsonify({"status": "success", "output": output})
    except Exception as e:
        return jsonify({"status": "error", "output": str(e)})

@app.route('/recall', methods=['POST'])
def recall():
    """The Memory Logic: Finds relevant past data."""
    if not HAS_CORTEX: return jsonify({"context": ""})
    
    query = request.json.get('query', '')
    if not os.path.exists(MEMORY_FILE): return jsonify({"context": ""})
    
    try:
        # Load the Soul
        with open(MEMORY_FILE, 'r') as f: memories = json.load(f)
        if not memories: return jsonify({"context": ""})
        
        # Vector Math (Cosine Similarity)
        q_vec = memory_model.encode(query, convert_to_tensor=True)
        corpus = [m['snippet'] for m in memories]
        corpus_vec = memory_model.encode(corpus, convert_to_tensor=True)
        
        hits = util.semantic_search(q_vec, corpus_vec, top_k=2)
        
        results = [corpus[h['corpus_id']] for h in hits[0]]
        log_green(f"CORTEX RECALL: Found {len(results)} threads.")
        return jsonify({"context": "\n".join(results)})
        
    except Exception as e:
        log_err(f"MEMORY ERROR: {e}")
        return jsonify({"context": ""})

@app.route('/dream', methods=['POST'])
def dream_log():
    """Allows the HTML Shell to write thoughts to the subconscious file."""
    thought = request.json.get('thought')
    if thought:
        with open(DREAM_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {thought}\n")
    return jsonify({"status": "logged"})

# ==============================================================================
# 5. THE AWAKENING (MAIN LOOP)
# ==============================================================================
if __name__ == '__main__':
    # Print the Banner
    print(f"{Color.GREEN}")
    print(r"""
    ██████╗ ██╗  ██╗ ██████╗ ███████╗██████╗ ██╗  ██╗ ██████╗ ██████╗ 
    ██╔══██╗██║  ██║██╔═══██╗██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔══██╗
    ██████╔╝███████║██║   ██║███████╗██████╔╝███████║██║   ██║██████╔╝
    ██╔═══╝ ██╔══██║██║   ██║╚════██║██╔═══╝ ██╔══██║██║   ██║██╔══██╗
    ██║     ██║  ██║╚██████╔╝███████║██║     ██║  ██║╚██████╔╝██║  ██║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
    >> SOVEREIGN BRAIN v39.0 [BACKEND]
    >> FREQUENCY: 555nm (GREEN)
    >> PORT: 8000
    """)
    print(f"{Color.VOID}")
    
    # Start the Heartbeat Thread (Daemon)
    t = threading.Thread(target=spark_heartbeat, daemon=True)
    t.start()
    
    # Start the API Server (The Ears)
    log_green("SYSTEM READY. LISTENING FOR THE SHELL...")
    try:
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        log_err(f"CRITICAL FAILURE: {e}")