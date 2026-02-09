"""
Simple animation components for Study Buddy UI.
Kept minimal for a clean interface.
"""

def get_loading_animation() -> str:
    """Returns HTML/CSS for a standard loading spinner."""
    return """
    <div class="loading-spinner">
        <div class="spinner"></div>
        <div class="text">Processing...</div>
    </div>
    <style>
        .loading-spinner {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 1rem;
        }
        
        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid #3c3e4a;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .text {
            color: #a0a0a0;
            font-size: 0.9rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """


def get_success_animation() -> str:
    """Returns simple success indicator."""
    return """
    <div style="text-align: center; color: #10b981; padding: 1rem; font-weight: 500;">
        <span style="font-size: 1.5rem;">✓</span> Completed successfully
    </div>
    """


def get_progress_bar(progress: int, text: str = "") -> str:
    """
    Returns HTML/CSS for a simple progress bar.
    """
    return f"""
    <div class="simple-progress">
        <div class="bar-container">
            <div class="bar" style="width: {progress}%;"></div>
        </div>
        {f'<div class="text">{text} ({progress}%)</div>' if text else ''}
    </div>
    <style>
        .simple-progress {{
            margin: 1rem 0;
        }}
        
        .bar-container {{
            width: 100%;
            height: 8px;
            background-color: #262730;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .bar {{
            height: 100%;
            background-color: #667eea;
        }}
        
        .text {{
            margin-top: 0.5rem;
            color: #a0a0a0;
            font-size: 0.8rem;
            text-align: center;
        }}
    </style>
    """


def get_upload_zone_animation() -> str:
    """No special animation for upload zone in simple mode."""
    return ""


def get_card_hover_effect() -> str:
    """No special hover effects in simple mode."""
    return ""


def get_typing_indicator() -> str:
    """Sleek jumping dots for typing animation."""
    return """
    <div class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
    </div>
    <style>
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 4px 0;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background-color: #46b8c9;
            border-radius: 50%;
            display: inline-block;
            animation: jump 1.4s infinite ease-in-out both;
        }
        
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes jump {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1.0); }
        }
    </style>
    """

