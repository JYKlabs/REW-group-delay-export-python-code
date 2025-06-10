import requests
import base64
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d

# Base URL of the API
base_url = 'http://localhost:4735'

# Function to fetch all measurements' UUIDs
def get_all_measurements():
    response = requests.get(f'{base_url}/measurements')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error fetching measurements: {response.status_code}')

# Function to fetch Group Delay
def get_group_delay(uuid):
    response = requests.get(f'{base_url}/measurements/{uuid}/group-delay')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error fetching group delay: {response.status_code}')

# Function to generate a unique filename
def get_unique_filename(directory, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base} {counter}{extension}"
        counter += 1
    return new_filename

# Fetch all measurements' UUIDs
measurements = get_all_measurements()

# Set the path for saving files
output_folder = '/Users/jooyoungkim/Desktop/Folder'
os.makedirs(output_folder, exist_ok=True)

for key, measurement in measurements.items():
    uuid = measurement['uuid']
    title = measurement['title']

    # Fetch Group Delay data
    group_delay_data = get_group_delay(uuid)

    # Encoded string from API
    encoded_string = group_delay_data['magnitude']

    # Decode the string
    decoded_bytes = base64.b64decode(encoded_string)

    # Convert the decoded bytes to a numpy array of Big-Endian float32
    decoded_values = np.frombuffer(decoded_bytes, dtype=">f4")  # Use Big-Endian format

    # Set the frequency range (40-250Hz)
    freq_step = group_delay_data['freqStep']
    actual_start_freq = freq_step  # Set actual_start_freq to freq_step for GD, 12 times freq_step for EGD
    start_freq = 40
    end_freq = 250

    # Save Group Delay data to a text file
    output_path = os.path.join(output_folder, get_unique_filename(output_folder, f'{title} group delay values.txt'))
    with open(output_path, 'w') as f:
        for i, gd in enumerate(decoded_values):
            freq = actual_start_freq + i * freq_step
            f.write(f'{freq:.3f} Hz, {gd:.6f} seconds\n')

    # Extract Group Delay values within the 40-250Hz range
    start_index = int((start_freq - actual_start_freq) / freq_step)
    end_index = int((end_freq - actual_start_freq) / freq_step)
    group_delay_values = decoded_values[start_index:end_index]

    # Generate the accurate frequency array
    frequencies = np.arange(
        actual_start_freq + start_index * freq_step,
        actual_start_freq + end_index * freq_step,
        freq_step
    )

    # Create the interpolation function
    interpolation = interp1d(frequencies, group_delay_values, kind='cubic')

    # Generate a finer frequency range
    fine_frequencies = np.linspace(start_freq, end_freq, 210000)
    fine_frequencies = fine_frequencies[fine_frequencies <= frequencies[-1]]  # Limit to the maximum range
    fine_group_delay = interpolation(fine_frequencies)

    # Find the maximum value from the interpolated data
    fine_max_index = np.argmax(np.abs(fine_group_delay))
    fine_max_value = fine_group_delay[fine_max_index]
    fine_max_freq = fine_frequencies[fine_max_index]

    print(f'Max Group Delay (absolute value) after interpolation: {fine_max_value:.6f} seconds at {fine_max_freq:.3f} Hz')

    # Save the maximum value and frequency to a text file
    max_value_line = f'Max Group Delay (absolute value): {fine_max_value:.6f} seconds at {fine_max_freq:.3f} Hz'
    max_output_path = os.path.join(output_folder, get_unique_filename(output_folder, f'{title} group delay max value.txt'))
    with open(max_output_path, 'w') as f:
        f.write(max_value_line)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, group_delay_values, label='Group Delay')
    plt.plot(fine_frequencies, fine_group_delay, label='Interpolated Group Delay', linestyle='--')
    plt.scatter([fine_max_freq], [fine_max_value], color='red', label='Max Value', zorder=5)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Group Delay (seconds)')
    plt.title(f'Excess Group Delay by Frequency for {title}')
    plt.legend()
    plt.grid(True)

    # Save the graph as an image file
    graph_output_path = os.path.join(output_folder, get_unique_filename(output_folder, f'{title} group delay graph.png'))
    plt.savefig(graph_output_path)
    plt.close()
