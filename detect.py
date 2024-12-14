import sys
import os
import time
from SecuGen import *  # Import the SecuGen SDK or whatever specific module you have

# Initialize the SecuGen Fingerprint scanner
def initialize_scanner():
    try:
        # Create a fingerprint scanner object
        scanner = SecuGenFingerprintScanner()
        # Initialize the scanner
        scanner.initialize()
        return scanner
    except Exception as e:
        print(f"Error initializing scanner: {e}")
        sys.exit(1)

# Capture the fingerprint and save it to a file
def capture_fingerprint(scanner):
    try:
        print("Please place your finger on the scanner.")
        # Wait for a fingerprint to be captured
        while not scanner.capture_fingerprint():
            print("No fingerprint detected. Try again.")
            time.sleep(1)

        # Save the captured fingerprint data as a file
        fingerprint_data = scanner.get_fingerprint_data()
        file_path = "fingerprint_template.fpt"  # You can specify any filename and location
        with open(file_path, "wb") as f:
            f.write(fingerprint_data)
        print(f"Fingerprint saved to {file_path}")

    except Exception as e:
        print(f"Error capturing fingerprint: {e}")
        sys.exit(1)

# Main function to run the script
def main():
    # Initialize the scanner
    scanner = initialize_scanner()

    # Capture and save the fingerprint
    capture_fingerprint(scanner)

    # Clean up and close the scanner
    scanner.close()

if __name__ == "__main__":
    main()
