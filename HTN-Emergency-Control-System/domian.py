# -------------------------
# Primitive Operators
# -------------------------

def call_fire_department(state):
    if state["fire_detected"]:
        state["fire_department_called"] = True
        return state
    return None


def send_ambulance(state):
    if state["injuries_reported"]:
        state["ambulance_sent"] = True
        return state
    return None


def activate_alarm(state):
    if not state["alarm_active"]:
        state["alarm_active"] = True
        return state
    return None


def unlock_exits(state):
    if state["building_locked"]:
        state["building_locked"] = False
        return state
    return None


def evacuate_people(state):
    if state["alarm_active"] and not state["building_locked"]:
        state["people_evacuated"] = True
        return state
    return None


def extinguish_fire(state):
    if state["fire_department_called"]:
        state["fire_detected"] = False
        state["fire_extinguished"] = True
        return state
    return None


def provide_first_aid(state):
    if state["ambulance_sent"]:
        state["injuries_treated"] = True
        return state
    return None


def send_security_team(state):
    if state["security_available"]:
        state["security_dispatched"] = True
        return state
    return None


def call_police(state):
    state["police_called"] = True
    return state


# -------------------------
# Compound Task Methods
# -------------------------

def method_handle_fire_emergency(state):
    if state["emergency_type"] == "fire":
        return [
            ("assess_emergency",),
            ("dispatch_response_team",),
            ("evacuate_building",),
            ("resolve_incident",)
        ]
    return None


def method_handle_medical_emergency(state):
    if state["emergency_type"] == "medical":
        return [
            ("assess_emergency",),
            ("dispatch_response_team",),
            ("resolve_incident",)
        ]
    return None


def method_assess_fire(state):
    if state["fire_detected"]:
        return [
            ("activate_alarm",)
        ]
    return None


def method_assess_medical(state):
    if state["injuries_reported"]:
        return []
    return None


def method_dispatch_fire_team(state):
    if state["fire_detected"]:
        return [
            ("call_fire_department",)
        ]
    return None


def method_dispatch_medical_team(state):
    if state["injuries_reported"]:
        return [
            ("send_ambulance",)
        ]
    return None


def method_dispatch_security_if_available(state):
    if state["security_available"]:
        return [
            ("send_security_team",)
        ]
    return None


def method_dispatch_police_if_no_security(state):
    if not state["security_available"]:
        return [
            ("call_police",)
        ]
    return None


def method_evacuate_locked_building(state):
    if state["building_locked"]:
        return [
            ("unlock_exits",),
            ("evacuate_people",)
        ]
    return None


def method_evacuate_unlocked_building(state):
    if not state["building_locked"]:
        return [
            ("evacuate_people",)
        ]
    return None


def method_resolve_fire(state):
    if state["fire_detected"]:
        return [
            ("extinguish_fire",)
        ]
    return None


def method_resolve_medical(state):
    if state["injuries_reported"]:
        return [
            ("provide_first_aid",)
        ]
    return None


# -------------------------
# Register Domain
# -------------------------

methods = {
    "handle_emergency": [
        method_handle_fire_emergency,
        method_handle_medical_emergency
    ],
    "assess_emergency": [
        method_assess_fire,
        method_assess_medical
    ],
    "dispatch_response_team": [
        method_dispatch_fire_team,
        method_dispatch_medical_team,
        method_dispatch_security_if_available,
        method_dispatch_police_if_no_security
    ],
    "evacuate_building": [
        method_evacuate_locked_building,
        method_evacuate_unlocked_building
    ],
    "resolve_incident": [
        method_resolve_fire,
        method_resolve_medical
    ]
}

operators = {
    "call_fire_department": call_fire_department,
    "send_ambulance": send_ambulance,
    "activate_alarm": activate_alarm,
    "unlock_exits": unlock_exits,
    "evacuate_people": evacuate_people,
    "extinguish_fire": extinguish_fire,
    "provide_first_aid": provide_first_aid,
    "send_security_team": send_security_team,
    "call_police": call_police
}