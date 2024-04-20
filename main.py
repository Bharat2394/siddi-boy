import pandas as pd
import os
import cv2
import phe as paillier
from tqdm import tqdm
import json
import numpy as np
from phe import PaillierPublicKey, PaillierPrivateKey, EncryptedNumber
import matplotlib.pyplot as plt

# Function to read patient data from CSV
def read_patient_data(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Function to load patient images
def load_patient_images(image_folder, patient_ids):
    images = {}
    for patient_id in tqdm(patient_ids, desc="Loading Images"):
        image_path = os.path.join(image_folder, f"{patient_id}.jpg")  
        if os.path.exists(image_path):
            images[patient_id] = cv2.imread(image_path)
    return images

# Function to perform Paillier encryption on patient IDs
def encrypt_patient_data(pubkey, patient_id):
    encrypted_id = pubkey.encrypt(patient_id)
    return encrypted_id

# Function to perform computation on encrypted data
def perform_computation_on_encrypted_data(encrypted_data):
    # Implement computations on encrypted data
    pass

# Function to decrypt patient IDs
def decrypt_patient_data(privkey, encrypted_data):
    decrypted_id = privkey.decrypt(encrypted_data)
    return decrypted_id

# Function to save keys to a text file
def save_keys_to_text(keys_mapping, filename):
    with open(filename, 'w') as file:
        for patient_id, keys in keys_mapping.items():
            public_key_str = f"Public key for patient ID {patient_id}: {keys['public_key'].n}\n"
            private_key_str = f"Private key for patient ID {patient_id}: {keys['private_key'].p}, {keys['private_key'].q}\n"
            file.write(public_key_str)
            file.write(private_key_str)

# Function to derive unique public and private keys for each patient
def derive_keys(master_public_key, master_private_key, patient_id):
    # Generate a unique public key for the patient
    derived_public_key = PaillierPublicKey(n=master_public_key.n)
    # Generate a unique private key for the patient
    derived_private_key = PaillierPrivateKey(public_key=derived_public_key, p=master_private_key.p, q=master_private_key.q)
    return derived_public_key, derived_private_key

# Main function
def main():
    # Update CSV file path
    csv_file = r"C:/Users/Bharat Gupta/Dropbox/My PC (DESKTOP-JQLKL3B)/Desktop/SIDDI BOY/THESIS/Book1.csv"
    # Read patient data from CSV
    patient_data = read_patient_data(csv_file)
    patient_ids = patient_data['patient_id'].tolist()

    # Update image folder path
    image_folder = r"C:/Users/Bharat Gupta/Dropbox/My PC (DESKTOP-JQLKL3B)/Desktop/SIDDI BOY/THESIS/dataset"
    # Load patient images
    patient_images = load_patient_images(image_folder, patient_ids)

    # Generate master keys
    master_public_key, master_private_key = paillier.generate_paillier_keypair()

    # Generate and store keys for each patient
    keys_mapping = {}
    for patient_id in tqdm(patient_ids, desc="Generating Keys"):
        derived_public_key, derived_private_key = derive_keys(master_public_key, master_private_key, patient_id)
        keys_mapping[patient_id] = {'public_key': derived_public_key, 'private_key': derived_private_key}

    # Save keys to text file
    save_keys_to_text(keys_mapping, 'keys1.txt')

    # Encrypt and process patient data
    encrypted_patient_data = {}
    for patient_id in tqdm(patient_ids, desc="Encrypting Patient IDs"):
        encrypted_id = encrypt_patient_data(keys_mapping[patient_id]['public_key'], patient_id)
        encrypted_patient_data[patient_id] = encrypted_id

    # Perform computation on encrypted data
    perform_computation_on_encrypted_data(encrypted_patient_data)

    # Decrypt and associate patient data with images
    decrypted_patient_data = {}
    for patient_id, encrypted_id in tqdm(encrypted_patient_data.items(), desc="Decrypting Patient IDs"):
        decrypted_id = decrypt_patient_data(keys_mapping[patient_id]['private_key'], encrypted_id)
        patient_image = patient_images.get(patient_id)
        # Associate decrypted data with patient image
        decrypted_patient_data[patient_id] = {'id': decrypted_id, 'image': patient_image}

    # Output decrypted patient data with associated images
    for patient_id, data_with_image in tqdm(decrypted_patient_data.items(), desc="Displaying Data"):
        print(f"ID: {patient_id}")
        decrypted_info = patient_data[patient_data['patient_id'] == patient_id]
        if not decrypted_info.empty:
            patient_info = f"Name: {decrypted_info['name'].values[0]}, Age: {decrypted_info['age'].values[0]}, Gender: {decrypted_info['gender'].values[0]}, Insurance: {decrypted_info['insurance'].values[0]}, Past History: {decrypted_info['past history'].values[0]}"
            print(f"Decrypted Information: {patient_info}")
            # Display the image with patient information using Matplotlib
            plt.imshow(cv2.cvtColor(data_with_image['image'], cv2.COLOR_BGR2RGB))
            plt.title(patient_info)
            plt.axis('off')
            plt.show()

if __name__ == '__main__':
    main()