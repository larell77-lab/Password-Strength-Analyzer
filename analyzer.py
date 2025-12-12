import re
import os

# --- SETUP: Load the blocklist ---
def load_common_passwords():
    # Look for the file in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "common_passwords.txt")
    
    if not os.path.exists(filepath):
        print(f"Warning: Could not find '{filepath}'.") 
        return set()
    
    with open(filepath, 'r') as f:
        return set(line.strip().lower() for line in f)

# --- LOGIC: Judge the password ---
def assess_password_strength(password, common_passwords):
    score = 0
    recommendations = []
    
    # Check 1: Is it in the blocklist?
    if password.lower() in common_passwords:
        return {"rating": "WEAK (Compromised)", "score": 0, "recommendations": ["Change immediately! Common password detected."]}

    # Check 2: Length
    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    else: recommendations.append("Make it longer (8+ chars).")

    # Check 3: Variety (UPPER, lower, 123, !@#)
    if re.search(r"[a-z]", password): score += 1
    else: recommendations.append("Add lowercase letters.")
    
    if re.search(r"[A-Z]", password): score += 1
    else: recommendations.append("Add uppercase letters.")
    
    if re.search(r"\d", password): score += 1
    else: recommendations.append("Add numbers.")
    
    if re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password): score += 1
    else: recommendations.append("Add special characters.")

    # Rating
    if score < 3: rating = "WEAK"
    elif score < 5: rating = "MODERATE"
    else: rating = "STRONG"

    return {"score": score, "rating": rating, "recommendations": recommendations}

# --- MAIN: Run the menu ---
def main():
    print("--- PASSWORD ANALYZER ---")
    blocklist = load_common_passwords()
    print(f"(Loaded {len(blocklist)} passwords from blocklist)")

    while True:
        pwd = input("\nEnter password to test (or 'q' to quit): ")
        if pwd == 'q': break
        
        result = assess_password_strength(pwd, blocklist)
        print(f"Rating: {result['rating']} (Score: {result['score']}/6)")
        for rec in result['recommendations']:
            print(f"- {rec}")

if __name__ == "__main__":
    main()