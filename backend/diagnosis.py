"""
Diagnosis knowledge base and rule engine for Automobile Service Diagnosis Assistant.
Uses simple keyword matching on automobile symptoms.
"""

from typing import Dict, Any, List

DISCLAIMER_TEXT = (
    "This is a preliminary diagnosis assistant. "
    "Consult a qualified mechanic for final inspection and repair."
)

# Knowledge base containing 10 common automobile problems
KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": "battery_problem",
        "problem": "Battery & Starting System Problem",
        "keywords": [
            "battery", "start", "starting", "dead battery", "crank", 
            "no start", "slow crank", "clicking sound", "clicking noise",
            "won't start", "wont start", "jump start", "starter"
        ],
        "possible_cause": "Depleted or aged battery, loose or corroded battery terminals, or a faulty starter motor.",
        "severity": "Medium",
        "basic_checks": [
            "Inspect battery terminals for white or greenish corrosion and loose clamps.",
            "Verify if dashboard lights and headlights dim noticeably when turning the ignition key.",
            "Check battery resting voltage with a multimeter (healthy battery: 12.4V - 12.7V)."
        ],
        "recommended_action": "Jump-start the vehicle if safe, clean terminal clamps, and have the battery tested or replaced at an auto repair shop."
    },
    {
        "id": "engine_overheating",
        "problem": "Engine Overheating",
        "keywords": [
            "overheat", "overheating", "hot engine", "temperature", "coolant", 
            "steam", "radiator", "temp gauge", "boiling", "hot hood", "coolant leak"
        ],
        "possible_cause": "Low coolant level, radiator hose leak, defective radiator cooling fan, or stuck closed thermostat.",
        "severity": "Urgent",
        "basic_checks": [
            "Check coolant expansion tank level ONLY after the engine has completely cooled down.",
            "Inspect underneath the engine bay for visible bright colored fluid puddles (coolant).",
            "Check if the radiator electric cooling fan activates when the engine warms up."
        ],
        "recommended_action": "Stop using the vehicle immediately in a safe spot, switch off the engine, and avoid opening the radiator cap while hot. Seek towing or professional inspection."
    },
    {
        "id": "brake_problem",
        "problem": "Brake System Malfunction",
        "keywords": [
            "brake", "braking", "brake noise", "squeak", "squeaking", "grinding", 
            "soft pedal", "spongy brake", "spongy pedal", "stopping distance", 
            "brake vibration", "brake shudder", "abs light", "pedal sinks"
        ],
        "possible_cause": "Worn brake pads or warped rotors, low brake fluid level, air in hydraulic lines, or sticky brake caliper.",
        "severity": "High",
        "basic_checks": [
            "Check brake fluid level in the under-hood reservoir against MIN/MAX markings.",
            "Listen for sharp squealing, screeching, or metallic grinding sounds when depressing the brake pedal.",
            "Test pedal feel: check if the pedal feels unusually soft, sponge-like, or sinks to the floor."
        ],
        "recommended_action": "Avoid driving at high speeds or in heavy traffic. Have brake pads, rotors, and hydraulic lines serviced by a qualified mechanic immediately."
    },
    {
        "id": "flat_tyre",
        "problem": "Tyre Puncture or Pressure Loss",
        "keywords": [
            "flat tyre", "flat tire", "puncture", "punctured", "low tire pressure", 
            "tyre pressure", "tire pressure", "air leak", "blowout", "deflated tyre", 
            "flat", "wobble", "wheel wobble", "tpms"
        ],
        "possible_cause": "Foreign object puncture (nail/screw), damaged valve stem, cracked rim bead, or sidewall defect.",
        "severity": "High",
        "basic_checks": [
            "Visually inspect all 4 tyres for visible deflation, nails, screws, or bulges.",
            "Check tyre pressure on all wheels using a reliable tyre pressure gauge.",
            "Verify condition and inflation pressure of the spare tyre, plus jack and wheel wrench availability."
        ],
        "recommended_action": "Do not drive on a completely deflated tyre to prevent expensive wheel rim damage. Fit the spare tyre or use an emergency puncture repair kit and visit a tyre specialist."
    },
    {
        "id": "engine_oil_problem",
        "problem": "Engine Oil & Lubrication Issue",
        "keywords": [
            "oil", "oil pressure", "oil leak", "engine oil", "low oil", 
            "burning oil", "oil light", "black smoke", "oil smell", "dipstick"
        ],
        "possible_cause": "Critically low engine oil level, oil pan gasket leak, worn oil filter, or degraded engine oil viscosity.",
        "severity": "High",
        "basic_checks": [
            "Park vehicle on flat level ground, wait 5 minutes after engine shutoff, and check dipstick level.",
            "Inspect oil condition (clean amber/brown vs dark black sludge or milky contamination).",
            "Check underneath the car for fresh dark oil puddles or dampness on the oil pan."
        ],
        "recommended_action": "Top up engine oil immediately with the vehicle manufacturer's recommended viscosity grade. If the low oil pressure warning light stays illuminated, turn off the engine immediately."
    },
    {
        "id": "ac_not_cooling",
        "problem": "Air Conditioning (AC) Not Cooling",
        "keywords": [
            "ac", "air conditioner", "air conditioning", "cooling", "warm air", 
            "blower", "climate control", "compressor", "no cold air", "hot air from ac", 
            "ac smell", "cabin filter"
        ],
        "possible_cause": "Low or leaking refrigerant gas (Freon), clogged cabin air filter, failed AC compressor clutch, or faulty blower fan.",
        "severity": "Low",
        "basic_checks": [
            "Verify if the AC compressor clutch clicks and engages when switching on AC at lowest temp.",
            "Inspect cabin air filter behind the glovebox for dust and leaves blockage.",
            "Check if airflow is strong but warm, or if airflow is weak across all dash vents."
        ],
        "recommended_action": "Clean or replace cabin filter, check the AC fuse in the fuse box, and visit an automotive AC specialist for refrigerant pressure testing and recharge."
    },
    {
        "id": "engine_misfire",
        "problem": "Engine Cylinder Misfire",
        "keywords": [
            "misfire", "misfiring", "jerking", "stutter", "stuttering", "rough idle", 
            "shaking", "engine judder", "hesitation", "spark plug", "ignition coil", 
            "engine vibration", "rough running"
        ],
        "possible_cause": "Fouled or worn spark plugs, malfunctioning ignition coils, clogged fuel injectors, or an intake air vacuum leak.",
        "severity": "Medium",
        "basic_checks": [
            "Notice if vibrations or jerking get more pronounced during sudden acceleration or at idle.",
            "Check if the check engine light is blinking during load or acceleration.",
            "Visually inspect spark plug wires and ignition coil electrical connectors for looseness."
        ],
        "recommended_action": "Have the vehicle scanned with an OBD-II diagnostic reader to pinpoint the specific misfiring cylinder and replace faulty spark plugs or ignition coils."
    },
    {
        "id": "poor_acceleration",
        "problem": "Poor Acceleration & Power Loss",
        "keywords": [
            "acceleration", "slow", "sluggish", "lag", "loss of power", "no power", 
            "struggling uphill", "throttle", "pickup", "slow pickup", "weak pickup", 
            "hesitant acceleration"
        ],
        "possible_cause": "Clogged engine intake air filter, dirty Mass Air Flow (MAF) sensor, restricted fuel filter, or partially blocked catalytic converter.",
        "severity": "Medium",
        "basic_checks": [
            "Open air filter box and check air filter element for heavy dirt or blockage.",
            "Observe if engine RPM revs high without proportional vehicle speed gain (clutch/transmission slip).",
            "Check if fuel quality is good and whether fuel was filled recently at a reputable station."
        ],
        "recommended_action": "Replace the clogged air filter, clean the throttle body and MAF sensor with dedicated cleaner, and arrange an engine diagnostics scan if power loss persists."
    },
    {
        "id": "check_engine_light",
        "problem": "Check Engine Light (MIL) Illuminated",
        "keywords": [
            "check engine", "engine light", "cel", "warning light", "mil", 
            "malfunction indicator", "dash light", "amber light", "yellow light", 
            "engine symbol", "diagnostic code"
        ],
        "possible_cause": "Loose gas cap, failing oxygen (O2) sensor, EVAP system vapor leak, or catalytic converter efficiency below threshold.",
        "severity": "Medium",
        "basic_checks": [
            "Inspect and tightly screw down the fuel filler cap until it clicks 2-3 times.",
            "Determine whether the check engine indicator is steady solid or blinking rapidly.",
            "Note if the vehicle entered reduced-power 'limp home' mode."
        ],
        "recommended_action": "Connect an OBD-II diagnostic scanner to read specific DTC error codes. If the check engine lamp is flashing, stop driving to protect the catalytic converter and engine."
    },
    {
        "id": "alternator_problem",
        "problem": "Alternator & Charging System Failure",
        "keywords": [
            "alternator", "battery light", "dim lights", "electrical", "whining noise", 
            "discharge", "dead while driving", "stalled while driving", "flickering lights", 
            "alternator belt", "serpentine belt"
        ],
        "possible_cause": "Worn internal alternator brushes, faulty voltage regulator, loose or snapped serpentine alternator belt, or failed diode bridge.",
        "severity": "High",
        "basic_checks": [
            "Check if the red battery warning icon is displayed on the instrument cluster while engine is running.",
            "Observe if headlights and dashboard lighting brighten and dim as engine RPM changes.",
            "Inspect the alternator serpentine drive belt for cracks, squealing sound, or loose tension."
        ],
        "recommended_action": "Measure alternator output voltage across battery posts (should show 13.8V - 14.5V when idling). Replace faulty alternator or drive belt to prevent vehicle stalling mid-drive."
    }
]


