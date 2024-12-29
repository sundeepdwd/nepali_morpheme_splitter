# Define the necessary character sets for Nepali syllable parsing
FIRST_SYMBOLS = ['ऀ', 'ँ', 'ं', 'ः']
VOWELS = [
    'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऌ',
    'ऍ', 'ऎ', 'ए', 'ऐ', 'ऑ', 'ऒ', 'ओ', 'औ'
]
CONSONANTS = [
    'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
    'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न',
    'ऩ', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ऱ', 'ल',
    'ळ', 'ऴ', 'व', 'श', 'ष', 'स', 'ह', 'त्र', 'क्ष'
]
MATRAS = ["ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ"]
HALANT = '्'
SPLIT_MARKER = '+'

def parse_nepali_syllables(word, return_type="string"):
    """
    Parses a Nepali word into its constituent syllables.

    Parameters:
    - word (str): The Nepali word to parse.
    - return_type (str): The type of value to return. 
                         "string" returns a '+' separated string of syllables.
                         "list" returns a list of syllables.

    Returns:
    - str or list: The parsed syllables either as a string or list.
    """
    syllables = []
    current_syllable = ""
    i = 0
    length = len(word)

    while i < length:
        char = word[i]

        if char in VOWELS:
            # Standalone vowel or vowel following a consonant
            if current_syllable:
                syllables.append(current_syllable)
                current_syllable = ""
            syllables.append(char)
            i += 1

        elif char in CONSONANTS:
            # Start of a consonant cluster or a single consonant
            current_syllable += char
            i += 1

            # Check if the next character is a halant indicating a consonant cluster
            if i < length and word[i] == HALANT:
                current_syllable += HALANT
                i += 1
                # Append the next consonant to form the cluster
                if i < length and word[i] in CONSONANTS:
                    current_syllable += word[i]
                    i += 1
                else:
                    # Halant without a following consonant; treat halant as part of the syllable
                    pass
            # Check for matra (vowel sign) following the consonant
            if i < length and word[i] in MATRAS:
                current_syllable += word[i]
                i += 1
                syllables.append(current_syllable)
                current_syllable = ""
            else:
                # No matra; syllable ends with the consonant
                syllables.append(current_syllable)
                current_syllable = ""

        elif char in FIRST_SYMBOLS or char in MATRAS:
            # Vowel signs or diacritics that modify the previous character
            if current_syllable:
                current_syllable += char
            else:
                # Diacritics without a preceding consonant or vowel
                syllables.append(char)
            i += 1

        else:
            # Any other character (punctuation, numbers, etc.)
            if current_syllable:
                syllables.append(current_syllable)
                current_syllable = ""
            syllables.append(char)
            i += 1

    # Append any remaining syllable
    if current_syllable:
        syllables.append(current_syllable)

    # Join syllables with '+' if string is desired
    if return_type == "string":
        return SPLIT_MARKER.join(syllables)
    elif return_type == "list":
        return syllables
    else:
        raise ValueError("Invalid return_type. Choose 'string' or 'list'.")

# Example usage:
if __name__ == "__main__":
    nepali_word = "नेपाल"  # Example Nepali word
    parsed = parse_nepali_syllables(nepali_word, return_type="list")
    print("Parsed Syllables:", parsed)
