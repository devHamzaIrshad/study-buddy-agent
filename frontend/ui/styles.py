"""
Clean, simple UI styles with dark theme.
"""

def get_custom_css() -> str:
    """Returns custom CSS for simple, clean UI."""
    return """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        scroll-behavior: auto !important;
    }
    
    /* Main app background - Deep Navy matching logo */
    .stApp {
        background-color: #0d1117;
    }
    
    /* Logo Styling */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #46b8c9;
        box-shadow: 0 0 15px rgba(70, 184, 201, 0.3);
        background-color: white; /* Ensures background is clean before masking if needed */
    }
    
    /* Clean Headers */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    h1 { 
        font-size: 2.2rem;
        color: #46b8c9; /* Teal accent */
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Cards & Containers */
    .stMarkdown, .stChatMessage, .element-container {
        border-radius: 12px;
    }
    
    /* Chat messages - Theme Matched */
    .stChatMessage {
        background-color: transparent;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border: 1px solid #30363d;
    }
    
    .stChatMessage:hover {
        border-color: #46b8c9;
    }
    
    /* User message card */
    [data-testid="stChatMessageContent"][data-role="user"] {
        background-color: #161b22;
        border-radius: 12px;
    }
    
    /* Assistant message card */
    [data-testid="stChatMessageContent"][data-role="assistant"] {
        background-color: #0d1117;
        border-left: 3px solid #46b8c9;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Button styling - Teal Theme */
    .stButton > button {
        background-color: #21262d;
        color: white;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #30363d;
        border-color: #46b8c9;
        color: #46b8c9;
    }
    
    /* Primary buttons */
    button[kind="primary"] {
        background-color: #46b8c9 !important;
        color: #0d1117 !important;
        border: none !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #3aa3b3 !important;
        box-shadow: 0 0 10px rgba(70, 184, 201, 0.4) !important;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #161b22;
        border: 1px dashed #30363d;
        border-radius: 8px;
    }
    
    /* Chat input styling */
    .stChatInput > div {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    
    .stChatInput > div:focus-within {
        border-color: #46b8c9;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: #46b8c9;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #46b8c9;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
    }
    
    /* Popover button styling for the "+" icon */
    [data-testid="stPopover"] > div:first-child > button {
        background-color: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #46b8c9 !important;
        font-size: 1.5rem !important;
        padding: 0 !important;
        margin-top: 5px !important;
    }
    
    [data-testid="stPopover"] > div:first-child > button:hover {
        border-color: #46b8c9 !important;
        background-color: #30363d !important;
    }
    
    /* Hide the default popover label arrow if possible */
    [data-testid="stPopover"] div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
    }
    </style>
    """

