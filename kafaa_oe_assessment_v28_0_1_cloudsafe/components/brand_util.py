
import streamlit as st
def effective_brand_mode() -> str:
    """Return the brand mode considering project override and global default."""
    if st.session_state.get('brand_mode_override', False):
        return st.session_state.get('brand_mode_project', st.session_state.get('brand_mode_global', 'Kafaa'))
    # Backward compatibility: if an explicit export-time selection exists, honor it temporarily
    if 'brand_mode' in st.session_state:
        return st.session_state['brand_mode']
    return st.session_state.get('brand_mode_global', 'Kafaa')


def accent_color_hex() -> str:
    """Return hex accent color based on brand mode, defense visuals, and token choice/profile."""
    import streamlit as st
    # Manual token wins
    token = st.session_state.get('accent_token_choice', 'Auto (by profile)')
    profile = st.session_state.get('profile_key','default')
    use_def = st.session_state.get('use_defense_visuals', False)
    # Token palette
    TOKENS = {
        'Kafaa Teal': '#117B77',
        'Defense Navy': '#0B3D91',
        'Automotive Blue': '#1E5AA0',
        'Electronics Indigo': '#3949AB',
        'Pharma Indigo': '#3F51B5',
        'Food & Beverage Green': '#2E7D32',
        'Metal Fab Slate': '#24303C',
        'Neutral Slate': '#4A4A4A',
    }
    if token != 'Auto (by profile)':
        return TOKENS.get(token, '#117B77')
    # Auto by profile
    if profile.startswith('defense') and use_def:
        return '#0B3D91'
    if 'metal' in profile: return '#24303C'
    if 'electronic' in profile: return '#3949AB'
    if 'pharma' in profile: return '#3F51B5'
    if 'automotive' in profile: return '#1E5AA0'
    if 'food' in profile or 'beverage' in profile: return '#2E7D32'
    return '#117B77'
