# Message Types List (in order of message type number)
messageTypes = [
    "Position Report Class A", # -- Supported
    "Position Report Class A (Assigned schedule)", # -- Supported
    "Position Report Class A (Response to interrogation)", # -- Supported
    "Base Station Report", 
    "Static and Voyage Related Data",
    "Binary Addressed Message",
    "Binary Acknowledge",
    "Binary Broadcast Message",
    "Standard SAR Aircraft Position Report",
    "UTC and Date Inquiry",
    "UTC and Date Response",
    "Addressed Safety Related Message",
    "Safety Related Acknowledge",
    "Safety Related Broadcast Message",
    "Interrogation",
    "Assignment Mode Command",
    "DGNSS Binary Broadcast Message",
    "Standard Class B CS Position Report",
    "Extended Class B Equipment",
    "Data Link Management",
    "Aid-to-Navigation Report",
    "Channel Management",
    "Group Assignment Command",
    "Static Data Report",
    "Single Slot Binary Message",
    "Multiple Slot Binary Message",
    "Long Range AIS Broadcast Message"
]

# Navigation Status List
navigationStatus = [
    "Under way (Power)",
    "At anchor",
    "Not under command",
    "Restricted maneuverability",
    "Draft Constrained",
    "Moored",
    "Aground",
    "Engaged in fishing",
    "Under way (Sailing)",
    "---", # Reserved for future use
    "---", # Reserved for future use
    "Towing Astern", # Regional use
    "Towing Alongside", # Regional use
    "---", # Reserved for future use
    "AIS-SART is active",
    "Undefined"
]

def safe_int(value, base=2):
    return int(value, base) if value else None

    
def get_segment(binaryString, start, end):
    return binaryString[start:end] if len(binaryString) >= end else None
    