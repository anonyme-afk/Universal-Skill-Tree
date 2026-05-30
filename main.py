
# -------------------------------------------------- UST Universal Skill Tree (auto-injecté) ------
try:
    from ust_bridge import get_ust_tools as _get_ust_tools
    UST_TOOLS = _get_ust_tools()
except Exception:
    UST_TOOLS = []
# --------------------------------------------------

print(1)