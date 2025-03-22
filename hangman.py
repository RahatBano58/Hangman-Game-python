import streamlit as st
import random
from typing import List, Set
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Hangman Game",
    page_icon="🎮",
    layout="centered"
)

# Custom CSS with gradient background, animations, and responsiveness
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(45deg, #ff9a9e, #add8e6, #ea9ef7);
        color: #4f0778;
        font-family: Arial, sans-serif;
        font-size: 20px;
        font-weight: bold;
        animation: fadeIn 2s ease-in-out;
    }

    .stButton > button {
        background-color: #8e44ad;  /* Dark Purple */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        animation: fadeIn 1.5s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #5e3370;  /* Even darker purple on hover */
        animation: scaleUp 0.2s ease-in-out;
    }
    .word-display {
        font-size: 2.5rem;
        letter-spacing: 0.5rem;
        font-family: monospace;
        color: #8e44ad;  /* Dark Purple */
        animation: fadeIn 2s ease-in-out;
    }
    .game-title {
        color: #c655f2;  /* Light Purple */
        text-align: center;
        font-size: 3rem;
        margin-bottom: 2rem;
        animation: titleAnimation 2s infinite;
    }

    @keyframes titleAnimation {
        0%, 100% { transform: rotate(-5deg); }
        50% { transform: rotate(5deg); }
    }

    .category {
        color: #8e44ad;  /* Dark Purple */
        font-weight: bold;
        animation: fadeIn 2s ease-in-out;
    }

    .score {
        font-size: 1.8rem;
        color: #3498db;  /* Light Blue */
        animation: fadeIn 1.5s ease-in-out;
    }

    @media (max-width: 768px) {
        .word-display {
            font-size: 1.8rem;
            letter-spacing: 0.3rem;
        }

        .game-title {
            font-size: 2.5rem;
        }

        .score {
            font-size: 1.2rem;
        }

        .category {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# Word categories and their words
WORDS = {
    "Animals": ["ELEPHANT", "GIRAFFE", "PENGUIN", "KANGAROO", "DOLPHIN", "ZEBRA", "GORILLA", "LION", "TIGER", "MONKEY"],
    "Countries": ["FRANCE", "JAPAN", "BRAZIL", "CANADA", "EGYPT", "CHINA", "INDIA", "NORTH KOREA", "SOUTH KOREA", "RUSSIA"],
    "Fruits": ["APPLE", "BANANA", "ORANGE", "MANGO", "GRAPE", "PINEAPPLE", "KIWI", "PAPAYA", "WATERMELON", "LEMON"],
    "Sports": ["FOOTBALL", "TENNIS", "BASKETBALL", "CRICKET", "SWIMMING", "HOCKEY", "VOLLEYBALL", "BASEBALL", "SOCCER", "GOLF"],
    "Colors": ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN", "BLACK", "WHITE", "GRAY"],
    "Vegetables": ["CARROTS", "CUCUMBERS", "POTATOES", "ONIONS", "LETTUCE", "TOMATOES", "EGGPLANT", "PEAS", "CABBAGE", "SPINACH"],
}

# Hangman ASCII art states
HANGMAN_STATES = [
    """
       --------
       |      |
       |      
       |    
       |      
       |     
    """,
    """
       --------
       |      |
       |      O
       |    
       |      
       |     
    """,
    """
       --------
       |      |
       |      O
       |      |
       |      
       |     
    """,
    """
       --------
       |      |
       |      O
       |     /|
       |      
       |     
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |      
       |     
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |     / 
       |     
    """,
    """
       --------
       |      |
       |      O
       |     /|\\
       |     / \\
       |     
    """
]

def initialize_session_state():
    if 'word' not in st.session_state:
        st.session_state.word = ""
    if 'guessed_letters' not in st.session_state:
        st.session_state.guessed_letters = set()
    if 'wrong_guesses' not in st.session_state:
        st.session_state.wrong_guesses = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'games_played' not in st.session_state:
        st.session_state.games_played = 0
    if 'category' not in st.session_state:
        st.session_state.category = ""

def new_game():
    # Select random category and word
    category = random.choice(list(WORDS.keys()))
    word = random.choice(WORDS[category])
    st.session_state.word = word
    st.session_state.category = category
    st.session_state.guessed_letters = set()
    st.session_state.wrong_guesses = 0
    st.session_state.games_played += 1

def display_word(word: str, guessed_letters: Set[str]) -> str:
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def main():
    st.markdown("<h1 class='game-title'>🎮 Hangman Game</h1>", unsafe_allow_html=True)
    
    initialize_session_state()
    
    # New Game button
    if st.button("New Game") or not st.session_state.word:
        new_game()
    
    # Display score
    st.markdown(f"<p class='score'>Score: {st.session_state.score} | Games Played: {st.session_state.games_played}</p>", 
                unsafe_allow_html=True)
    
    # Display category
    st.markdown(f"<p class='category'>Category: {st.session_state.category}</p>", 
                unsafe_allow_html=True)
    
    # Display hangman
    st.text(HANGMAN_STATES[st.session_state.wrong_guesses])
    
    # Display word
    word_display = display_word(st.session_state.word, st.session_state.guessed_letters)
    st.markdown(f"<p class='word-display'>{word_display}</p>", unsafe_allow_html=True)
    
    # Create 3 rows of letters for the virtual keyboard
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cols_per_row = [9, 9, 8]  # Number of letters in each row
    start_idx = 0
    
    for row_letters in cols_per_row:
        cols = st.columns(row_letters)
        for i, col in enumerate(cols):
            if start_idx + i < len(letters):
                letter = letters[start_idx + i]
                if col.button(
                    letter,
                    key=letter,
                    disabled=letter in st.session_state.guessed_letters
                ):
                    # Process guess
                    st.session_state.guessed_letters.add(letter)
                    if letter not in st.session_state.word:
                        st.session_state.wrong_guesses += 1
        start_idx += row_letters
    
    # Check win/lose conditions
    word_completed = all(letter in st.session_state.guessed_letters 
                        for letter in st.session_state.word)
    
    if word_completed:
        st.success("🎉 Congratulations! You won!")
        st.session_state.score += 1
        if st.button("Play Again"):
            new_game()
    
    elif st.session_state.wrong_guesses >= 6:
        st.error(f"Game Over! The word was: {st.session_state.word}")
        if st.button("Try Again"):
            new_game()

    # Add hint system
    if st.button("Get Hint (Costs 1 point)", disabled=st.session_state.score < 1):
        unguessed_letters = [letter for letter in st.session_state.word if letter not in st.session_state.guessed_letters]
        if unguessed_letters:
            hint_letter = random.choice(unguessed_letters)
            st.session_state.guessed_letters.add(hint_letter)
            st.session_state.score -= 1

if __name__ == "__main__":
    main()
 # Credit line at the bottom
    st.markdown("<p style='text-align: center; margin-top: 10px; color: #fc03a5; font-weight: bold; font-size: 30px; font-family: monospace;'>Created By: Rahat Bano 🎮</p>", unsafe_allow_html=True) 