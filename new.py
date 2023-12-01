import numpy as np
import matplotlib.pyplot as plt

def read_s2p(file_path):
    frequency = []
    S21_mag, S21_phase = [], []
    
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#') and not line.startswith('!'):
                data = line.split()
                frequency.append(float(data[0]))  # Frequency in Hz
                S21_mag.append(float(data[3]))  # S21 magnitude in dB
                S21_phase.append(float(data[4]))  # S21 phase in degrees

    return np.array(frequency), np.array(S21_mag), np.array(S21_phase)

def average_s21(files):
    sum_s21 = 0
    count = 0

    for file in files:
        frequency, S21_mag, S21_phase = read_s2p(file)
        S21_complex = (10 ** (S21_mag / 20)) * np.exp(1j * np.radians(S21_phase))
        sum_s21 += S21_complex
        count += 1


    avg_s21 = sum_s21 / count
    print(avg_s21)
    return frequency, avg_s21


def calibrate_data(reference_data, target_data):
    # Calibrate target data based on reference data
    calibrated_data = target_data / reference_data
    return calibrated_data

def process_files_by_distance(file_groups):
    averaged_data = {}
    for distance, files in file_groups.items():
        _, avg_s21 = average_s21(files)  # Unpack and ignore the frequency
        averaged_data[distance] = avg_s21
    return averaged_data

def plot_power_delay_profile(frequency, avg_s21, max_time_ns=150, color='blue'):
    time_signal = np.fft.ifft(avg_s21)
    time_signal_power = np.abs(time_signal) ** 2

    frequency_resolution = frequency[1] - frequency[0]
    time_step = 1 / ((len(frequency)-1) * frequency_resolution)  # in seconds
    time_step_ns = time_step * 1e9  # Convert time step to nanoseconds
    time_array_ns = np.arange(len(time_signal)) * time_step_ns

    # Truncate the graph at max_time_ns
    max_index = np.where(time_array_ns > max_time_ns)[0][0]
    time_array_ns = time_array_ns[:max_index]
    time_signal_power = time_signal_power[:max_index]

    plt.figure(figsize=(10, 6))

# Assuming calibrated_data is a dictionary with distances as keys and S21 data as values
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange']  # Add more colors if needed
    for i, (distance, calib_s21) in enumerate(calibrated_data.items()):
        plot_power_delay_profile(frequency, calib_s21, max_time_ns=150, color=colors[i % len(colors)])

    plt.title('Calibrated Power Delay Profiles')
    plt.xlabel('Time Delay (ns)')
    plt.ylabel('Power (dB)')
    plt.grid(True)
    plt.legend([f'{d}m' for d in calibrated_data.keys()])
    plt.show()




file_groups = {
    1: ['/Users/user/Desktop/Advanced_Measurement/uwb 2/1s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/1s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/1s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/1s24.s2p'],  # 1 meter files
    2:['/Users/user/Desktop/Advanced_Measurement/uwb 2/2s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/2s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/2s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/2s24.s2p'],  # 2 meter files
  
    3:['/Users/user/Desktop/Advanced_Measurement/uwb 2/3s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/3s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/3s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/3s24.s2p'],
    4:['/Users/user/Desktop/Advanced_Measurement/uwb 2/4s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/4s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/4s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/4s24.s2p'],
    5:['/Users/user/Desktop/Advanced_Measurement/uwb 2/5s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/5s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/5s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/5s24.s2p'],
    6:['/Users/user/Desktop/Advanced_Measurement/uwb 2/6s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/6s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/6s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/6s24.s2p'],
    7:['/Users/user/Desktop/Advanced_Measurement/uwb 2/7s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/7s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/7s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/7s24.s2p'],
    8:['/Users/user/Desktop/Advanced_Measurement/uwb 2/8s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/8s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/8s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/8s24.s2p'],
    9:['/Users/user/Desktop/Advanced_Measurement/uwb 2/9s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/9s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/9s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/9s24.s2p'],
    10:['/Users/user/Desktop/Advanced_Measurement/uwb 2/10s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/10s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/10s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/10s24.s2p'],
    11:['/Users/user/Desktop/Advanced_Measurement/uwb 2/11s13.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/11s14.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/11s23.s2p', 
         '/Users/user/Desktop/Advanced_Measurement/uwb 2/11s24.s2p']
}



# Process and average the files for each distance
averaged_data = process_files_by_distance(file_groups)

# Calibrate data against the 1-meter data
calibrated_data = {}
for distance, avg_s21 in averaged_data.items():
    if distance == 1:
        ref_s21 = avg_s21  # Reference data from 1 meter
    else:
        calibrated_data[distance] = calibrate_data(ref_s21, avg_s21)

# Plot calibrated data for each distance
frequency, S21_mag, S21_phase = read_s2p(file_groups[1][0])
  # Assuming all files have the same frequency points



for distance, calib_s21 in calibrated_data.items():
   plot_power_delay_profile(frequency, calib_s21)












