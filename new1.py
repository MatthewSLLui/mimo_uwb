import numpy as np
import matplotlib.pyplot as plt

def read_s2p(file_path):
    frequency = []
    S21_mag_linear, S21_phase_rad = [], []
    
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#') and not line.startswith('!'):
                data = line.split()
                frequency.append(float(data[0]))  # Frequency in Hz
                S21_mag_linear.append(10 ** (float(data[3]) / 20))  # S21 magnitude in dB  10 ** (float(data[3]) / 20)
                S21_phase_rad.append(float(data[4]))  # S21 phase in degrees
    #print(S21_phase)
    return np.array(frequency), np.array(S21_mag_linear), np.array(S21_phase_rad)
import numpy as np





def plot_power_delay_profile(file_paths):
    
    accumulated_S21_mag = 0
    
    accumulated_S21_phase = 0
    count = 0

    for file_path in file_paths:
        frequency, S21_mag_linear, S21_phase_rad = read_s2p(file_path)
        
        accumulated_S21_mag += S21_mag_linear
        accumulated_S21_phase += S21_phase_rad
        count += 1
    
    
    #print()
    avg_S21_mag = accumulated_S21_mag // 4
    avg_S21_phase = accumulated_S21_phase //4

    S21_avg_complex= avg_S21_mag * np.exp(1j * np.radians(avg_S21_phase))
    
    
    time_signal = np.fft.ifft(S21_avg_complex)
    time_signal_power = np.abs(time_signal) ** 2

    frequency_resolution = frequency[1] - frequency[0]
    time_step = 1 / ((len(frequency)-1) * frequency_resolution)  # in seconds
    time_step_ns = time_step * 1e9  # Convert time step to nanoseconds
    time_array_ns = np.arange(len(time_signal)) * time_step_ns

    plt.figure(figsize=(8, 4))
    plt.plot(time_array_ns, 10 * np.log10(time_signal_power))
    plt.title('Average Power Delay Profile')
    plt.xlabel('Time Delay (ns)')
    plt.ylabel('Power (dB)')
    plt.grid(True)
    plt.show()

# List of S2P file paths
file_paths = ['/Users/user/Desktop/Advanced_Measurement/uwb 2/1s13.s2p',
               '/Users/user/Desktop/Advanced_Measurement/uwb 2/1s14.s2p',
                 '/Users/user/Desktop/Advanced_Measurement/uwb 2/1s23.s2p',
                   '/Users/user/Desktop/Advanced_Measurement/uwb 2/1s24.s2p']

plot_power_delay_profile(file_paths)
