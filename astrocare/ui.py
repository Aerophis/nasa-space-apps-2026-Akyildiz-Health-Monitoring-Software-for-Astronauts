"""Shared presentation styles; no data or storage behavior lives here."""

import streamlit as st
from string import Template

from astrocare.theme import COLORS


def choice_key(name, language):
    """Keep existing English widget keys, remount formatted options for other locales."""
    return name if language == "en" else f"{name}__{language}"


def _remember_choice(name, key):
    st.session_state[f"_selection_{name}"] = st.session_state[key]


def localized_choice(renderer, label, options, *, name, language, initial, **kwargs):
    """Locale-specific frontend identity, language-independent selection state.

    Some native choice widgets retain cached selected labels when only their
    format function changes. Recreate those widgets without discarding choices.
    """
    key = choice_key(name, language)
    value_key = f"_selection_{name}"
    locale_key = f"_selection_language_{name}"
    if st.session_state.get(locale_key) != language or key not in st.session_state:
        st.session_state[key] = st.session_state.get(value_key, initial)
    st.session_state[locale_key] = language
    value = renderer(label, options, key=key, on_change=_remember_choice, args=(name, key), **kwargs)
    st.session_state[value_key] = value
    return value


def apply_theme():
    styles = Template("""<style>
    :root {color-scheme: dark;}
    .stApp {background: $background; color: $text;}
    [data-testid="stHeader"] {background: $background;}
    [data-testid="stSidebar"] {background: $surface; border-right: 1px solid $border;}
    .stMainBlockContainer {max-width: 1440px; padding-top: 2.5rem; padding-bottom: 2rem;}
    .stApp p, .stApp li, .stApp label {font-size: 1rem; line-height: 1.55;}
    .stApp h1 {font-size: 2.6rem; letter-spacing: -.035em; color: $text;}
    .stApp h2 {font-size: 1.6rem; letter-spacing: -.02em; color: $text;}
    .stApp h3 {font-size: 1.2rem; color: $text;}
    .stApp [data-testid="stCaptionContainer"] p {color: $secondary; font-size: .95rem; opacity: 1;}
    .stApp [data-testid="stWidgetLabel"] p {color: $text;}
    .stApp a {color: $sleep;}
    [data-testid="stMetric"] {background: $card; border: 1px solid $border;
        border-radius: 12px; padding: 1.15rem; min-height: 148px;}
    .stApp [data-testid="stMetricValue"] p {font-size: 2rem; line-height: 1.25; color: $text;}
    [data-testid="stMetricDelta"] {color: $secondary;}
    [data-testid="stExpander"] {background: $surface; border-color: $border; border-radius: 10px;}
    [data-testid="stTabs"] [role="tab"] {font-size: 1rem; padding: .75rem .2rem;}
    [data-testid="stTabs"] [role="tablist"] {gap: 1.5rem;}
    [data-testid="stPlotlyChart"] {outline: 1px solid $border; border-radius: 12px;
        background: $surface; overflow: hidden;}
    [data-testid="stPlotlyChart"] .modebar .icon path {fill: $secondary;}
    [data-testid="stMultiSelect"] .react-aria-ComboBox > [role="group"] {
        background: $surface; border: 1px solid $control_border; border-radius: 8px;}
    [data-testid="stMultiSelectTagsContainer"] > [role="group"] {gap: .4rem;}
    [data-testid="stMultiSelect"] [data-tag] {
        background: $chip !important; color: $text !important;
        border: 1px solid $control_border; border-radius: 6px;
        padding: .3rem .5rem; gap: .4rem;}
    [data-testid="stMultiSelect"] [data-tag] > span {
        color: $text !important; font-size: .95rem; line-height: 1.4;}
    [data-testid="stMultiSelect"] [data-tag]:hover {border-color: $focus;}
    [data-testid="stMultiSelect"] [data-tag] button {
        color: $text !important; opacity: 1; min-width: 24px; min-height: 24px;
        border-radius: 4px; background: transparent;}
    [data-testid="stMultiSelect"] [data-tag] button svg {width: .7em; height: .7em;}
    [data-testid="stMultiSelect"] [data-tag] button:hover {background: $border;}
    [data-testid="stMultiSelect"] input {color: $text; caret-color: $text;}
    [data-testid="stMultiSelect"] .react-aria-ComboBox > [role="group"]:hover {border-color: $focus;}
    [data-testid="stMultiSelect"] [data-focus-within="true"][role="group"] {
        outline: 2px solid $focus; outline-offset: 2px;}
    [data-testid="stMultiSelect"] button, [data-testid="stSelectbox"] button {color: $text;}
    [data-testid="stSelectbox"] .react-aria-ComboBox > [role="group"] {
        background: $surface; border: 1px solid $control_border; border-radius: 8px;}
    [data-testid="stSelectbox"] [role="combobox"] {
        color: $text; background: transparent; border: 0; outline: 0;}
    [data-testid="stSelectbox"] [role="combobox"]::placeholder {color: $muted;}
    [data-testid="stSelectbox"] .react-aria-ComboBox > [role="group"]:hover {border-color: $focus;}
    [data-testid="stSelectbox"] [data-focus-within="true"][role="group"] {
        outline: 2px solid $focus; outline-offset: 2px;}
    [role="listbox"] {background: $surface; color: $text; border: 1px solid $control_border;}
    [role="option"] {color: $text;}
    [role="option"][aria-selected="true"], [role="option"][data-focused="true"] {
        color: $text; background: $card;}
    [role="option"][aria-selected="true"] {box-shadow: inset 3px 0 0 $focus;}
    [role="option"][data-focused="true"] {outline: 2px solid $focus; outline-offset: -2px;}
    [data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button {
        color: $text; background: $card; border: 1px solid $control_border;}
    .stApp button:focus-visible, .stApp [data-tag]:focus-visible {
        outline: 2px solid $focus; outline-offset: 2px;}
    [data-testid="stAlert"] {border-radius: 10px;}
    @media (max-width: 700px) {
        .stMainBlockContainer {padding: 1.5rem 1rem;}
        .stApp h1 {font-size: 2rem;}
        [data-testid="stTabs"] [role="tablist"] {gap: .8rem;}
    }
    </style>""").substitute(COLORS)
    st.markdown(styles, unsafe_allow_html=True)