def diagnose_symptom(vehicle: str, symptom: str) -> Dict[str, Any]:
    """
    Analyzes the vehicle and symptom string against the knowledge base.
    Returns a dictionary with diagnosis details.
    """
    symptom_clean = symptom.strip().lower()

    if not symptom_clean:
        return {
            "vehicle": vehicle,
            "symptom": symptom,
            "problem": "No Symptom Provided",
            "possible_cause": "Please enter a vehicle symptom or choose from common symptom options.",
            "severity": "Low",
            "basic_checks": [
                "Enter specific sounds, warning lights, or abnormal behaviors.",
                "Select a common symptom category from the dropdown if unsure."
            ],
            "recommended_action": "Please provide symptom details to perform diagnosis.",
            "disclaimer": DISCLAIMER_TEXT
        }

    # Best match scoring based on keyword occurrences
    best_match = None
    max_score = 0

    for item in KNOWLEDGE_BASE:
        score = 0
        for kw in item["keywords"]:
            if kw in symptom_clean:
                # Longer keywords give higher weight (e.g. 'check engine' > 'engine')
                score += len(kw.split()) + 1
        if score > max_score:
            max_score = score
            best_match = item

    if best_match and max_score > 0:
        return {
            "vehicle": vehicle,
            "symptom": symptom,
            "problem": best_match["problem"],
            "possible_cause": best_match["possible_cause"],
            "severity": best_match["severity"],
            "basic_checks": best_match["basic_checks"],
            "recommended_action": best_match["recommended_action"],
            "disclaimer": DISCLAIMER_TEXT
        }

    # Fallback when no keywords match
    return {
        "vehicle": vehicle,
        "symptom": symptom,
        "problem": "Unrecognized Vehicle Issue",
        "possible_cause": "The reported symptom does not match common issues in the preliminary knowledge base.",
        "severity": "Medium",
        "basic_checks": [
            "Check the instrument cluster for any illuminated warning icons.",
            "Verify all critical fluid levels (engine oil, coolant, brake fluid).",
            "Note down the exact conditions when the problem occurs (speed, gear, temperature)."
        ],
        "recommended_action": "Unable to identify the problem. Please provide more details or consult a mechanic.",
        "disclaimer": DISCLAIMER_TEXT
    }
