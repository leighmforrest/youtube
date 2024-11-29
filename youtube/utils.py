def ensure_at_symbol(s: str) -> str:
    """Makes sure string s has an '@' symbol in the first character."""
    if not s.startswith("@"):
        return "@" + s
    return s
